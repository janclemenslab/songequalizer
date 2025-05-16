from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import random
import json
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import glob

app = FastAPI(title="Image Comparison App")

# Configure templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/fig", StaticFiles(directory="fig"), name="fig")

# Path to save responses
RESPONSES_FILE = "responses.json"

# Function to get all image files from the fig folder
def get_all_images() -> List[str]:
    fig_dir = "fig"
    # Get all PNG files in the fig directory
    image_files = glob.glob(os.path.join(fig_dir, "*.png"))
    return image_files

# Function to get a random pair of images
def get_random_image_pair() -> Tuple[str, str]:
    image_files = get_all_images()
    
    # Select two random images
    selected_images = random.sample(image_files, 2)
    
    # Convert to relative paths for the template
    relative_paths = [os.path.basename(img) for img in selected_images]
    
    return relative_paths[0], relative_paths[1]

# Function to save user responses
def save_response(image1: str, image2: str, same: bool, username: str) -> None:
    response_data = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "image1": image1,
        "image2": image2,
        "same": same
    }
    
    # Create the file if it doesn't exist
    if not os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "w") as f:
            json.dump([], f)
    
    # Read existing responses
    with open(RESPONSES_FILE, "r") as f:
        responses = json.load(f)
    
    # Append new response
    responses.append(response_data)
    
    # Write back to file
    with open(RESPONSES_FILE, "w") as f:
        json.dump(responses, f, indent=2)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, username: Optional[str] = Cookie(None)):
    # If no username cookie exists, redirect to login page
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    # Get a random pair of images
    image1, image2 = get_random_image_pair()
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "image1": image1, 
            "image2": image2,
            "username": username
        }
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=RedirectResponse)
async def login(username: str = Form(...)):
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="username", value=username)
    return response

@app.post("/submit", response_class=RedirectResponse)
async def submit(
    image1: str = Form(...), 
    image2: str = Form(...), 
    same: str = Form(...),
    username: Optional[str] = Cookie(None)
):
    # Convert string 'true'/'false' to boolean
    is_same = (same.lower() == 'true')
    
    # Save the response with username
    if username:
        save_response(image1, image2, is_same, username)
    else:
        # Fallback in case username is not set
        save_response(image1, image2, is_same, "anonymous")
    
    # Redirect back to the main page for the next pair
    return RedirectResponse(url="/", status_code=303)

@app.get("/quit", response_class=HTMLResponse)
async def quit(request: Request, username: Optional[str] = Cookie(None)):
    response = templates.TemplateResponse("quit.html", {"request": request, "username": username})
    # Clear the username cookie
    response.delete_cookie(key="username")
    return response

@app.get("/download-responses")
async def download_responses():
    """Endpoint to download the responses.json file"""
    if os.path.exists(RESPONSES_FILE):
        return FileResponse(
            path=RESPONSES_FILE, 
            filename="responses.json",
            media_type="application/json"
        )
    else:
        return JSONResponse(
            content={"error": "No responses file found"},
            status_code=404
        )

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    """Admin page to monitor responses and download data"""
    response_count = 0
    users = set()
    
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "r") as f:
            try:
                responses = json.load(f)
                response_count = len(responses)
                
                # Extract unique usernames from responses
                for response in responses:
                    if "username" in response:
                        users.add(response["username"])
                    
            except json.JSONDecodeError:
                response_count = 0
    
    return templates.TemplateResponse(
        "admin.html", 
        {
            "request": request,
            "response_count": response_count,
            "user_count": len(users),
            "users": sorted(list(users))
        }
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
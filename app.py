from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import random
import json
from datetime import datetime
from typing import List, Tuple, Dict
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
def save_response(image1: str, image2: str, same: bool) -> None:
    response_data = {
        "timestamp": datetime.now().isoformat(),
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
async def index(request: Request):
    # Get a random pair of images
    image1, image2 = get_random_image_pair()
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "image1": image1, 
            "image2": image2
        }
    )

@app.post("/submit", response_class=RedirectResponse)
async def submit(
    image1: str = Form(...), 
    image2: str = Form(...), 
    same: str = Form(...)
):
    # Convert string 'true'/'false' to boolean
    is_same = (same.lower() == 'true')
    
    # Save the response
    save_response(image1, image2, is_same)
    
    # Redirect back to the main page for the next pair
    return RedirectResponse(url="/", status_code=303)

@app.get("/quit", response_class=HTMLResponse)
async def quit(request: Request):
    return templates.TemplateResponse("quit.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
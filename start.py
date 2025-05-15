import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Start the server
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=port,
        workers=1,  # Number of worker processes
        log_level="info"
    )
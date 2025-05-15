# Image Comparison App

This application displays pairs of images from the `fig` folder and asks the user to determine whether the images in each pair are the same or different. The app selects random pairs of images until the user decides to quit. All user responses are saved.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Jinja2

## Installation

1. Install the required packages:

```bash
pip install fastapi uvicorn jinja2
```

2. Make sure your images are in the `fig` directory (the app assumes there are PNG files in this directory).

## Running the App

1. Start the application:

```bash
python app.py
```

2. Open your browser and navigate to:

```
http://localhost:8000
```

## How to Use

1. The app will display two randomly selected images from the `fig` folder.
2. Choose if the images are the same or different using:
   - Click the "Same" button or press the `S` key if you think the images are the same
   - Click the "Different" button or press the `D` key if you think they're different
3. After submitting your answer, a new pair of images will be shown.
4. Click the "Quit" button when you want to end the session.
5. All responses are saved in a file called `responses.json` in the application directory.
6. After quitting, you can download the responses directly using the "Download Responses" button.

## Features

- **Consistent Image Display**: All images are displayed with the same height for easy comparison, regardless of their original dimensions
- **Keyboard Shortcuts**: Use `S` key for "Same" and `D` key for "Different" to quickly respond
- **Response Tracking**: All user responses are automatically saved with timestamps
- **Admin Dashboard**: Accessible via the "Admin" link in the top-right corner or directly at `/admin`
- **Download Responses**: Download collected responses in JSON format from multiple locations

## Accessing Response Data

There are multiple ways to access the response data:

1. **After Quitting**: When you end a session, a "Download Responses" button appears on the quit page
2. **Admin Dashboard**: Visit the `/admin` page to see response statistics and download data
3. **Direct URL**: Access `/download-responses` directly to download the JSON file
4. **Local File**: The `responses.json` file is stored in the application directory

## Response Data Format

The `responses.json` file contains an array of response objects with the following structure:

```json
{
  "timestamp": "2023-07-01T12:34:56.789012",
  "image1": "example_image1.png",
  "image2": "example_image2.png",
  "same": true
}
```

- `timestamp`: The date and time when the response was submitted.
- `image1`: The filename of the first image.
- `image2`: The filename of the second image.
- `same`: `true` if the user indicated the images are the same, `false` otherwise.


## Deploy
To deploy your app on Render for free:

  1. Create a GitHub repository for your project and push all files including the ones I just
  created.
  2. Sign up at https://render.com (free account)
  3. Once logged in:
    - Click "New +" → "Web Service"
    - Connect your GitHub account
    - Select your repository
    - Render will automatically detect your configuration from render.yaml
  4. Alternative manual setup:
    - Name: songequalizer
    - Runtime: Python 3
    - Build Command: pip install -r requirements.txt
    - Start Command: python start.py
  5. Select the free plan and click "Create Web Service"

  Your app will be deployed to a URL like https://songequalizer.onrender.com.

  Note: The free tier has limitations - your app will sleep after 15 minutes of inactivity and
   has a monthly usage limit.
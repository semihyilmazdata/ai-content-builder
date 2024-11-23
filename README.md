# AI Content Builder - YouTube Video Summarizer

A web application that automatically generates summaries of YouTube videos using their transcripts. Built with FastAPI backend and HTML/JavaScript frontend.

## Project Structure
```
ai-content-builder/
├── backend/
│   ├── main.py
│   └── youtube_summarizer.py
├── frontend/
│   └── index.html
├── requirements.txt
└── README.md
```

## Prerequisites
- Python 3.9+
- pip (Python package installer)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/semihyilmazdata/ai-content-builder.git
cd ai-content-builder
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv youtube_summarizer_env

# Activate virtual environment
# On Windows:
youtube_summarizer_env\Scripts\activate
# On macOS/Linux:
source youtube_summarizer_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
cd backend
uvicorn main:app --reload --port 8000
```
The backend server will be running at `http://localhost:8000`

### 3. Frontend Setup
```bash
# In a new terminal, navigate to the frontend directory
cd frontend

# Start a simple HTTP server
# On Python 3
python -m http.server 5500
```
The frontend will be accessible at `http://localhost:5500`

## Usage

1. Open your browser and go to `http://localhost:5500`
2. Paste a YouTube URL into the input field
3. Click "Summarize" or press Enter
4. Wait for the summary to be generated
5. View the summary and statistics

## API Endpoints

### POST `/summarize`
Generates a summary of a YouTube video.

Request body:
```json
{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Response:
```json
{
    "success": true,
    "data": {
        "summary": "Generated summary text",
        "stats": {
            "transcript_length": 1000,
            "summary_length": 200,
            "timing": {
                "total_time": 15.35,
                "url_processing_time": 0.001,
                "transcript_fetch_time": 1.45,
                "summarization_time": 8.67
            }
        }
    }
}
```

### GET `/health`
Health check endpoint to verify the API is running.

Response:
```json
{
    "status": "healthy",
    "timestamp": "2024-11-23T12:34:56.789Z"
}
```

## Common Issues

1. **CORS Issues**: If you see CORS errors in the console, make sure both backend and frontend are running on the specified ports.

2. **Model Download**: On first run, the application will download the required AI models. This might take some time depending on your internet connection.

3. **Video Unavailable**: Make sure the YouTube video has closed captions available.

## Development

- Backend is built with FastAPI and uses the transformers library for text summarization
- Frontend is built with HTML, JavaScript, and Tailwind CSS
- The application uses YouTube's transcript API to fetch video captions

## License
MIT
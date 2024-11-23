# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_summarizer import VideoSummarizer

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize summarizer
print("Initializing Summarizer...")
summarizer = VideoSummarizer()
print("Summarizer Ready!")

class VideoRequest(BaseModel):
    url: str

@app.post("/summarize")
async def summarize_video(request: VideoRequest):
    try:
        print(f"Received request for URL: {request.url}")
        result = summarizer.get_video_summary(request.url)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        print("Successfully processed video")
        return {
            "success": True,
            "data": {
                "summary": result["summary"],
                "stats": {
                    "transcript_length": result["transcript_length"],
                    "summary_length": result["summary_length"],
                    "timing": result["timing_stats"]
                }
            }
        }
    except Exception as e:
        print(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_endpoint():
    return {"message": "Backend is working!"}
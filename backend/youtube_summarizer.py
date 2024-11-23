import os
import time
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

# Set tokenizers parallelism to False to avoid the warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class VideoSummarizer:
    def __init__(self):
        self.timing_stats = {}
        print("Initializing summarizer... (will download model only on first run)")
        start_time = time.time()
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.timing_stats['model_load_time'] = time.time() - start_time
        print(f"Summarizer ready! (Loaded in {self.timing_stats['model_load_time']:.2f} seconds)")

    def extract_video_id(self, url):
        """Extract YouTube video ID from URL."""
        start_time = time.time()
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?]*)',
            r'youtube\.com/embed/([^&\n?]*)',
            r'youtube\.com/v/([^&\n?]*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                self.timing_stats['url_processing_time'] = time.time() - start_time
                return match.group(1)
        return None

    def get_video_transcript(self, video_id):
        """Get video transcript using YouTube Transcript API."""
        start_time = time.time()
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([item['text'] for item in transcript_list])
            self.timing_stats['transcript_fetch_time'] = time.time() - start_time
            return transcript_text
        except Exception as e:
            print(f"Transcript error: {str(e)}")
            return None

    def chunk_text(self, text, chunk_size=500):
        """Split text into smaller chunks for processing."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_length += len(word) + 1  # +1 for space
            if current_length > chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def summarize_content(self, text):
        """Summarize text using transformers."""
        if not text:
            return None
            
        try:
            start_time = time.time()
            # Split text into chunks
            chunks = self.chunk_text(text)
            self.timing_stats['chunking_time'] = time.time() - start_time
            
            # Summarize each chunk
            print("Generating summary...")
            summaries = []
            summary_start_time = time.time()
            for i, chunk in enumerate(chunks, 1):
                if len(chunk.strip()) < 50:  # Skip very short chunks
                    continue
                chunk_start_time = time.time()
                print(f"Processing chunk {i}/{len(chunks)}...")
                
                # Calculate dynamic max_length based on input length
                input_length = len(chunk.split())
                max_length = min(130, max(30, input_length // 2))
                
                summary = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min(30, max_length - 10),
                    do_sample=False
                )
                summaries.append(summary[0]['summary_text'])
                print(f"Chunk {i} processed in {time.time() - chunk_start_time:.2f} seconds")
            
            self.timing_stats['summarization_time'] = time.time() - summary_start_time
            
            # Combine summaries
            final_summary = ' '.join(summaries)
            return final_summary
            
        except Exception as e:
            print(f"Summarization error: {str(e)}")
            return None

    def get_video_summary(self, url):
        """Main function to get video content summary."""
        self.timing_stats = {}  # Reset timing stats for new request
        overall_start_time = time.time()
        
        # Extract video ID
        video_id = self.extract_video_id(url)
        if not video_id:
            return {"error": "Invalid YouTube URL"}
        
        # Get transcript
        print("Fetching video transcript...")
        transcript = self.get_video_transcript(video_id)
        if not transcript:
            return {"error": "Failed to fetch video transcript. The video might not have subtitles/transcript available."}
        
        # Generate summary
        summary = self.summarize_content(transcript)
        if not summary:
            return {"error": "Failed to generate summary"}
        
        # Calculate total time
        self.timing_stats['total_time'] = time.time() - overall_start_time
        
        return {
            'summary': summary,
            'timing_stats': self.timing_stats,
            'transcript_length': len(transcript.split()),
            'summary_length': len(summary.split())
        }

    def print_timing_report(self):
        """Print a detailed timing report."""
        print("\n=== Performance Report ===")
        print(f"Total Processing Time: {self.timing_stats['total_time']:.2f} seconds")
        print("\nBreakdown:")
        print(f"├── URL Processing: {self.timing_stats.get('url_processing_time', 0):.2f}s")
        print(f"├── Transcript Fetch: {self.timing_stats.get('transcript_fetch_time', 0):.2f}s")
        print(f"├── Text Chunking: {self.timing_stats.get('chunking_time', 0):.2f}s")
        print(f"└── Summarization: {self.timing_stats.get('summarization_time', 0):.2f}s")
        print("\nModel Loading Time (first run only):", f"{self.timing_stats.get('model_load_time', 0):.2f}s")

# Example usage
if __name__ == "__main__":
    # Initialize the summarizer once
    start_time = time.time()
    summarizer = VideoSummarizer()
    
    # You can now use it multiple times without redownloading the model
    url = "https://www.youtube.com/watch?v=0JUN9aDxVmI&ab_channel=HarvardUniversity"
    
    print("\nProcessing video...")
    result = summarizer.get_video_summary(url)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("\nContent Summary:")
        print(result['summary'])
        print(f"\nTranscript length: {result['transcript_length']} words")
        print(f"Summary length: {result['summary_length']} words")
        summarizer.print_timing_report()
import json
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from src.common.output_file_manager import provide_file_path

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return transcript

def save_transcript_to_json(video_id):
    transcript = get_transcript(video_id)
    file_path = provide_file_path(f"{video_id}_transcript", ".json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(transcript, f, ensure_ascii=False, indent=4)
    print(f"Transcript saved to {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and save YouTube video transcript.")
    parser.add_argument("--video_id", "-v", required=True, help="The ID of the YouTube video")
    args = parser.parse_args()
    
    save_transcript_to_json(args.video_id)
    
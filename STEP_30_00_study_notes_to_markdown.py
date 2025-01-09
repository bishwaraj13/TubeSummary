import json
from datetime import timedelta
import argparse
from src.common.output_file_manager import provide_file_path, get_latest_file

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS or MM:SS format"""
    # Convert to integer to avoid float formatting issues
    seconds = int(seconds)
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}"
    else:
        return f"{int(minutes):02d}:{int(secs):02d}"

def json_to_markdown(json_data, video_id):
    """Convert lecture JSON to markdown format"""
    # Start with the overview
    markdown = f"# {json_data['title']}\n\n## Overview\n\n{json_data['overview']}\n\n"
    citation = 1
    
    # Process each topic
    for topic in json_data['topics']:
        link = f"https://www.youtube.com/watch?v={video_id}&t={int(topic['time_start'])}s"

        markdown += f"## {topic['title']} [[{citation}]]({link})\n\n"
        citation += 1
        
        # Process description items
        for desc_item in topic['description']:
            if desc_item['type'] == 'text':
                markdown += f"{desc_item['content']}\n\n"
            
            elif desc_item['type'] == 'snapshot':
                snapshot_time_in_seconds = float(desc_item['content'])
                snapshot_time = format_timestamp(snapshot_time_in_seconds)
                link = f"https://www.youtube.com/watch?v={video_id}&t={int(snapshot_time_in_seconds)}s"
                markdown += f"📸 [*Snapshot from {snapshot_time}*]({link})\n\n"
            
            elif desc_item['type'] == 'example':
                markdown += f"**Example:**\n> {desc_item['content']}\n\n"
            
            elif desc_item['type'] == 'summary_point':
                markdown += f"💡 **Key Point:** {desc_item['content']}\n\n"
    
    return markdown.strip()

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create study notes in markdown")
    parser.add_argument("--video_id", "-v", required=True, help="The ID of the YouTube video")
    args = parser.parse_args()

    notes_json_file = get_latest_file('./output/STEP_20_00_create_study_notes_json', extension=".json")
    notes_json = json.load(open(notes_json_file))

    markdown_output = json_to_markdown(notes_json, args.video_id)
    
    # get markdown file path
    notes_title = notes_json['title']
    markdown_file_path = provide_file_path(notes_title.lower().replace(" ", "_"), ".md", media=False)

    # Write to file
    with open(markdown_file_path, 'w') as file:
        file.write(markdown_output)
        
    print(f"Markdown file saved at: {markdown_file_path}")


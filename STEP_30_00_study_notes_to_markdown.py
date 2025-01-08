import json
from datetime import timedelta
import markdown2
import pdfkit

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    return str(timedelta(seconds=seconds))

def json_to_markdown(json_data):
    """Convert lecture JSON to markdown format"""
    # Start with the overview
    markdown = f"# Lecture Notes\n\n## Overview\n\n{json_data['overview']}\n\n"
    
    # Process each topic
    for topic in json_data['topics']:
        # Add topic header with timestamps
        start_time = format_timestamp(topic['time_start'])
        end_time = format_timestamp(topic['time_end'])
        markdown += f"## {topic['title']} ({start_time} - {end_time})\n\n"
        
        # Process description items
        for desc_item in topic['description']:
            if desc_item['type'] == 'text':
                markdown += f"{desc_item['content']}\n\n"
            
            # elif desc_item['type'] == 'snapshot':
            #     snapshot_time = format_timestamp(float(desc_item['content']))
            #     markdown += f"📸 *Snapshot at {snapshot_time}*\n\n"
            
            elif desc_item['type'] == 'example':
                markdown += f"**Example:**\n> {desc_item['content']}\n\n"
            
            elif desc_item['type'] == 'summary_point':
                markdown += f"💡 **Key Point:** {desc_item['content']}\n\n"
    
    return markdown.strip()

def save_markdown_as_pdf(markdown_content, output_pdf_path):
    html_content = markdown2.markdown(markdown_content)
    pdfkit.from_string(html_content, output_pdf_path)

# Example usage
if __name__ == "__main__":
    # For reading from a file
    with open('./output/STEP_20_00_context_cache_transcripts/study_notes_2025-01-08_18-22-49.json') as f:
        notes_json = json.load(f)
    
    # Using sample data
    markdown_output = json_to_markdown(notes_json)
    
    # Write to file
    with open('lecture_notes.md', 'w') as file:
        file.write(markdown_output)
        
    print("Markdown file has been created successfully!")


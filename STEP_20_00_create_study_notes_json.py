import vertexai
import datetime
import os
import json

from vertexai.preview import caching
from vertexai.preview.generative_models import GenerativeModel

from src.prompt_library.topic_lister import topic_lister_prompt, topic_lister_generation_config
from src.prompt_library.topic_detailing import topic_detailing_prompt, topic_detailing_generation_config
from src.prompt_library.config import SAFETY_CONFIG
from src.common.output_file_manager import provide_file_path, get_latest_file
from dotenv import load_dotenv

def create_context_cache(transcript):
    system_instruction = '''
    You are an expert educational content creator specializing in creating comprehensive study notes.
    You are provided with a video transcript of a lecture on YouTube.
    '''
    model_name = os.getenv("MODEL_NAME")
    contents = f"Transcript: {transcript}"

    cached_content = caching.CachedContent.create(
        model_name=model_name,
        system_instruction=system_instruction,
        contents=contents,
        ttl=datetime.timedelta(minutes=60),
        display_name="transcript-cache",
    )

    print(cached_content)
    print(f"Context cache created with ID: {cached_content.name}")
    return cached_content.name

def create_segments(cache_id):
    vertexai.init()
    cached_content = caching.CachedContent(cached_content_name=cache_id)

    model = GenerativeModel.from_cached_content(cached_content=cached_content)

    response = model.generate_content(topic_lister_prompt, 
                                      generation_config=topic_lister_generation_config,
                                      safety_settings=SAFETY_CONFIG)
    
    print(f"Created segments: {response.text}")
    json_response = json.loads(response.text)

    return json_response

def describe_segment(cache_id, segment):
    vertexai.init()
    cached_content = caching.CachedContent(cached_content_name=cache_id)
    model = GenerativeModel.from_cached_content(cached_content=cached_content)

    response = model.generate_content(
                                    f"{topic_detailing_prompt}\n\nThe topic is: {segment}",
                                    generation_config=topic_detailing_generation_config,
                                    safety_settings=SAFETY_CONFIG
                                    )
    
    print(f"Described segment: {response.text}")
    json_response = json.loads(response.text)

    return json_response

def main():
    load_dotenv()
    transcript_file = get_latest_file('output/STEP_10_00_download_transcripts', extension=".json")

    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript = json.load(f)

    print("Creating context cache for transcripts...")
    cache_id = create_context_cache(transcript)

    print("Creating segments...")
    segments = create_segments(cache_id)

    for segment in segments['topics']:
        print(f"Describing segment: {segment['title']}")
        segment_description = describe_segment(cache_id, segment['title'])
        segment['description'] = segment_description['content']

    file_path = provide_file_path("study_notes", ".json", media=False)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(segments, f, ensure_ascii=False, indent=4)
    print(f"Study notes saved to {file_path}")

if __name__=="__main__":
    main()
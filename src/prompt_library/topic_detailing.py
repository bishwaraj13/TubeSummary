from vertexai.generative_models import GenerationConfig

topic_detailing_prompt = '''
Your task is to analyze the following topic segment from a video lecture and create detailed notes with strategic placement of video snapshots.

Generate detailed notes that:
1. Break down complex concepts
2. Include relevant examples
3. Highlight key points
4. Indicate where visual aids from the video would be most beneficial

Please analyze the following topic segment and return the results in this exact JSON format:

{
    "topic_title": "The main topic title",
    "content": [
        {
            "type": "text",
            "content": "Detailed explanation or point",
        },
        {
            "type": "snapshot",
            "content": seconds,
        },
        {
            "type": "example",
            "content": "Practical example or illustration of the concept"
        },
        {
            "type": "summary_point",
            "content": "Important summary or takeaway"
        }
    ],
    "key_terms": [
        {
            "term": "Technical term or concept",
            "definition": "Clear explanation of the term"
        }
    ]
}

Note: 
- Inside the "content" list, you can include multiple text, snapshot, example, and summary_point items as needed.
- Use the "snapshot" type to indicate where a video snapshot should be included. In case of a snapshot, the "content" field should contain the timestamp in seconds in double quotes.
'''

schema = {
    "type": "object",
    "properties": {
        "topic_title": {
            "type": "string",
            "description": "The main topic title"
        },
        "content": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "Type of content (text, snapshot, example, summary_point)"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content of the section"
                    }
                }
            }
        },
        "key_terms": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "Technical term or concept"
                    },
                    "definition": {
                        "type": "string",
                        "description": "Clear explanation of the term"
                    }
                }
            }
        }
    }
}

topic_detailing_generation_config = GenerationConfig(
    # The MIME type of the response (e.g. "application/json" or "text/plain"
    response_mime_type="application/json",
    # The temperature of the model, which controls randomness (0.0 to 1.0)
    temperature=1,
    top_p=0.95,
    top_k=1,
    # The maximum number of tokens to generate in the response (1 to 8192)
    max_output_tokens=8192,
    response_schema=schema
)

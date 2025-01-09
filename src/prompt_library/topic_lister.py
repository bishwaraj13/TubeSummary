from vertexai.generative_models import GenerationConfig

topic_lister_prompt = '''
Your task is to analyze the following video lecture transcript and:

1. Add a title to the entire lecture
1. Create a high-level overview of the entire lecture
2. Identify distinct main topics/segments
3. Determine the timestamp boundaries for each segment
4. Return the information in a structured JSON format

Important Instructions:
- Identify natural breaking points where new topics or concepts are introduced
- Create clear, concise titles for each segment that reflect the main concept discussed
- Use timestamps or word positions to mark the beginning and end of each segment
- Ensure topics are meaningful units of content
- Maintain hierarchical organization of topics

Please analyze the following transcript and return the results in this exact JSON format:

{{
    "title": "Clear and descriptive lecture title",
    "overview": "A concise 2-3 sentence summary of the entire lecture",
    "topics": [
        {{
            "title": "Clear and descriptive topic title",
            "time_start": start_time_in_seconds,
            "time_end": end_time_in_seconds
        }}
    ]
}}
'''

schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "A clear and descriptive lecture title"
        },
        "overview": {
            "type": "string",
            "description": "A concise 2-3 sentence summary of the entire lecture"
        },
        "topics": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Clear and descriptive topic title"
                    },
                    "time_start": {
                        "type": "number",
                        "format": "float",
                        "description": "Start time of the topic in seconds"
                    },
                    "time_end": {
                        "type": "number",
                        "format": "float",
                        "description": "End time of the topic in seconds"
                    }
                }
            }
        }
    }
}

topic_lister_generation_config = GenerationConfig(
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

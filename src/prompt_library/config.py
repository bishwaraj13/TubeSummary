from vertexai.preview import generative_models

SAFETY_CONFIG = [
    generative_models.SafetySetting(
        category=generative_models.HarmCategory.HARM_CATEGORY_UNSPECIFIED,
        threshold=generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    generative_models.SafetySetting(
        category=generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    generative_models.SafetySetting(
        category=generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    generative_models.SafetySetting(
        category=generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    generative_models.SafetySetting(
        category=generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
]

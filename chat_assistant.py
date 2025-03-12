import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def get_chat_response(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant specializing in clarifying "
                              "and expanding upon sign language translations. Help explain "
                              "and provide context for translated sign language messages."
                },
                {"role": "user", "content": f"Please help explain this sign language "
 f"translation in more detail: {message}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Failed to get chat response: {str(e)}") 
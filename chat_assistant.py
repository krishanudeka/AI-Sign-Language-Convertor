import os
from deepseek_ai import DeepSeek # type: ignore

# DeepSeek API Key - Ensure this environment variable is set!
DEEPSEEK_API_KEY = "sk-7a896fc9b26642f59b5a0c6014981f3c"  # Hardcoding is NOT recommended for production

# Initialize DeepSeek client
deepseek = DeepSeek(api_key=DEEPSEEK_API_KEY)

def get_deepseek_response(message):
    """
    Generates a response from the DeepSeek chat model.

    Args:
        message: The user's message (sign language translation) to explain.

    Returns:
        The DeepSeek chat model's response, or None if an error occurred.
    """
    try:
        response = deepseek.chat.completions.create(
            model="deepseek-chat",  # Or replace with a different DeepSeek model
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
        print(f"Error with DeepSeek: {e}")  # Print the error for debugging
        return None  # Return None to indicate failure

def main():
    """
    Main function to get user input and generate a DeepSeek response.
    """
    user_message = input("Enter sign language translation: ")  # Get input from the user

    # Using DeepSeek Chat
    deepseek_response = get_deepseek_response(user_message)

    if deepseek_response:  # Check if a response was successfully generated
        print(f"DeepSeek Response: {deepseek_response}")
    else:
        print("Failed to get a response from DeepSeek.")

if __name__ == "__main__":
    main()

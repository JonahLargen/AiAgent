import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import argparse

SYSTEM_PROMPT = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

parser = argparse.ArgumentParser(description="Ask your AI Agent.")
parser.add_argument("prompt", type=str, help="The prompt to send to the AI Agent.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)
user_prompt = args.prompt
verbose = args.verbose
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
)
if verbose:
    print(f"User prompt: {user_prompt}")
print(response.text)
if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

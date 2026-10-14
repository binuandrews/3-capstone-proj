import os
import json
import google as genai
from openai import OpenAI
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

with open("config.json", 'r') as f:
  CONFIG = json.load(f)

'''Function to run chat with OpenAI API'''
def run_openai(user_message: str) -> str:
  api_key = os.getenv("OPEN_AI_API_KEY")
  if not api_key:
    raise ValueError("OPEN_AI_API_KEY environment variable not set")
  client = OpenAI(api_key = api_key)
  response = client.chat.completions.create(
      model = CONFIG["openai"]["model"],
      messages = user_message,
      max_tokens = CONFIG["openai"].get(["max_tokens"], 200),
      temperature = CONFIG["openai"].get(["temperature"], 0.7),
      top_p = CONFIG["openai"].get(["top_p"], 0.9)
  )
  return response.choices[0].message.content.strip()


'''Function to run chat with Gemini API'''
def run_gemini(user_message: str) -> str:
  api_key = os.getenv("GEMINI_API_KEY")
  if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

  client = genai.Client(api_key=api_key)
  response = client.models.generate_content(
      model=CONFIG["gemini"]["model"],
      contents=user_message,
      generation_config={
        "temperature": CONFIG["gemini"].get("temperature", 0.7),
        "top_p": CONFIG["gemini"].get("top_p", 0.9),
        "max_output_tokens": CONFIG["gemini"].get("max_output_tokens", 200)
      }
  )
  return response.text.strip()

'''Router function to select the appropriate LLM provider based on the configuration'''
def run_llm(history):
  provider = CONFIG["provider"]
  if provider == "openai":
    return run_openai(history)
  elif provider == "gemini":
    conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    return run_gemini(conversation_text)
  else:
    raise ValueError(f"Unsupported provider: {provider}")
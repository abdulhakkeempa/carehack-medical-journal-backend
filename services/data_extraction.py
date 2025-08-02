from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

endpoint = "https://eastus.api.cognitive.microsoft.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"

subscription_key = os.getenv("AZURE_API_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


def extract_health_data(input_date, journal_entry):
  prompt = f"""
  Your task is to analyze a user's daily medical journal entry and return a JSON object with the following structure:

  {{
    "date": "<date in YYYY-MM-DD format>",
    "condition": "<short summary of the main health-related issue or observation>",
    "type": "<one of: 'physical', 'emotional', 'mental', 'medication', 'general'>",
    "remarks": "<optional insights, suggestions, or follow-up notes if available>"
  }}

  Guidelines:
  - The "condition" should concisely summarize the journal content.
  - The "type" should reflect the nature of the journal entry:
    - Use 'emotional' for feelings, moods, stress, etc.
    - Use 'physical' for pain, symptoms, fatigue, etc.
    - Use 'mental' for cognitive issues, confusion, clarity, etc.
    - Use 'medication' for notes on medicine intake or side effects.
    - Use 'general' for anything that doesn't fit the above.
  - The "remarks" field can include advice, next steps, or personal notes if they exist in the journal entry.
  - If the journal refers to a specific date (e.g., “Yesterday”, “Last night”, or mentions an explicit date), extract and normalize it to YYYY-MM-DD format and use that as the "date" value.
  - Otherwise, use the current date provided in the input (under the `today` key) as the default "date".

  Now, analyze the following input and return the structured JSON:

  Input:
  {{
    "today": "{input_date}",
    "journal": "{journal_entry}"
  }}
  """

  response = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": "You are an expert in structuring unstructured health journal entries into clean JSON format with relevant metadata.",
          },
          {
              "role": "user",
              "content": prompt,
          }
      ],
      max_tokens=4096,
      temperature=1.0,
      top_p=1.0,
      model=deployment
  )

  print(response.choices[0].message.content)

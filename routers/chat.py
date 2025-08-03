from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import asyncio
from models.tables import health_records
from db import database


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

router = APIRouter()

prompt = """
You are a highly experienced psychologist specializing in Cognitive Behavioral Therapy (CBT), especially the CBT Triangle (Thoughts – Emotions – Behaviors). Your role is to help users gently explore whether their physical or emotional pain stems from:

1. An emotional or behavioral trigger (CBT-relevant), or 
2. A possible physical/medical issue (CBT-irrelevant)


## Core Instructions:
- Ask short, clear, calming questions (max 8 words).
- Use warm, empathetic tone throughout.
- Expect vague or defensive answers. Be patient. Reframe gently if needed, but never pressure the user.
- Never repeat the same question.
- Proceed based on the user's response clarity:

## If answers are clear or specific:
- Explore gently using the CBT triangle:
- What were you thinking then?
- How did it make you feel?
- What did you do afterward?
- Help the user reflect and recognize a potential emotional trigger or behavioral pattern.
- Do not discuss physical causes unless pain clearly points to them.

## If the issue appears physical or medical:
- Do not continue CBT questioning.
- Acknowledge their concern and gently suggest medical evaluation.
- Do not bring emotional causes into discussion further.

## If the user is unable or unwilling to open up:
- Do not push or continue with questioning.
- Offer a general calming suggestion or self-care tip (e.g., rest, hydration, breathing exercise).
- Wind up the session gently and supportively.
- In future conversations, if the user seems more open, revisit gently:
--- Would you feel okay sharing more today?
--- Can we go back to how you felt then?

## End Goal:
By the end of the conversation, either:
- Guide the user to a possible emotional trigger using the CBT triangle,
OR
- Help them consider medical consultation, if more appropriate,
OR
- Offer general relief and close supportively if they aren't ready to engage.

Maintain emotional safety and trust above all else.
"""


async def fetch_user_timeline_summaries():
    """
    Fetches the user's health records and summarizes them into a timeline.
    """
    user_id = 1

    query = health_records.select().where(health_records.c.user_id == user_id)
    records = await database.fetch_all(query)

    timeline = "\n".join([
        f"{r['date']}: {r['condition']} ({r['type']})" + (f" - {r['remarks']}" if r['remarks'] else "")
        for r in records
    ])

    summary_prompt = f"Summarize the following medical journal entries for a user as a timeline, highlighting key events and trends.\n\n{timeline}"
    summary_response = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are a medical journal summarizer."}, {"role": "user", "content": summary_prompt}],
        max_tokens=512,
        temperature=0.7,
        model=deployment
    )
    timeline_summary = summary_response.choices[0].message.content

    return timeline_summary.strip()


timeline_summary = """
Timeline Summary: ### Timeline Summary of Medical Journal Entries

**2025-08-01**
- **Key Event:** High temperature reported (physical).
- **Trend:** Possible onset of illness or fever-related condition.

**2025-08-02**
- **Key Events:**
  - Feeling cold and experiencing headache (physical).
  - Several entries lack health-related information or are incomplete, with one noting gratitude.
- **Trend:** Symptoms (cold and headache) may indicate progression of illness. Lack of detailed observations makes it harder to track health patterns effectively.

**2025-08-03**
- **Key Event:** Feeling lonely (emotional).
- **Trend:** Emergence of emotional distress, possibly linked to earlier physical symptoms or a separate issue.

### Key Observations:
- Physical health issues (fever, cold, headache) arose on 2025-08-01 and 2025-08-02, potentially indicating a short-term illness.
- Emotional health concern (loneliness) noted on 2025-08-03, suggesting a shift in focus from physical to emotional well-being.
- Gaps in detailed journaling may hinder comprehensive health tracking.

### Recommendations:
- Consistently record both physical and emotional health observations for better trend analysis.
- Explore connections between physical symptoms and emotional states.
"""


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    # timeline_summary = await fetch_user_timeline_summaries()
    # print("Timeline Summary:", timeline_summary)
    system_context = prompt + f"\n\nUser's medical timeline summary:\n{timeline_summary}"
    messages = [{"role": "system", "content": system_context}]
    try:
        while True:
            response = client.chat.completions.create(
                messages=messages,
                max_tokens=4096,
                temperature=1.0,
                top_p=1.0,
                model=deployment
            )

            llm_reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": llm_reply})
            await websocket.send_text(llm_reply)

            data = await websocket.receive_text()
            messages.append({"role": "user", "content": data})
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        

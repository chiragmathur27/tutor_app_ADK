from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid
from typing import List, Tuple

import os
from dotenv import load_dotenv

from tutor_agent import root_agent
from google.adk.runners import Runner, RunConfig
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()
PORT = int(os.environ.get("PORT",8000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tutor-app-adk-fe.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
)
session_service = InMemorySessionService()

runner = Runner(
    app_name="Tutor_App",
    agent=root_agent,
    session_service=session_service
)

class MessageRequest(BaseModel):
    content: str
    user_id: str = "Chirag Mathur"
    session_id: str = None

class AgentResponse(BaseModel):
    full_response: str
    session_id: str
    events: List[dict] = []

async def process_message(
    content: str,
    user_id: str = "Chirag Mathur",
    session_id: str = None,
    run_config: RunConfig = None
) -> Tuple[str, str, List[dict]]:
    """
    Method to call the runner's run_async method and collect events,
    extracting the full agent response.
    """
    if session_id is None:
        session_id = str(uuid.uuid4())
        if not session_service.get_session(app_name="Tutor_App", user_id=user_id, session_id=session_id):
            session_service.create_session(
                app_name="Tutor_App",
                user_id=user_id,
                session_id=session_id
            )

    new_message = types.Content(role="user",parts=[types.Part(text=content)])


    if run_config is None:
        run_config = RunConfig()

    collected_events = []
    agent_full_response = ""

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message,
            run_config=run_config
        ):
            event_dict = {
                "type": getattr(event, 'type', 'unknown'),
                "partial": getattr(event, 'partial', False),
                "event_class": event.__class__.__name__
            }

            if hasattr(event, 'content') and event.content:
                event_dict["content_present"] = True
                if hasattr(event.content, 'parts') and event.content.parts:
                    event_dict["content_parts_count"] = len(event.content.parts)
                    for i, part in enumerate(event.content.parts):
                        if hasattr(part, 'text') and part.text:
                            event_dict[f"part_{i}_text"] = part.text
                            agent_full_response += part.text # Accumulate the text
                        elif hasattr(part, 'function_call') and part.function_call:
                            event_dict[f"part_{i}_function_call"] = {
                                "name": part.function_call.name,
                                "args": part.function_call.args
                            }
                        elif hasattr(part, 'function_response') and part.function_response:
                            event_dict[f"part_{i}_function_response"] = {
                                "name": part.function_response.name,
                                "response": part.function_response.response
                            }
                else:
                    event_dict["content_parts_empty"] = True
            else:
                event_dict["content_present"] = False

            # Also check for direct 'text' attribute if it's not nested in content
            if hasattr(event, 'text') and event.text:
                 event_dict["direct_event_text"] = event.text

            collected_events.append(event_dict)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

    return agent_full_response, session_id, collected_events

@app.post("/chat", response_model=AgentResponse)
async def chat_endpoint(request: MessageRequest):
    """
    FastAPI endpoint to handle chat requests, returning the agent's full response
    and the session ID used.
    """
    full_response, used_session_id, events = await process_message(
        content=request.content,
        user_id=request.user_id,
        session_id=request.session_id
    )

    return AgentResponse(full_response=full_response, session_id=used_session_id, events=events)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
import os

from utility import convert_speech_to_text, load_model, convert_text_to_speech
from delivery import main
from templates import orchestrator_template
from support import get_response

from crewai import Agent
from crewai.flow import Flow, start,listen, router

from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException,Form, File, UploadFile
from fastapi.responses import FileResponse
from typing import Optional

app = FastAPI()

UPLOAD_DIR = "recordings"
os.makedirs(UPLOAD_DIR, exist_ok=True)

llm = load_model()

class RouterState(BaseModel):
    router_flag: bool = False
    query: str = ""

class AppFlow(Flow[RouterState]):

    @start()
    def classify(self):
        agent = Agent(role = "Intent classifier",
                      name = "orchestrator",
                      goal =orchestrator_template,
                      backstory = "You work at a customer care for a logistics company and need to understand user's intent so the query can be transfered to the right agent",
                      memory=True,
                        llm=llm,
                        reasoning=True

        )
        result = agent.kickoff(self.state.query)
        print(f"==============intent: {result.raw}============")
        if result.raw.lower() == "delivery-agent":
            self.state.router_flag="delivery-agent"
        else:
            self.state.router_flag="support-agent"
        # return result

    @router(classify)
    def router_method(self):
        if self.state.router_flag=="delivery-agent":
            return "delivery-agent"
        else:
            return "support-agent"
        
    @listen("delivery-agent")
    def delivery_agent(self):
        order_id = main()
        convert_text_to_speech(f"Thank you! your order with order id {order_id} has been placed.","order_placed")
        return "order_placed"

    @listen("support-agent")
    def support_agent(self):
        response = get_response(self.query)
        convert_text_to_speech(f"{response}", "response")
        return "response"

@app.post("/query")
def start(text: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None)):
    query = None

    if text:
        query = text

    elif audio:
        try:
            filename = audio.filename
            file_path = os.path.join('..', 'input_recordings',filename)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        query = convert_speech_to_text(file_path)
        print(f"========{query}========")
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, details="No query passed")

    initial_state = RouterState(query=query)

    # Pass it to the flow
    flow = AppFlow(state=initial_state)
    result = flow.kickoff()
    result = "order_placed"

    response_file_path = os.path.join('..', 'recordings', result + '.wav')
    return FileResponse(response_file_path, media_type='audio/wav', filename=result+".wav")


@app.get("test_api")
def test_api():
    return "API is working"

from utility import convert_speech_to_text, load_model, convert_text_to_speech
from delivery import main
from crewai import Agent
from crewai.flow import Flow, start,listen, router
from templates import orchestrator_template
from pydantic import BaseModel
from support import get_response

llm = load_model()

class RouterState(BaseModel):
    router_flag: bool = False
    query: str = ""

class AppFlow(Flow[RouterState]):
    
    @start()
    def get_query(self)->str:
        # query = input("Enter your query")
        # query = convert_speech_to_text(r"C:\Users\Anoopkumarjain\Documents\git_reps\GenAI\documents\recordings\query_delivery.wav")
        query = convert_speech_to_text(r"C:\Users\Anoopkumarjain\Documents\git_reps\GenAI\documents\recordings\query_support.wav")
        print(f"============query:{query}==========")
        self.query=query
        # return query

    @listen(get_query)
    def classify(self):
        agent = Agent(role = "Intent classifier",
                      name = "orchestrator",
                      goal =orchestrator_template,
                      backstory = "You work at a customer care for a logistics company and need to understand user's intent so the query can be transfered to the right agent",
                      memory=True,
                        llm=llm,
                        reasoning=True

        )
        result = agent.kickoff(self.query)
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

    @listen("support-agent")
    def support_agent(self):
        response = get_response(self.query)
        convert_text_to_speech(f"{response}", "response")
        
flow = AppFlow()
result = flow.kickoff()

print(f"Generated fun fact: {result}")

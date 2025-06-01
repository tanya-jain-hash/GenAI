import os
from crewai import LLM, Agent
from crewai.tools import tool
from crewai.flow.flow import Flow, listen, start

from ollama import chat
from ollama import ChatResponse
import asyncio



llm = LLM(
    model="ollama/tinyllama:1.1b",
    base_url="http://localhost:11434"
)


class ExampleFlow(Flow):
    # model = llm
    
    @start()
    def get_query(self)->str:
        query = input("Enter your query")
        return query

    @listen(get_query)
    def get_response(self, get_query):
        agent = Agent(role = "Intent classifier",
                      name = "orchestrator",
                      goal ="""
                            Task: Identify the intent of the user query and classify it into one of the following:
                            - DELIVERY-AGENT
                            - SUPPORT AGENT
                            - FAQ AGENT

                            Refer to the following example scenarios to understand how to classify the user query.
                            Example:
                            DELIVERY-AGENT for following scenarios
                            1. query: "I want to send a package from new york to new delhi. Can you help me book it?"
                            Answer: DELIVERY-AGENT
                            2. query: "book a package delivery to san francisco"
                            Answer: DELIVERY-AGENT
                            3. query : "book a pickup for HnM dress"
                            Answer: DELIVERY-AGENT
                            4. query: "schedule a delivery to new york"
                            Answer: DELIVERY-AGENT

                            keywords: "book","delivery","pickup" etc.

                            SUPPORT-AGENT for following scenarios
                            1. query: "My package was supposed to arrive yesterday. Where is it?"
                            Answer : SUPPORT-AGENT
                            2. query: "I missed the delivery. Can you reschedule it for tomorrow morning?"
                            Answer: SUPPORT-AGENT
                            3. query: "I received a damaged item. How do I raise a complaint?"
                            Asnwer: SUPPORT-AGENT
                            4. query: "The delivery agent was rude. How can I report this?"
                            Answer: SUPPORT-AGENT
                            keywords:  "where","miss","complaint","damage","report","raise" etc.


                            FAQ-AGENT for following scenarios
                            1. query: "What’s your policy on missed deliveries?"
                            Answer: FAQ-AGENT
                            2. query: "How do I track my shipment?"
                            Answer: FAQ-AGENT
                            3. query: "Are there any extra charges for COD orders?"
                            Answer: FAQ-AGENT
                            4. query: "Do you deliver on Sundays and public holidays?"
                            Answer: FAQ-AGENT
                            keyowrds: "policy", "how" etc.

                            Do not answer user query. Only return the agent name [ one of DELIVERY-AGENT, SUPPORT AGENT, FAQ AGENT] for the present query only.

                            Answer: 
                            """,
                      backstory = "You work at a customer care for a logistics company and need to understand user's intent so the query can be transfered to the right agent",
                      memory=True,
                        llm=llm,
                        reasoning=True

        )
        result = agent.kickoff(get_query)
        return result


flow = ExampleFlow()
# flow.plot()
result = flow.kickoff_async()

print(f"Generated fun fact: {result}")

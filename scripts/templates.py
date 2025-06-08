orchestrator_template = """
                            Task: Identify the intent of the user query and classify it into one of the following:
                            - DELIVERY-AGENT
                            - SUPPORT AGENT

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

                            delivery-agent is used to book package deliveries.
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

                            support-agent is used to answer the question relating to the package
                            keywords:  "where","miss","complaint","damage","report","raise" etc.


                            Do not answer user query. Only return the agent name [ one of DELIVERY-AGENT, SUPPORT AGENT] for the present query only.

                            Answer: 
                            """

schema = """
   "shipment" 
   "id" int , 
   "customer_name" text , 
   "customer_mobile_no" int , 
   "shipment_origin" text , 
   "shipment_destination" text , 
   "shipment_amount" int , 
   "payment_status" text,
   "payment_mode" text
   "order_id" text
   primary key: "id"
"""				
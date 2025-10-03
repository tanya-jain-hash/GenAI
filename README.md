# GenAI Logistics VoiceBot
The GenAI Logistics Voice Agent simulates a real-world logistics customer service call using voice-first AI models. Unlike a traditional chatbot, it is designed as a sequential voice interaction system that replicates how a live agent would engage with a customer.

A call begins with a synthesized agent greeting (via TTS), followed by the customer’s spoken response. This response is transcribed, analyzed for intent, and routed to the correct support agent. In addition, natural language queries can be converted to SQL to fetch relevant logistics data from a database.

## Key Features (Open-Source resources)
1. Voice Interaction
- SUMO Bark (TTS): Generates natural agent voices for greetings and responses.
- Whisper (STT): Transcribes user responses into text.
2. Intent Understanding & Routing
- LLaMA 3.3 (via Ollama): Provides fast inference for intent detection and conversation flow.
- CrewAI: Powers multi-agent orchestration for agent handover and workflow simulation.
3. Natural Language to SQL
- gaussalgo/T5-LM-Large-text2sql-spider: Converts natural queries into executable SQL statements.
- SQLite (logistics_dummy.db): Stores shipment/customer data for query resolution.
4. Deployment
- FastAPI backend to expose APIs for voice processing, intent classification, and agent routing.

## Tech Stack
1. Languages: Python
2. Core Models:
- Whisper (Speech-to-Text)
- SUMO Bark (Text-to-Speech)
- LLaMA 3.3 (Ollama runtime for low-latency inference)
- gaussalgo/T5-LM-Large-text2sql-spider (NL → SQL)
4. Frameworks:
- CrewAI (agentic framework)
- FastAPI (deployment)
5. Database: SQLite (logistics_dummy.db)

## Future Scope
- Latency Reduction: Optimize inference for real-time call handling
- Improved SQL Query Generation: Enhance natural language → SQL accuracy and handle complex queries
- More Specialized Agents: Expand intent classes and agent coverage (customs, insurance, payments, etc.)
- Tool Integrations: Connect to ticketing systems (e.g., ServiceNow, Jira, Freshdesk) to auto-raise tickets when issues cannot be resolved automatically
- Scalability: Deploy on cloud telephony systems (Twilio, Asterisk) for production-grade simulation

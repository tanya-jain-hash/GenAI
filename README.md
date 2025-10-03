# GenAI Logistics VoiceBot
The GenAI Logistics Voice Agent simulates a real-world customer service call in the logistics domain. Instead of a text chatbot, it recreates the workflow of a voice-based agent, handling both speech generation and speech recognition in a sequential pipeline.

## Key Features
- Voice Simulation: Uses SUMO Bark (TTS) to generate natural-sounding agent voices.
- Speech Recognition: Integrates OpenAI Whisper (STT) to transcribe user responses.
- Intent Understanding: User text is analyzed to classify the request (e.g., shipment status, payment, delivery delays).
- Agent Routing: Queries are connected to the most relevant logistics support agent.
- Agentic Framework: Powered by AutoGen to manage multi-agent workflows and simulate real-world interaction dynamics.
- Dummy Logistics Data: Includes logistics_dummy.db to simulate customer and shipment records.

## Tools & Technologies
- Programming Language: Python
- TTS: Bark (SUMO fork)
- STT: OpenAI Whisper
- Agent Framework: AutoGen
- Database: SQLite (logistics_dummy.db) for simulated logistics queries
- 

🤖 AI Project Assistant

An advanced multi-agent AI assistant system that combines retrieval, memory, graph reasoning, and tool integration to deliver accurate, personalized, and efficient responses.

🚀 Overview

This project goes beyond a simple chatbot by implementing a production-style AI architecture. It uses a Main Agent to orchestrate multiple components such as worker agents, vector search, graph database, caching, and external tools.

👉 The goal:
Build an AI system that is accurate (no hallucination), personalized, and scalable.

🧠 Architecture
User
→ Long-Term Memory (personalization)
→ Semantic Cache (Redis)
→ Hybrid Retrieval (BM25 + Vector DB)
→ Graph DB (Neo4j relationships)
→ Main Agent (decision engine)
→ Worker Agents (specialists)
→ MCP Tools (external integrations)
→ Final Answer

⚙️ Key Features
🔹 Multi-Agent System
Main Agent → decides what to do
Concept Agent → explains concepts simply
Project Agent → explains system-specific details

🔹 Retrieval-Augmented Generation (RAG)
Always retrieves data before answering
Prevents hallucination
Uses:
Qdrant (Vector DB) → semantic search
BM25 → keyword search

👉 Hybrid retrieval = better accuracy

🔹 Graph Database (Neo4j)
Models relationships between system components
Enables queries like:
"How is Redis connected to this project?"
🔹 Long-Term Memory
Stores user preferences
Personalizes responses

Example:

"I prefer simple explanations"
→ saved → used in future answers
🔹 Semantic Cache (Redis)
Reuses answers for similar questions
Reduces API cost and latency
🔹 Metadata-Based Cache Policy
Controls what gets cached
Prevents caching sensitive or dynamic responses
🔹 MCP (Model Context Protocol)
Connects AI agents to external tools
Standardized tool execution layer
🔹 Streamlit UI

Interactive chat interface
Shows:
Responses
Tools used
Cache status
Debug info

🛠️ Tech Stack
Category Technology
AI / Agents OpenAI Agents SDK
LLM OpenAI GPT-4.1
Vector DB Qdrant
Keyword Search BM25 (rank-bm25)
Graph DB Neo4j
Cache Redis + RedisVL
Memory JSON-based storage
UI Streamlit
Embeddings sentence-transformers
Tool Protocol MCP

🧪 Example Capabilities
Concept Explanation
"What is a vector database?"
→ Concept Agent → simple explanation
Project Understanding
"What is this project?"
→ Retrieval + Project Agent
Relationship Query
"How is Redis connected?"
→ Graph DB (Neo4j)
Personalization
"I prefer simple explanations"
→ Stored in memory → affects future answers
Smart Caching
"Explain vector DB"
→ Cached
"Explain vector database simply"
→ Cache HIT (semantic)
🧑‍💻 Installation
git clone https://github.com/your-username/ai-project.git
cd ai-project
pip install -r requirements.txt
🔐 Environment Variables

Create .env:

OPENAI_API_KEY=your_key
REDIS_URL=redis://localhost:6379/0
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

▶️ Run the App
Terminal Mode
python -m app.main
UI Mode
streamlit run ui.py

📌 Project Structure
app/
├── main.py
├── agent_runner.py
├── workers.py
├── retrieval.py
├── hybrid_retrieval.py
├── bm25_search.py
├── semantic_cache.py
├── cache_policy.py
├── memory.py
├── graph_db.py
├── graph_seed.py
├── mcp_client.py
├── prompts/
ui.py
requirements.txt
.env.example
🎯 Key Learnings

This project demonstrates:

✔ Multi-agent AI design
✔ RAG (retrieval-first architecture)
✔ Hybrid search (BM25 + vector)
✔ Graph-based reasoning
✔ Semantic caching
✔ Tool orchestration (MCP)
✔ Memory-driven personalization
✔ Production-ready system thinking

🏁 Future Improvements
Multi-user memory support
Streaming responses
LangSmith / tracing integration
Full cloud deployment (Render / Railway)
Graph + Vector fusion retrieval
💡 Resume Line

Built a modular multi-agent AI assistant integrating RAG (Qdrant), hybrid retrieval (BM25 + vector), Neo4j graph database, Redis semantic caching, and long-term memory for personalized and grounded responses.

🤝 Contributing

Feel free to fork and enhance the system!

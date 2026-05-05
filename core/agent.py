import google.generativeai as genai

from core.router import QueryRouter
from tools.retriever_tool import RetrieverTool
from tools.image_tool import ImageTool
from core.config import GEMINI_API_KEY


class AgentSystem:
    def __init__(self):
        print("🚀 Initializing system...")

        # Router
        self.router = QueryRouter()

        # Tools
        self.retriever = RetrieverTool()
        self.image_tool = ImageTool()

        # LLM
        genai.configure(api_key=GEMINI_API_KEY)
        self.llm = genai.GenerativeModel("gemini-2.5-flash-lite")  # or "gemini-1.5-flash"

        # Memory
        self.chat_history = []
        self.max_history = 5

        print("✅ System ready")

    # -------------------------
    # MEMORY
    # -------------------------
    def get_memory_context(self):
        history_text = ""
        for u, a in self.chat_history[-self.max_history:]:
            history_text += f"User: {u}\nAssistant: {a}\n"
        return history_text

    def save_memory(self, query, response):
        self.chat_history.append((query, response))

    # -------------------------
    # AGENT PROMPT
    # -------------------------
    def agent_prompt(self, query):
        memory = self.get_memory_context()

        return f"""
You are an intelligent Computer book teacher for students.

Conversation so far:
{memory}

You have tools:

1. RetrieverTool(query) → document text
2. ImageTool(query) → analyze images

Rules:
- If question is about document text → CALL_RETRIEVER: <query>
- If about diagrams/images → CALL_IMAGE: <query>
- If both → CALL_BOTH: <query>
- If no tool needed → answer directly

ONLY output:
CALL_RETRIEVER: ...
CALL_IMAGE: ...
CALL_BOTH: ...
OR direct answer

User Question:
{query}
"""

    # -------------------------
    # LLM AGENT (TOOL CALLING)
    # -------------------------
    def run_llm_agent(self, query):
        print("🧠 LLM Agent deciding...")

        decision = self.llm.generate_content(self.agent_prompt(query)).text.strip()
        print("🔍 Decision:", decision)

        memory = self.get_memory_context()

        # RETRIEVER
        if decision.startswith("CALL_RETRIEVER:"):
            tool_query = decision.replace("CALL_RETRIEVER:", "").strip()

            context = self.retriever.run(tool_query)

            if not context.strip():
                return "❌ I couldn't find relevant info in the document."

            prompt = f"""
Conversation:
{memory}

Context:
{context}

Question:
{query}
"""
            return self.llm.generate_content(prompt).text

        # IMAGE
        if decision.startswith("CALL_IMAGE:"):
            tool_query = decision.replace("CALL_IMAGE:", "").strip()
            return self.image_tool.run(tool_query)

        # BOTH
        if decision.startswith("CALL_BOTH:"):
            tool_query = decision.replace("CALL_BOTH:", "").strip()

            context = self.retriever.run(tool_query)
            image_ans = self.image_tool.run(tool_query)

            prompt = f"""
Conversation:
{memory}

Text Context:
{context}

Image Insight:
{image_ans}

Question:
{query}
"""
            return self.llm.generate_content(prompt).text

        # DIRECT
        return decision

    # -------------------------
    # FAST RETRIEVAL
    # -------------------------
    def run_retrieval(self, query):
        print("📄 Retrieval path...")

        context = self.retriever.run(query)

        if not context.strip():
            return "❌ No relevant info found in document."

        memory = self.get_memory_context()

        prompt = f"""
Conversation:
{memory}

Context:
{context}

Question:
{query}
"""
        return self.llm.generate_content(prompt).text

    # -------------------------
    # MAIN RUN
    # -------------------------
    def run(self, query):
        route_info = self.router.route(query)
        route = route_info["route"]

        print("🧭 Route:", route)

        # GREETING
        if route == "greeting":
            response = "👋 Hello! Ask me about the document."
            self.save_memory(query, response)
            return response

        # CASUAL
        if route == "casual":
            response = "🤖 I’m your document assistant."
            self.save_memory(query, response)
            return response

        # INVALID
        if route == "invalid":
            response = "⚠️ Please enter a valid query."
            self.save_memory(query, response)
            return response

        # GIBBERISH
        if route == "gibberish":
            response = "🤖 I couldn't understand that."
            self.save_memory(query, response)
            return response

        # RETRIEVAL
        if route == "retrieval":
            response = self.run_retrieval(query)
            self.save_memory(query, response)
            return response

        # LLM AGENT
        if route == "llm":
            response = self.run_llm_agent(query)
            self.save_memory(query, response)
            return response
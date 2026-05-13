import google.generativeai as genai
from tools.retriever_tool import RetrieverTool
from tools.image_tool import ImageTool
from core.config import GEMINI_API_KEY

class AgentSystem:
    def __init__(self):
        print("🚀 Initializing Pure Agentic system...")

        # Tools
        self.retriever = RetrieverTool()
        self.image_tool = ImageTool()

        # LLM
        genai.configure(api_key=GEMINI_API_KEY)
        self.llm = genai.GenerativeModel("gemini-2.5-flash-lite") # Or gemini-pro depending on what you used

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
        You are an intelligent AI agent.

        Conversation so far:
        {memory}

        You have access to these tools:
        1. RetrieverTool(query) → retrieves relevant text from the document.
        2. ImageTool(query) → analyzes images from the document.

        Your job:
        - Decide what tool is needed based on the user's question.
        - If the question is about document text or concepts → CALL_RETRIEVER: <query>
        - If the question specifically asks about diagrams, charts, or images → CALL_IMAGE: <query>
        - If both are needed → CALL_BOTH: <query>
        - If no tool is needed (e.g., greetings, general chat, or you already know the answer from conversation) → answer directly.

        STRICT RULES:
        Only output ONE of these formats if you need a tool:
        CALL_RETRIEVER: <search query>
        CALL_IMAGE: <search query>
        CALL_BOTH: <search query>
        OR just write your direct answer if no tool is needed.

        User Question:
        {query}
        """

    # -------------------------
    # LLM AGENT (TOOL CALLING)
    # -------------------------
    def run_llm_agent(self, query):
        print("🧠 LLM Agent deciding...")
        decision = self.llm.generate_content(self.agent_prompt(query)).text.strip()
        print("🔍 Agent Decision:", decision)

        memory = self.get_memory_context()

        # -------------------------
        # CALL RETRIEVER
        # -------------------------
        if decision.startswith("CALL_RETRIEVER:"):
            tool_query = decision.replace("CALL_RETRIEVER:", "").strip()
            print("📄 Using Retriever Tool...")
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

        # -------------------------
        # CALL IMAGE TOOL
        # -------------------------
        if decision.startswith("CALL_IMAGE:"):
            tool_query = decision.replace("CALL_IMAGE:", "").strip()
            print("🖼 Using Image Tool...")
            return self.image_tool.run(tool_query)

        # -------------------------
        # CALL BOTH
        # -------------------------
        if decision.startswith("CALL_BOTH:"):
            tool_query = decision.replace("CALL_BOTH:", "").strip()
            print("🔀 Using BOTH tools...")
            context = self.retriever.run(tool_query)
            image_ans = self.image_tool.run(tool_query)

            final_prompt = f"""
            Conversation:
            {memory}
            Text Context:
            {context}
            Image Insight:
            {image_ans}
            Question:
            {query}
            """
            return self.llm.generate_content(final_prompt).text

        # -------------------------
        # DIRECT ANSWER
        # -------------------------
        return decision

    # -------------------------
    # MAIN ENTRY POINT
    # -------------------------
    def run(self, query):
        # Every query goes straight to the LLM to decide
        response = self.run_llm_agent(query)
        self.save_memory(query, response)
        return response
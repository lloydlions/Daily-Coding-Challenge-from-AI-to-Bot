from openai import AsyncOpenAI
import os

class AIEngine:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is missing.")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model_name = "qwen/qwen-2.5-7b-instruct"

    async def generate_challenge(self, lang: str, difficulty: str, framework: str, context: str) -> str:
        prompt = f"""
        Generate a {difficulty} level programming challenge in {lang}. 
        Language Context: {context}

        You MUST output the response in Markdown format using exactly this structure:

        ### 🧩 Daily Coding Challenge: [Creative Title]
        **Language:** {lang} | **Difficulty:** {difficulty}
        
        ---
        
        ### 📝 Problem Statement
        [Detailed description of the task]
        
        ### ⚙️ Setup & Dependencies
        [Provide exact terminal commands or configuration to set up {framework}]
        
        ### 💡 Pro-Tip
        [Provide a strategic hint on how to resolve the problem efficiently]
        
        ### 🎓 Lesson: [Key Concept]
        [Explain a key language feature needed to solve this, e.g., the .toString() method, and show an example of how to use it.]
        
        ### 🧪 Test File
        ```
        // Provide exactly 10 assertions or fewer using {framework}
        ```
        
        ### 🏗️ Boilerplate
        ```
        // Minimal starter code for the solution
        ```
        """
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

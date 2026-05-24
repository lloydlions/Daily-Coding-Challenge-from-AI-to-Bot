import google.generativeai as genai
import os

class AIEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

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
        response = await self.model.generate_content_async(prompt)
        return response.text
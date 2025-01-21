import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

class ContentParser:
    def __init__(self):
        load_dotenv()
        self.setup_logging()
        self.setup_gemini()

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)

    def setup_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def parse_content(self, content: dict, user_question: str = None) -> dict:
        try:
            base_prompt = f"""
            Context: Website content from {content['title']}
            
            Content: {content['text_content'][:2000]}  # First 2000 chars for context
            """
            
            if user_question:
                prompt = f"""
                {base_prompt}
                
                Question: {user_question}
                
                Please provide a detailed answer to the question based on the website content.
                If the content doesn't contain relevant information, please state that clearly.
                """
            else:
                prompt = f"""
                {base_prompt}
                
                Please provide:
                1. A 2-3 sentence summary
                2. Three main takeaways
                """

            response = self.model.generate_content(prompt)
            
            # Clean and truncate content for preview
            clean_text = ' '.join(content['text_content'].split())
            preview_text = clean_text[:500] + "..." if len(clean_text) > 500 else clean_text
            
            return {
                'summary': response.text,
                'original_title': content['title'],
                'preview_text': preview_text,
                'full_text': clean_text,
                'extracted_links': content['links'][:5],  # Show only first 5 links
                'headers': content['headers'][:3],  # Show only first 3 headers
                'all_links': content['links'],
                'all_headers': content['headers']
            }

        except Exception as e:
            self.logger.error(f"Error parsing content: {str(e)}")
            return None

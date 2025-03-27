from together import Together

_TOGETHER_MODEL = "meta-llama/Llama-Vision-Free"

class TogetherLLMClient:
    def __init__(self):
        self.client = Together()
        self.model = _TOGETHER_MODEL
        
    def generate_response(self, query, sources):
        """
        Generate a response using the Together AI LLM based on search results
        
        Args:
            query (str): The original user query
            sources (list): List of source dictionaries from Brave Search
            
        Returns:
            str: Generated response
        """
        # Prepare context from sources
        context = self._prepare_context(sources)
        
        # Create prompt with system instructions
        prompt = self._create_prompt(query, context)
        
        try:
            # Call the Together API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI search assistant. Your task is to provide accurate, comprehensive answers based on the search results provided. Always cite your sources."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response with Together.ai: {e}")
            return f"Sorry, I encountered an error when generating your response: {str(e)}"
    
    def _prepare_context(self, sources):
        """
        Prepare context from the sources for the LLM
        
        Args:
            sources (list): List of source dictionaries
            
        Returns:
            str: Formatted context
        """
        context = "Here are the search results:\n\n"
        
        for i, source in enumerate(sources, 1):
            context += f"SOURCE {i} - {source['title']}\n"
            context += f"URL: {source['url']}\n"
            
            # Include a snippet of the content, not everything to save on tokens
            content_preview = source['content'][:500] + "..." if len(source['content']) > 500 else source['content']
            context += f"CONTENT: {content_preview}\n\n"
        
        return context
    
    def _create_prompt(self, query, context):
        """
        Create a prompt for the LLM
        
        Args:
            query (str): The original user query
            context (str): The formatted context from sources
            
        Returns:
            str: Complete prompt
        """
        return f"""
            I need you to answer the following query: "{query}"

            {context}

            Based on these search results, provide a comprehensive answer to the query. 
            Include relevant information from the sources and cite where you got information from (Source 1, Source 2, etc.).
            If the search results don't contain enough information to fully answer the query, acknowledge this limitation.
            """
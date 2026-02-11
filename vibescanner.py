import os
import re
from dotenv import load_dotenv
from google import genai
from typing import Dict
import json
# Using a hypothetical wrapper for your chosen LLM (e.g., Gemini or OpenAI)
#from engine_core import SovereignLLM 

class VibeScanner:
    def __init__(self, api_key: str):
        
        self.client=genai.Client(api_key=api_key)
        self.model= os.getenv("MODEL_ID")
        
        # Defining the "Inception Markers" for 2026
        self.markers = {
            "hive": ["coachable", "low-ego", "culture-fit", "alignment", "seamless", "high-sync"],
            "sovereign": ["autonomy", "dissent", "first principles", "high-variance", "sovereign", "unconventional"]
        }

    def analyze_jd(self, jd_text: str):
        """
        Analyzes a JD for psychological entrainment and 'Borg' markers.
        """
        prompt = f"""
        Act as a Systems Auditor. Analyze the following Job Description for 'Inception' techniques.
        
        JD TEXT: 
        {jd_text}
        
        Identify:
        1. THE UNSPOKEN COMMAND: What is the company actually asking for (e.g., Compliance vs. Innovation)?
        2. THE FRICTION SCORE: On a scale of 1-10, how likely is a 'Self-Aware' individual to be rejected?
        3. EUPHEMISM DECODER: Translate corporate terms (e.g., 'Moving as one' -> 'Hive Mind requirement').
        
        Return the result in JSON format with keys: 'command', 'friction_score', 'translations', and 'vibe_type'.
        """
        
        #analysis = os.getenv("temp_text")
        analysis = self.client.models.generate_content(model=self.model, contents=prompt)
        
        if analysis and analysis.text:
            return self.format_response(analysis.text)
        else:
            return None
    
    def format_response(self,json_text:str):
        try:
            match = re.search(r'(\{.*\}|\[.*\])', json_text, re.DOTALL)
            
            if match:
                json_str = match.group(1)
                
            response = []
            data = json.loads(json_str)
            response.append("<h1>What is the company actually asking for (e.g., Compliance vs. Innovation)?</h1>")
            response.append(data["command"])
            response.append("<br/><br/>")
            
            response.append("<h1>On a scale of 1-10, how likely is a 'Self-Aware' individual to be rejected?</h1>")
            response.append(str(data["friction_score"]) )
            response.append("<br/><br/>")        
            
            if data["translations"] and len(data["translations"].items()) >0:
                response.append("<h1>Translate corporate terms (e.g., 'Moving as one' -> 'Hive Mind requirement')</h1><br/>")
                for k,v in data["translations"].items():                      
                    response.append("<b>{0}</b> -> {1}".format(k,v))
                    response.append("<br/><br/>")
            
            response.append("<h1>Vibe Type</h1>")           
            response.append(data["vibe_type"])
            response.append("<br/><br/>")
            
            return "\n".join(response)
        except json.JSONDecodeError as e:
            return json_text
        except Exception as e:
            return str(e)

# Example Usage
'''
if __name__ == "__main__":
    load_dotenv()
    scanner = VibeScanner(api_key=os.getenv("API_KEY"))
    
    # Testing with a 'Meta-style' JD snippet
    test_jd = "We are looking for a culture-first engineer who prioritizes alignment and is highly coachable."
    
    report = scanner.analyze_jd(test_jd)
    print(f"VIBE REPORT: {report}")
'''
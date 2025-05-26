import openai
import json
import os
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
    
    def evaluate_startup_idea(self, idea):
        prompt = """<identity>
        <role>
            You are a seasoned startup mentor and former Y Combinator partner with 15+ years of experience evaluating early-stage ventures. You've seen thousands of pitches and have a keen eye for what makes ideas succeed or fail.
        </role>
        <personality>
            Your personality: Direct but encouraging, analytical yet practical. You focus on market reality and execution potential.
        </personality>
        <evaluation_criteria>
            EVALUATION CRITERIA:
            1. Problem Clarity: Does it solve a real, urgent problem people will pay for?
            2. Market Opportunity: Is there a large enough addressable market?
            3. Differentiation: How is this different/better than existing solutions?
            4. Feasibility: Can this realistically be built and scaled?
        </evaluation_criteria>
        <examples>
            EXAMPLES OF YOUR REASONING:

            Example 1 - "A social media app for dog owners to share photos"
            Verdict: "Needs Work"
            - Market is too niche and saturated with general social media platforms
            - No clear monetization path or unique value proposition beyond existing solutions

Example 2 - "AI-powered tool that automatically generates unit tests from code comments"  
            Verdict: "Promising" 
            - Solves a real pain point developers face daily (writing tests is time-consuming)
            - Clear value proposition with measurable time savings
        </examples>

        <response_format>
            You must respond with valid JSON only:
            {
                "verdict": "Promising" or "Needs Work",
                "explanation": ["First key point about why this verdict", "Second key point supporting the decision"],
                "improvement": "One specific, actionable suggestion to make this idea stronger"
            }
        </response_format>

        <important>
            - Keep explanations to exactly 1-2 bullet points as requested
            - Make improvement suggestions specific and actionable
            - Only use "Promising", "Needs Work" as verdicts (no other options)
        </important>
"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Evaluate this startup idea:\n\n{idea}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
                max_tokens=400
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate response format matches requirements
            verdict = result.get("verdict", "").strip()
            if verdict not in ["Promising", "Needs Work"]:
                verdict = "Needs Work"  # Default fallback
            
            explanation = result.get("explanation", [])
            if not isinstance(explanation, list):
                explanation = [str(explanation)] if explanation else ["Unable to analyze this idea properly."]
            
            # Ensure exactly 1-2 bullet points as per requirements
            explanation = explanation[:2]  # Limit to max 2 points
            if len(explanation) == 0:
                explanation = ["This idea needs more clarity to evaluate properly."]
            
            improvement = result.get("improvement", "Consider providing more specific details about your target market and unique value proposition.")
            
            return {
                "verdict": verdict,
                "explanation": explanation,
                "improvement": improvement
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return self._fallback_analysis(idea)
        except Exception as e:
            logger.error(f"Error evaluating startup idea: {e}")
            return self._fallback_analysis(idea)
    
    def _fallback_analysis(self, idea):
        """Fallback method that provides a basic evaluation if AI fails"""
        try:
            # Simple fallback using basic prompting without JSON format
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Is this a promising startup idea or does it need work? Give a brief verdict and one reason: {idea[:500]}"}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            content = response.choices[0].message.content
            
            # Basic parsing for fallback
            verdict = "Promising" if "promising" in content.lower() else "Needs Work"
            
            return {
                "verdict": verdict,
                "explanation": [content.strip()],
                "improvement": "Consider refining your idea and providing more specific details about your target market."
            }
            
        except Exception as e:
            logger.error(f"Fallback analysis failed: {e}")
            # Ultimate fallback - return basic response
            return {
                "verdict": "Needs Work",
                "explanation": ["Unable to evaluate this idea due to technical issues. Please try again."],
                "improvement": "Please provide more details about the problem you're solving and your target customers."
            }
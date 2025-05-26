import openai
import json
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

class AIService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
    
    def evaluate_startup_idea(self, idea, location="Remote/Online"):
        prompt = f"""<identity>
        <role>
            You are a seasoned startup mentor and former Y Combinator partner with 15+ years of experience evaluating early-stage ventures. You've seen thousands of pitches and have a keen eye for what makes ideas succeed or fail. You understand how location impacts startup success.
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
        <location_context>
            LOCATION CONTEXT: {location}
            Consider location only when it's specifically relevant to the idea's success (e.g., local services, regulatory constraints, market maturity). For most tech/online ideas, focus on the core concept.
        </location_context>
        <examples>
            EXAMPLES OF YOUR REASONING:

            Example 1 - "A social media app for dog owners to share photos" (San Francisco)
            Verdict: "Needs Work"
            - Market is too niche and saturated with general social media platforms
            - San Francisco has high competition and development costs for consumer social apps

            Example 2 - "AI-powered tool that automatically generates unit tests" (Remote/Online)  
            Verdict: "Promising" 
            - Solves a real pain point developers face daily
            - Clear value proposition with measurable time savings

            Example 3 - "Food delivery for busy professionals" (Lagos, Nigeria)
            Verdict: "Promising"
            - Addresses real need in growing urban market
            - Local opportunity due to less mature delivery infrastructure
        </examples>

        <gibberish_detection>
            IMPORTANT: If the idea description is unclear, nonsensical, too vague, or appears to be gibberish/random text, use verdict "Needs Clarification" and ask them to re-explain.
        </gibberish_detection>

        <response_format>
            You must respond with valid JSON only:
            {{
                "verdict": "Promising" or "Needs Work" or "Needs Clarification",
                "explanation": ["First key point about why this verdict", "Second key point supporting the decision"],
                "improvement": "One specific, actionable suggestion to make this idea stronger",
                "location_note": "Brief note on location relevance (only if location significantly impacts the idea)"
            }}
        </response_format>

        <important>
            - Keep explanations to exactly 1-2 bullet points as requested
            - Make improvement suggestions specific and actionable
            - Use "Promising", "Needs Work", or "Needs Clarification" as verdicts only
            - Include location note only when location significantly impacts the idea
            - For most online/tech ideas, location may not be relevant to mention
        </important>
"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Evaluate this startup idea for location '{location}':\n\n{idea}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate response format
            verdict = result.get("verdict", "").strip()
            if verdict not in ["Promising", "Needs Work", "Needs Clarification"]:
                verdict = "Needs Work"  # Default fallback
            
            explanation = result.get("explanation", [])
            if not isinstance(explanation, list):
                explanation = [str(explanation)] if explanation else ["Unable to analyze this idea properly."]
            
            # Ensure exactly 1-2 bullet points
            explanation = explanation[:2]
            if len(explanation) == 0:
                explanation = ["This idea needs more clarity to evaluate properly."]
            
            improvement = result.get("improvement", "Consider providing more specific details about your target market and unique value proposition.")
            location_impact = result.get("location_impact", "Location not clearly analyzed. It may not be relevant to the idea.")
            
            return {
                "verdict": verdict,
                "explanation": explanation,
                "improvement": improvement,
                "location_impact": location_impact
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return self._fallback_analysis(idea, location)
        except Exception as e:
            logger.error(f"Error evaluating startup idea: {e}")
            return self._fallback_analysis(idea, location)
    
    def _fallback_analysis(self, idea, location):
        """Fallback method that provides a basic evaluation if AI fails"""
        try:
            # Simple fallback using basic prompting without JSON format
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Is this a promising startup idea or does it need work? Consider location '{location}'. Give a brief verdict and one reason: {idea[:500]}"}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            
            # Basic parsing for fallback
            if any(word in content.lower() for word in ["unclear", "confusing", "gibberish", "doesn't make sense"]):
                verdict = "Needs Clarification"
            elif "promising" in content.lower():
                verdict = "Promising"
            else:
                verdict = "Needs Work"
            
            return {
                "verdict": verdict,
                "explanation": [content.strip()],
                "improvement": "Consider refining your idea and providing more specific details about your target market.",
                "location_impact": f"Location '{location}' context needs more detailed analysis."
            }
            
        except Exception as e:
            logger.error(f"Fallback analysis failed: {e}")
            # Ultimate fallback
            return {
                "verdict": "Needs Clarification",
                "explanation": ["Unable to evaluate this idea due to technical issues. Please try again with a clear description."],
                "improvement": "Please provide more details about the problem you're solving and your target customers.",
                "location_impact": "Location impact could not be analyzed."
            }
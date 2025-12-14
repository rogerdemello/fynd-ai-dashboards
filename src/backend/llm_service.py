"""LLM integration for Task 2 - uses Google Gemini API."""
import os
from typing import Tuple

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def configure_genai():
    """Configure Gemini API with key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or not GENAI_AVAILABLE:
        return False
    genai.configure(api_key=api_key)
    return True


def generate_user_response(rating: int, review: str) -> str:
    """Generate a user-facing response based on rating and review."""
    if not configure_genai():
        return f"Thank you for your {rating}-star review! We appreciate your feedback."
    
    prompt = f"""You are a customer service representative. A user submitted a {rating}-star review with the following text:
"{review}"

Write a short, friendly response (2-3 sentences) thanking them and addressing their feedback appropriately."""
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=150,
                temperature=0.7,
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"Thank you for your {rating}-star review! We value your feedback."


def generate_admin_summary(rating: int, review: str) -> str:
    """Generate an internal summary for admin dashboard."""
    if not configure_genai():
        return f"User rated {rating} stars. Review: {review[:100]}..."
    
    prompt = f"""Summarize this customer review in one concise sentence for internal use:
Rating: {rating} stars
Review: "{review}"

Keep it brief and factual."""
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=80,
                temperature=0.3,
            )
        )
        return response.text.strip()
    except Exception:
        return f"{rating}-star review: {review[:80]}..."


def generate_recommended_action(rating: int, review: str) -> str:
    """Generate recommended next actions for admin."""
    if not configure_genai():
        if rating <= 2:
            return "Priority follow-up required. Contact customer within 24 hours."
        elif rating == 3:
            return "Monitor for patterns. Consider process improvements."
        else:
            return "Positive feedback. Share with team."
    
    prompt = f"""Based on this customer review, suggest one specific action for the business (1-2 sentences):
Rating: {rating} stars
Review: "{review}"

Focus on actionable next steps."""
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=100,
                temperature=0.5,
            )
        )
        return response.text.strip()
    except Exception:
        if rating <= 2:
            return "Priority follow-up required."
        return "Review and acknowledge feedback."

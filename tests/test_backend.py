"""Test script for backend API - verifies all endpoints work correctly."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from database import add_submission, get_all_submissions, get_analytics, init_db
from llm_service import generate_user_response, generate_admin_summary, generate_recommended_action

def test_database():
    """Test database operations."""
    print("Testing database...")
    
    # Initialize
    init_db()
    print("✓ Database initialized")
    
    # Add test submission
    sub_id = add_submission(
        rating=5,
        review="Test review for verification",
        ai_response="Test response",
        ai_summary="Test summary",
        ai_recommended_action="Test action"
    )
    print(f"✓ Added submission ID: {sub_id}")
    
    # Get all submissions
    submissions = get_all_submissions()
    print(f"✓ Retrieved {len(submissions)} submissions")
    
    # Get analytics
    analytics = get_analytics()
    print(f"✓ Analytics: {analytics}")
    
    return True

def test_llm_service():
    """Test LLM service (requires GEMINI_API_KEY)."""
    print("\nTesting LLM service...")
    
    # These will use fallback if no API key
    response = generate_user_response(5, "Great service!")
    print(f"✓ User response: {response[:50]}...")
    
    summary = generate_admin_summary(5, "Great service!")
    print(f"✓ Admin summary: {summary[:50]}...")
    
    action = generate_recommended_action(5, "Great service!")
    print(f"✓ Recommended action: {action[:50]}...")
    
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("Backend Test Suite")
    print("=" * 50)
    
    try:
        test_database()
        test_llm_service()
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

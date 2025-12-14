"""User Dashboard - Public-facing review submission interface."""
import streamlit as st
import requests
import os
import sys
from pathlib import Path

# Configuration
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# End of configuration

st.set_page_config(
    page_title="Customer Feedback",
    page_icon="⭐",
    layout="centered"
)

st.title("⭐ Share Your Feedback")
st.markdown("We value your opinion! Please rate your experience and share your thoughts.")

# Rating selection
rating = st.select_slider(
    "How would you rate your experience?",
    options=[1, 2, 3, 4, 5],
    value=5,
    format_func=lambda x: "⭐" * x
)

# Review text
review = st.text_area(
    "Tell us about your experience:",
    placeholder="Share your thoughts here...",
    height=150,
    max_chars=5000
)

# Submit button
if st.button("Submit Feedback", type="primary", use_container_width=True):
    if not review.strip():
        st.error("Please write a review before submitting.")
    else:
        with st.spinner("Processing your feedback..."):
            try:
                # Call API
                response = requests.post(
                    f"{API_URL}/api/submit",
                    json={"rating": rating, "review": review},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Thank you for your feedback!")
                    
                    # Display AI response
                    st.markdown("---")
                    st.markdown("### Our Response")
                    st.info(data["ai_response"])
                    
                    # Show submission ID
                    st.caption(f"Submission ID: {data['id']}")
                else:
                    st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to server. Please ensure the backend API is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.caption("Powered by AI | Your feedback helps us improve")

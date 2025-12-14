"""Admin Dashboard - Internal view of all submissions with analytics."""
import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

# Configuration
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# End of configuration

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Admin Dashboard - Customer Feedback Analytics")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 30s)", value=False)
if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()

# Refresh button
if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()

# Fetch data
try:
    # Get analytics
    analytics_response = requests.get(f"{API_URL}/api/analytics", timeout=10)
    analytics = analytics_response.json() if analytics_response.status_code == 200 else {}
    
    # Get submissions
    submissions_response = requests.get(f"{API_URL}/api/submissions", timeout=10)
    submissions_data = submissions_response.json() if submissions_response.status_code == 200 else {"submissions": []}
    submissions = submissions_data.get("submissions", [])
    
    # Display analytics
    st.markdown("## 📈 Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Submissions", analytics.get("total_submissions", 0))
    
    with col2:
        avg_rating = analytics.get("average_rating", 0)
        st.metric("Average Rating", f"{avg_rating:.2f} ⭐")
    
    with col3:
        rating_dist = analytics.get("rating_distribution", {})
        if rating_dist:
            most_common = max(rating_dist.items(), key=lambda x: x[1])
            st.metric("Most Common Rating", f"{most_common[0]} ⭐ ({most_common[1]} reviews)")
        else:
            st.metric("Most Common Rating", "N/A")
    
    # Rating distribution chart
    if rating_dist:
        st.markdown("### Rating Distribution")
        dist_df = pd.DataFrame([
            {"Rating": f"{k} ⭐", "Count": v} 
            for k, v in sorted(rating_dist.items())
        ])
        st.bar_chart(dist_df.set_index("Rating"))
    
    # Submissions table
    st.markdown("---")
    st.markdown("## 📋 Recent Submissions")
    
    if submissions:
        # Convert to DataFrame
        df = pd.DataFrame(submissions)
        
        # Format datetime
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
        
        # Display detailed view
        for idx, row in df.iterrows():
            with st.expander(
                f"⭐ {row['rating']} | ID: {row['id']} | {row.get('created_at', 'N/A')}",
                expanded=idx < 3  # Expand first 3
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Customer Review:**")
                    st.write(row["review"])
                    
                    st.markdown("**AI Response to Customer:**")
                    st.info(row["ai_response"])
                
                with col2:
                    st.markdown("**Internal Summary:**")
                    st.write(row["ai_summary"])
                    
                    st.markdown("**Recommended Action:**")
                    st.warning(row["ai_recommended_action"])
                    
                    st.markdown("**Details:**")
                    st.caption(f"Rating: {'⭐' * row['rating']}")
                    st.caption(f"Submitted: {row.get('created_at', 'N/A')}")
    else:
        st.info("No submissions yet. Waiting for customer feedback...")

except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to backend API. Please ensure the server is running at " + API_URL)
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")

# Footer
st.markdown("---")
st.caption(f"Connected to: {API_URL} | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

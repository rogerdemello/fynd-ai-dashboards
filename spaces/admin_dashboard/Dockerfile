FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose HF Spaces port
ENV PORT=7860

# Run Streamlit admin dashboard
CMD ["streamlit", "run", "src/dashboards/admin_dashboard.py", "--server.port", "7860", "--server.headless", "true"]

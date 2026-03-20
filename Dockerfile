# 1. Base Image: Python 3.9 Slim
FROM python:3.9-slim

# 2. Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Work Directory
WORKDIR /app

# 4. System Deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Python Deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. App Code
COPY . .

# 7. Ports
EXPOSE 8501

# 8. Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 9. Run
CMD ["streamlit", "run", "app_dashboard.py", "--server.address=0.0.0.0"]
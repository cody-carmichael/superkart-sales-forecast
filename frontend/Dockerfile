# Same slim Python 3.9 base as the backend
FROM python:3.9-slim

WORKDIR /app

# Bring in app.py and requirements.txt
COPY . .

RUN pip3 install -r requirements.txt

# Run Streamlit on port 8501 and listen on all interfaces so Codespaces can forward it
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]

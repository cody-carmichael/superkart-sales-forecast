FROM python:3.9-slim

# Everything lives in /app inside the container
WORKDIR /app

# Bring in app.py, requirements.txt and the model file
COPY . .

# Install the pinned libraries; --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Start gunicorn with 4 workers on port 7860
# app:superkart_api means "in app.py, run the Flask object called superkart_api"
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]

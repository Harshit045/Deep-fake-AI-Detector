# Stage 1: Build the React Frontend
FROM node:20 AS frontend-builder
WORKDIR /frontend
COPY forensic-frontend/package*.json ./
RUN npm install
COPY forensic-frontend/ ./
RUN npm run build

# Use official Python image
FROM python:3.10-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy built frontend from Stage 1 to Flask's static folder
COPY --from=frontend-builder /frontend/dist /app/static

# Hugging Face runs on port 7860 by default
EXPOSE 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "app:app"]
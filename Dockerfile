# Multi-stage Dockerfile for textbook generation system

# Backend stage
FROM python:3.11-slim as backend

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/src ./src

# Expose port
EXPOSE 8000

# Command to run the backend
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Frontend stage (build)
FROM node:18 as frontend-build

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/tsconfig.json .

# Build the frontend
RUN npm run build


# Frontend stage (serve)
FROM nginx:alpine as frontend

# Copy built frontend to nginx
COPY --from=frontend-build /app/frontend/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY frontend/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
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


# Docusaurus Frontend stage (build)
FROM node:18 as docusaurus-build

WORKDIR /app/website

# Copy package files
COPY website/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY website/src ./src
COPY website/docs ./docs
COPY website/static ./static
COPY website/docusaurus.config.js ./
COPY website/sidebars.js ./
COPY website/tsconfig.json ./

# Build the Docusaurus site
RUN npm run build


# Docusaurus Frontend stage (serve)
FROM nginx:alpine as frontend

# Copy built Docusaurus site to nginx
COPY --from=docusaurus-build /app/website/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY website/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
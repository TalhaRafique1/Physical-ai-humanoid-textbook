# Quickstart: Textbook Generation

## Overview
Get started with the textbook generation feature by following these steps to set up your development environment and run the service locally.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend development)
- Poetry (for Python dependency management) or pip
- Access to an LLM API (OpenAI, Anthropic, or open-source alternative)

## Backend Setup

### 1. Environment Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
poetry install
# OR if using pip
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here  # Or other LLM provider key
DATABASE_URL=postgresql://user:password@localhost:5432/textbook_generation
QDRANT_URL=http://localhost:6333
NEON_DATABASE_URL=your_neon_db_url
SECRET_KEY=your_secret_key_here
```

### 3. Run Backend Service
```bash
# Activate virtual environment
poetry shell

# Run the backend server
python -m src.api.main

# Or with uvicorn for development
uvicorn src.api.main:app --reload --port 8000
```

## Frontend Setup

### 1. Install Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 2. Environment Variables
Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

### 3. Run Frontend
```bash
# Start the development server
npm start
```

## API Usage Examples

### 1. Start Textbook Generation
```bash
curl -X POST http://localhost:8000/textbook-generation \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Introduction to Machine Learning",
    "target_audience": "undergraduate",
    "num_chapters": 8,
    "content_depth": "medium",
    "writing_style": "formal"
  }'
```

### 2. Check Generation Progress
```bash
curl http://localhost:8000/textbook-generation/gen_1234567890/progress
```

### 3. Export Textbook
```bash
curl -X POST http://localhost:8000/export \
  -H "Content-Type: application/json" \
  -d '{
    "generation_id": "gen_1234567890",
    "format": "pdf"
  }'
```

## Key Endpoints

- `POST /textbook-generation` - Start new textbook generation
- `GET /textbook-generation/{id}` - Get generation details
- `GET /textbook-generation/{id}/progress` - Get generation progress
- `GET /textbook-generation/{id}/preview` - Get textbook preview
- `POST /export` - Export textbook in specified format

## Testing

### Backend Tests
```bash
# Run all backend tests
poetry run pytest

# Run specific test file
poetry run pytest tests/unit/test_textbook_generation.py
```

### Frontend Tests
```bash
# Run frontend tests
npm test

# Run end-to-end tests
npm run test:e2e
```

## Development Workflow

1. **Create a new branch** for your feature
2. **Implement backend services** following the defined contracts
3. **Write unit tests** for new functionality
4. **Implement frontend components** to match the API contracts
5. **Test integration** between frontend and backend
6. **Update documentation** as needed
7. **Submit pull request** for review

## Troubleshooting

### Common Issues
- **LLM API errors**: Verify your API key and rate limits
- **Memory issues**: For large textbooks, ensure adequate memory allocation
- **Format conversion failures**: Check that Pandoc is properly installed

### Useful Commands
```bash
# Check backend API status
curl http://localhost:8000/health

# View backend logs
tail -f logs/app.log

# Format Python code
black src/

# Format JavaScript/TypeScript code
npm run format
```
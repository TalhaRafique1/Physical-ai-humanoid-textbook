# Textbook Generation System

A system for generating structured textbooks with chapters, sections, and formatting based on user-provided topics and parameters.

## Project Structure

```
book/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── models/          # Data models
│   │   ├── services/        # Business logic services
│   │   ├── api/             # API routes
│   │   └── config/          # Configuration files
│   ├── requirements.txt     # Python dependencies
│   └── tests/               # Backend tests
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── types/           # TypeScript types
│   ├── package.json         # Node.js dependencies
│   └── tests/               # Frontend tests
├── specs/001-textbook-generation/  # Feature specifications
│   ├── spec.md             # Feature specification
│   ├── plan.md             # Implementation plan
│   ├── data-model.md       # Data model
│   ├── research.md         # Research findings
│   └── tasks.md            # Implementation tasks
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (optional, for containerized deployment)
- Pandoc (for export functionality) - Install from https://pandoc.org/installing.html

### Local Development

1. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn src.api.main:app --reload
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Docker Setup

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/api/docs

## Features

- Generate structured textbooks with chapters and sections
- Customize content depth, writing style, and target audience
- Export textbooks in multiple formats (PDF, DOCX, EPUB)
- Real-time progress tracking during generation
- Content validation for educational appropriateness
- Integration with educational content sources (Wikipedia, arXiv)

## Usage Instructions

### 1. Generating a Textbook

1. Navigate to the textbook generation page in the frontend
2. Fill in the generation parameters:
   - **Topic**: The main subject for your textbook
   - **Target Audience**: Select from elementary, middle school, high school, undergraduate, graduate, professional, or general
   - **Content Depth**: Choose from shallow, medium, or deep
   - **Writing Style**: Select from formal, conversational, technical, academic, or casual
   - **Number of Chapters**: Specify how many chapters to generate (1-100)
   - **Sections per Chapter**: Number of sections in each chapter (1-20)
   - **Include Examples**: Whether to include practical examples
   - **Include Exercises**: Whether to include practice exercises
   - **Required Sources**: Add sources to reference (e.g., Wikipedia, arXiv)
   - **Excluded Topics**: Add topics to avoid
   - **Custom Instructions**: Any special requirements for content generation

3. Click "Generate Textbook" to start the process
4. Monitor progress in real-time using the progress indicator
5. Once complete, preview the generated content

### 2. Exporting a Textbook

1. After generating a textbook, navigate to the export page
2. Select the desired export format (PDF, DOCX, EPUB, HTML, TXT)
3. Click "Export" to generate the formatted file
4. Download the exported file when complete

### 3. Using the API Directly

You can also interact with the system using the API endpoints:

**Generate a textbook:**
```bash
curl -X POST http://localhost:8000/api/textbook-generation/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Introduction to Machine Learning",
    "targetAudience": "undergraduate",
    "numChapters": 5,
    "contentDepth": "medium",
    "writingStyle": "academic",
    "sectionsPerChapter": 3,
    "includeExamples": true,
    "includeExercises": false
  }'
```

**Check generation status:**
```bash
curl http://localhost:8000/api/textbook-generation/status/{textbook_id}
```

**Export a textbook:**
```bash
curl -X POST http://localhost:8000/api/export/generate \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "textbook_id={textbook_id}&format_name=PDF"
```

## API Endpoints

The backend API provides the following main endpoints:
- `POST /api/textbook-generation/generate` - Generate a new textbook
- `GET /api/textbook-generation/status/{textbook_id}` - Get generation status
- `GET /api/textbook-generation/{textbook_id}` - Get textbook details
- `GET /api/textbook-generation/list` - List all textbooks
- `POST /api/export/generate` - Export textbook in specified format
- `GET /api/export/formats` - Get supported export formats
- `GET /api/export/status/{textbook_id}` - Get export status
- `GET /api/export/download/{textbook_id}/{format_name}` - Download exported file
- `GET /api/preview/content/{textbook_id}` - Get textbook content preview
- `GET /api/preview/chapter/{textbook_id}/{chapter_number}` - Get chapter preview
- `GET /api/preview/toc/{textbook_id}` - Get table of contents
- `GET /api/preview/metadata/{textbook_id}` - Get textbook metadata
- `GET /health` - Health check endpoint
- `GET /api/docs` - Interactive API documentation

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Architecture

The system follows a modular architecture with clean separation of concerns:

- **Models**: Define the data structures (Textbook, Chapter, Section, etc.)
- **Services**: Contain business logic (generation, enrichment, export, validation)
- **API**: Handle HTTP requests and responses
- **Utils**: Provide helper functions (document conversion, progress tracking)
# Data Model: Textbook Generation

## Textbook Entity

**Definition**: A structured educational document containing chapters, sections, and metadata

**Fields**:
- `id` (string/UUID): Unique identifier for the textbook
- `title` (string): Title of the textbook
- `description` (string): Brief description of the textbook content
- `created_at` (datetime): Timestamp when the textbook was created
- `updated_at` (datetime): Timestamp when the textbook was last modified
- `status` (enum): Current status (draft, generating, completed, failed, exported)
- `total_chapters` (integer): Number of chapters in the textbook
- `target_audience` (string): Intended audience level (e.g., high school, undergraduate, graduate)
- `content_depth` (string): Depth level (shallow, medium, deep)
- `writing_style` (string): Writing style preference (formal, conversational, technical)
- `estimated_pages` (integer): Estimated number of pages
- `generated_content` (text): The actual textbook content in structured format
- `export_formats` (array): List of supported export formats
- `metadata` (object): Additional metadata (author, subject, tags, etc.)

## Chapter Entity

**Definition**: A major division of a textbook containing sections and content

**Fields**:
- `id` (string/UUID): Unique identifier for the chapter
- `textbook_id` (string/UUID): Reference to the parent textbook
- `title` (string): Title of the chapter
- `chapter_number` (integer): Sequential number of the chapter
- `word_count` (integer): Number of words in the chapter
- `sections_count` (integer): Number of sections in the chapter
- `content` (text): The chapter content
- `summary` (string): Brief summary of the chapter
- `learning_objectives` (array): List of learning objectives for this chapter

## Section Entity

**Definition**: A subdivision of a chapter containing specific topics or concepts

**Fields**:
- `id` (string/UUID): Unique identifier for the section
- `chapter_id` (string/UUID): Reference to the parent chapter
- `title` (string): Title of the section
- `section_number` (string): Number of the section (e.g., "1.1", "1.2")
- `content` (text): The section content
- `content_type` (enum): Type of content (text, example, exercise, summary)
- `word_count` (integer): Number of words in the section

## GenerationParameters Entity

**Definition**: User-specified settings for textbook generation

**Fields**:
- `id` (string/UUID): Unique identifier for the parameters set
- `user_id` (string/UUID): Reference to the user who created these parameters (optional)
- `topic` (string): Main topic or subject area for the textbook
- `target_audience` (string): Intended audience level
- `num_chapters` (integer): Desired number of chapters
- `content_depth` (string): Depth level preference
- `writing_style` (string): Writing style preference
- `sections_per_chapter` (integer): Desired number of sections per chapter
- `include_examples` (boolean): Whether to include examples
- `include_exercises` (boolean): Whether to include exercises
- `required_sources` (array): List of required source materials to reference
- `excluded_topics` (array): List of topics to avoid
- `custom_instructions` (text): Any special instructions for generation

## ExportFormat Entity

**Definition**: Specification for export format options

**Fields**:
- `id` (string/UUID): Unique identifier for the format
- `name` (string): Format name (PDF, DOCX, EPUB, etc.)
- `extension` (string): File extension
- `description` (string): Description of the format
- `options` (object): Format-specific options (margins, fonts, etc.)
- `is_default` (boolean): Whether this is the default export format

## Relationships

- **Textbook** (1) → (Many) **Chapter**: A textbook contains multiple chapters
- **Chapter** (1) → (Many) **Section**: A chapter contains multiple sections
- **Textbook** (1) → (1) **GenerationParameters**: Each textbook has one set of generation parameters
- **Textbook** (1) → (Many) **ExportFormat**: A textbook can be exported in multiple formats

## Validation Rules

### Textbook Validation
- Title must be 1-200 characters
- Status must be one of the defined enum values
- Target audience must be from predefined list
- Content depth must be from predefined list
- Total chapters must be between 1 and 1000

### Chapter Validation
- Title must be 1-100 characters
- Chapter number must be positive
- Must belong to a valid textbook

### Section Validation
- Title must be 1-100 characters
- Section number must follow proper hierarchy format
- Must belong to a valid chapter

### GenerationParameters Validation
- Topic must be provided and 1-200 characters
- Target audience must be from predefined list
- Number of chapters must be between 1 and 100
- Content depth must be from predefined list
- Writing style must be from predefined list

## State Transitions

**Textbook Status Transitions**:
1. `draft` → `generating` (when generation starts)
2. `generating` → `completed` (when generation finishes successfully)
3. `generating` → `failed` (when generation encounters an error)
4. `completed` → `exported` (when successfully exported to a format)
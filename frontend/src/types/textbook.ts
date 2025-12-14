// Textbook Generation System - TypeScript Interfaces

// Textbook status enumeration
export enum TextbookStatus {
  DRAFT = 'draft',
  GENERATING = 'generating',
  COMPLETED = 'completed',
  FAILED = 'failed',
  EXPORTED = 'exported'
}

// Textbook interface
export interface Textbook {
  id: string;
  title: string;
  description: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
  status: TextbookStatus;
  totalChapters: number;
  targetAudience: string;
  contentDepth: string;
  writingStyle: string;
  estimatedPages: number;
  generatedContent?: string;
  exportFormats: string[];
  metadata: Record<string, any>;
}

// Generation parameters interface
export interface GenerationParams {
  id?: string;
  userId?: string;
  topic: string;
  targetAudience: string;
  numChapters: number;
  contentDepth: string;
  writingStyle: string;
  sectionsPerChapter: number;
  includeExamples: boolean;
  includeExercises: boolean;
  requiredSources: string[];
  excludedTopics: string[];
  customInstructions: string;
}

// Chapter interface
export interface Chapter {
  id: string;
  textbookId: string;
  title: string;
  chapterNumber: number;
  wordCount: number;
  sectionsCount: number;
  content?: string;
  summary?: string;
  learningObjectives: string[];
}

// Section content type enumeration
export enum ContentType {
  TEXT = 'text',
  EXAMPLE = 'example',
  EXERCISE = 'exercise',
  SUMMARY = 'summary',
  INTRODUCTION = 'introduction',
  CONCLUSION = 'conclusion'
}

// Section interface
export interface Section {
  id: string;
  chapterId: string;
  title: string;
  sectionNumber: string;
  content?: string;
  contentType: ContentType;
  wordCount: number;
}

// Export format interface
export interface ExportFormat {
  id: string;
  name: string;
  extension: string;
  description: string;
  options: Record<string, any>;
  isDefault: boolean;
}

// Textbook generation status interface
export interface GenerationStatus {
  textbookId: string;
  status: string;
  progress: number;
  message: string;
  updatedAt: string;
}

// Export status interface
export interface ExportStatus {
  textbookId: string;
  exportFormats: string[];
  status: string;
  lastExported?: string;
}

// API response interfaces
export interface GenerateTextbookResponse {
  textbookId: string;
  status: string;
  message: string;
  estimatedCompletion?: string;
}

export interface ExportTextbookResponse {
  success: boolean;
  textbookId: string;
  format: string;
  outputPath: string;
  fileSize: number;
  message: string;
  error?: string;
}

export interface TextbookPreview {
  textbookId: string;
  title: string;
  description: string;
  status: TextbookStatus;
  preview: string;
  fullContentAvailable: boolean;
  contentLength: number;
  totalChapters: number;
  targetAudience: string;
  contentDepth: string;
  writingStyle: string;
  generatedAt: string;
}

export interface ChapterPreview {
  textbookId: string;
  chapterNumber: number;
  title: string;
  preview: string;
  targetAudience: string;
  contentDepth: string;
}

export interface TableOfContents {
  textbookId: string;
  title: string;
  totalChapters: number;
  tableOfContents: ChapterTocItem[];
}

export interface ChapterTocItem {
  chapterNumber: number;
  title: string;
  sections: SectionTocItem[];
}

export interface SectionTocItem {
  sectionNumber: string;
  title: string;
}

export interface TextbookMetadata {
  textbookId: string;
  title: string;
  description: string;
  status: TextbookStatus;
  createdAt: string;
  updatedAt: string;
  totalChapters: number;
  targetAudience: string;
  contentDepth: string;
  writingStyle: string;
  estimatedPages: number;
  exportFormats: string[];
  wordCount: number;
}

// WebSocket message interface for progress updates
export interface ProgressMessage {
  textbookId: string;
  status: string;
  progress: number;
  message: string;
  updatedAt: string;
}
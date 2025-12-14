<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Added sections: All principles and sections based on the AI-Native Textbook project
Removed sections: None (new constitution)
Modified principles: N/A (new constitution)
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# AI-Native Textbook for Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. AI-Native Education First
Every feature serves the mission of creating an intelligent, interactive textbook. All components must enhance the educational experience through AI capabilities, ensuring the platform feels like a real AI-powered education tool rather than a static book.

### II. Fast, Simple, Beautiful Design
The user interface must be clean, fast-loading, and mobile-friendly. All design decisions prioritize user experience with minimal, purposeful interactions. Complexity must be justified by clear user benefit.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. All features must be validated through automated tests before release.

### IV. Modular Architecture
Backend components must be modular (RAG + services + routes). Use clean folder structure with distinct separation: /backend, /website, /rag, /ingest, /agents. Components must be independently deployable and testable.

### V. Grounded AI Responses
All AI responses must be accurate, cited, and grounded in the textbook content. RAG systems must provide clear provenance for all answers, ensuring educational integrity and trustworthiness.

### VI. Accessible by Design
The platform must work on free tiers (Qdrant + Neon), support low-end devices, and provide one-click Urdu translation for global accessibility. All features must be deployable within 90 seconds for demonstration purposes.

## Technical Constraints

All data must be stored clearly in Neon + Qdrant databases. The system must avoid complexity and heavy dependencies. Deployment must be seamless across: Frontend on Vercel, Backend on Railway, Vector DB on Qdrant, and Database on Neon.

## Development Workflow

Focus on 6-8 short, clean, modern chapters with functional RAG chatbot, user authentication using Better-Auth, personalized content, auto-generated summaries/quizzes, and one-click Urdu translation. Prioritize user stories in order: textbook readability, chatbot functionality, personalization, translation, and assessment tools.

## Governance

All implementations must align with the mission of building a fully AI-native, interactive, intelligent textbook. Features must be fast, simple, beautiful, and feel like a REAL AI-powered education platform. Changes to core principles require explicit project stakeholder approval and must maintain the non-goal constraints: no unnecessary animations, no overly long chapters, no complex robotics code beyond educational content.

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
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
Every feature serves the mission of creating an intelligent, interactive textbook. All components must enhance the educational experience through AI capabilities, ensuring the platform feels like a real AI-powered education tool rather than a static book. All features must be fast, simple, beautiful, and feel like a REAL AI-powered education platform.

### II. Fast, Simple, Beautiful Design
The user interface must be clean, fast-loading, and mobile-friendly. All design decisions prioritize user experience with minimal, purposeful interactions. Complexity must be justified by clear user benefit. No extra animations beyond minimal useful motion. No overly long chapters (short + clear only).

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. All features must be validated through automated tests before release. Each user story/journey must be independently testable - meaning if you implement just ONE of them, you should still have a viable MVP that delivers value.

### IV. Modular Architecture
Backend components must be modular (RAG + services + routes). Use clean folder structure with distinct separation: /backend, /website, /rag, /ingest, /agents. Components must be independently deployable and testable. All data must be stored clearly in Neon + Qdrant databases.

### V. Grounded AI Responses
All AI responses must be accurate, cited, and grounded in the textbook content. RAG systems must provide clear provenance for all answers, ensuring educational integrity and trustworthiness. The RAG chatbot must answer questions ONLY from the book content.

### VI. Accessible by Design
The platform must work on free tiers (Qdrant + Neon), support low-end devices, and provide one-click Urdu translation for global accessibility. All features must be deployable within 90 seconds for demonstration purposes. Must support low-end devices (users reading on phones). Must avoid complexity and heavy dependencies.

## Technical Constraints

All data must be stored clearly in Neon + Qdrant databases. The system must avoid complexity and heavy dependencies. Deployment must be seamless across: Frontend on Vercel, Backend on Railway, Vector DB on Qdrant, and Database on Neon. Must work on free tiers (Qdrant + Neon).

## Development Workflow

Focus on 6-8 short, clean, modern chapters with functional RAG chatbot, user authentication using Better-Auth, personalized content based on user background, auto-generated summaries/quizzes, and one-click Urdu translation. Prioritize user stories in order: textbook readability, chatbot functionality, personalization, translation, and assessment tools.

The product must be fast, simple, beautiful, and feel like a REAL AI-powered education platform — not just a book. The book must be readable in < 45 minutes total. Personalization must visibly improve text. Urdu translation must be high-quality and fast.

## Governance

All implementations must align with the mission of building a fully AI-native, interactive, intelligent textbook. Features must be fast, simple, beautiful, and feel like a REAL AI-powered education platform. Changes to core principles require explicit project stakeholder approval and must maintain the non-goal constraints: no unnecessary animations, no overly long chapters, no complex robotics code beyond educational content.

All implementations must follow the Spec-Driven Development workflow with proper documentation in spec.md, plan.md, and tasks.md files. Each user story must have measurable acceptance criteria and be independently testable. The system must be fully deployed with stable URLs for frontend (Vercel), backend (Railway), vector DB (Qdrant), and database (Neon).

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
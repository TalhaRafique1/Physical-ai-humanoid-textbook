---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-09
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Claude Code
command: /sp.constitution
labels: ["constitution", "spec", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

/spec.constitution

# Project Constitution: AI-Native Textbook for Physical AI & Humanoid Robotics

## 1. Mission
Build a fully AI-native, interactive, intelligent textbook that teaches the Physical AI & Humanoid Robotics course.
The product must be fast, simple, beautiful, and feel like a REAL AI-powered education platform — not just a book.

## 2. Core Deliverables
1. A Docusaurus-based interactive textbook with 6–8 short, clean, modern chapters.
2. A functional RAG chatbot answering questions ONLY from the book.
3. User authentication (signup/login) using Better-Auth.
4. Personalized chapter content based on user background.
5. One-click Urdu translation for every chapter.
6. Auto-generated summaries, quizzes, and learning boosters.

## 3. Success Criteria
- Clean UI, fast loading, mobile-friendly.
- Book readable in < 45 minutes total.
- RAG answers accurate, cited, and grounded.
- Personalization visibly improves text.
- Urdu translation high-quality and fast.
- Fully deployed.
  - Frontend — Vercel
  - Backend — Railway
  - Vector DB — Qdrant
  - Database — Neon

## 4. Non-Goals
- No extra animations beyond minimal useful motion.
- No overly long chapters (short + clear only).
- No complex robotics code — only education content.

## 5. Architecture Principles
- Keep frontend extremely simple, readable.
- Keep backend modular (RAG + services + routes).
- All data must be stored clearly in Neon + Qdrant.
- Use clean folder structure:
  /backend
  /website
  /rag
  /ingest
  /agents
- Use reusable agent skills for bonus scoring.

## 6. User Stories (Prioritized)
1. As a learner, I want to read the textbook smoothly.
2. As a learner, I want to ask the chatbot questions.
3. As a learner, I want personalized content based on my background.
4. As a learner, I want Urdu translation.
5. As a learner, I want summaries + quizzes.
6. As an admin, I want clean architecture and deployment.

## 7. Constraints
- Must work on free tiers (Qdrant + Neon).
- Must deploy within 90 seconds demo recording.
- Must support low-end devices (users reading on phones).
- Must avoid complexity and heavy dependencies.

## 8. Risks & Mitigation
- RAG low accuracy → use chunking + MiniLM embeddings.
- Token usage high → implement in phases.
- User confusion → keep UI minimal and clean.
- Backend errors → add health checks + logging.

## 9. Definition of Done
- All chapters visible and readable.
- Chatbot fully functional with grounded answers.
- Auth + personalization + translation working.
- Quizzes + summaries per chapter generated.
- Fully deployed URLs live and stable.
- 90-second demo recorded.

## Response snapshot

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

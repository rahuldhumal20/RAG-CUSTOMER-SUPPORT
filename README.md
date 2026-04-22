# RAG-Based Customer Support Assistant

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system with:
- LangGraph workflow
- ChromaDB vector store
- Groq LLM integration
- Human-in-the-Loop (HITL) escalation

## Features
- PDF-based knowledge retrieval
- Context-aware responses
- Intent + confidence routing
- Multi-turn conversation memory
- REST API using FastAPI

## Tech Stack
- Python
- FastAPI
- LangChain
- LangGraph
- ChromaDB
- Groq API

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app
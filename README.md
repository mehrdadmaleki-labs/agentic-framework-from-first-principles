# Agentic Framework from First Principles

A hands-on educational project exploring how to build distributed agentic systems from scratch, starting with fundamental networking concepts and progressively introducing modern distributed architectures, containerization, asynchronous communication, and AI agents.

## Project Objective

The goal is to understand the underlying principles of distributed agent systems rather than relying entirely on existing frameworks.

Each version builds on previous concepts, with its own source code, architecture, documentation, and practical examples.

## Development Roadmap

| Version | Topic | Key Concepts | Status |
|---|---|---|---|
| V1 | TCP Client-Server | Python sockets, TCP/IP, JSON serialization, request-response communication | Completed |
| V2 | Reliable TCP Communication | Message framing, timeouts, error handling | Planned |
| V3 | Concurrent Communication | Multithreading, asyncio, multiple clients | Planned |
| V4 | HTTP and REST APIs | HTTP, FastAPI, Pydantic | Planned |
| V5 | Containerization | Docker, images, containers, networking | Planned |
| V6 | Multi-Agent Framework | Agent architecture, tool registry, execution loops | Planned |
| V7 | Asynchronous Messaging | Message queues, event-driven communication | Planned |
| V8 | Durable Agent Execution | Persistent state, checkpointing, pause/resume | Planned |
| V9 | LLM Integration | Local LLMs, tool calling, planning | Planned |
| V10 | Kubernetes Deployment | Orchestration, scaling, fault tolerance | Planned |

## Repository Structure

```text
agentic-framework-from-first-principles/
│
├── README.md
│
├── agentic-framework-v1/
│   ├── README.md
│   ├── agent_a.py
│   └── agent_b.py
│
└── Future versions...
```

Each version is designed as an independent learning module.

## V1 — TCP Client-Server Communication

The first implementation consists of two independent Python programs:

- **Agent A (Client):** Sends calculation requests through a TCP socket and receives responses.
- **Agent B (Server):** Listens for incoming connections, processes arithmetic operations, and sends JSON responses.

### Architecture

```text
        Agent A (TCP Client)
                 |
                 | JSON request
                 | TCP / 127.0.0.1:9000
                 v
        Agent B (TCP Server)
                 |
                 v
        Arithmetic Operation
                 |
                 | JSON response
                 v
               Agent A
```

The implementation supports addition, subtraction, multiplication, and division, along with basic error handling.

**[Explore V1 — TCP Client-Server](agentic-framework-v1/)**

## Learning Philosophy

This project follows a first-principles approach:

1. Understand the fundamental problem.
2. Implement a minimal working solution.
3. Explore its limitations.
4. Introduce new architectural concepts to address those limitations.
5. Document each implementation and its design decisions.

The objective is to develop a deeper understanding of how distributed applications and agentic frameworks operate internally.

## Technologies

The project begins with Python's standard library and will progressively explore:

- Python and TCP/IP sockets
- HTTP, REST APIs, and FastAPI
- Docker and Docker Compose
- Asynchronous programming and message queues
- Persistent storage and workflow orchestration
- Local large language models
- Kubernetes and distributed deployment

## Project Status

**Current version: V1 — TCP Client-Server**

This repository is under active educational development. Each subsequent version will introduce new concepts and architectural improvements.

## License

To be determined.
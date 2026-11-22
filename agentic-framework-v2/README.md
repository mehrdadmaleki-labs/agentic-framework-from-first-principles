# V2 — Reliable TCP Communication

This version improves the TCP client-server implementation from V1 by introducing **message framing, structured error handling, and connection management**.

## Architecture

```text
Agent A (TCP Client)
        |
        | JSON Request + "\n"
        v
    TCP Connection
        |
        v
Agent B (TCP Server)
        |
        | Receive chunks using recv()
        | Accumulate bytes in a buffer
        | Detect "\n" (end of message)
        | Decode and deserialize JSON
        | Execute arithmetic operation
        v
    JSON Response + "\n"
        |
        v
Agent A
```

## What's New in V2?

| Feature | V1 | V2 |
|---|---|---|
| Message reception | Single `recv(1024)` | Loop until `\n` |
| Message framing | None | Newline-delimited JSON |
| Connection cleanup | Manual | `with conn:` |
| Error handling | Arithmetic errors | Arithmetic, JSON and connection errors |
| Response structure | Structured JSON | Structured JSON with newline delimiter |

## Key Concept: TCP Message Framing

TCP transports a continuous stream of bytes, not individual messages.

One `sendall()` does not guarantee that the receiver gets the entire message in a single `recv()`.

V2 uses newline-delimited JSON:

```python
message = json.dumps(data) + "\n"
```

The receiver accumulates bytes until it finds `b"\n"`, indicating a complete message.

## Running the Project

Start Agent B first:

```bash
python agent_b.py
```

Then, in another terminal:

```bash
python agent_a.py
```

Example request:

```json
{"x": 5, "y": 70, "op": "MULTIPLY"}
```

Expected response:

```json
{"status": "success", "message": 350}
```

## Current Limitations

- The server handles one client at a time.
- Socket timeouts are not yet implemented.
- Incoming message sizes are not limited.
- The server processes one request per connection.

## Next Steps

Introduce socket timeouts, message-size limits, and concurrent client handling.
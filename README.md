# AI-Powered Socket Chatroom

A multithreaded terminal-based chatroom built with Python sockets and integrated with Google's Gemini AI.

Users can communicate in real time, send private messages, customize chat colors, and interact with an AI assistant directly inside the chatroom using commands.

---

# Features

- Real-time socket-based chatroom
- Multi-client support using threading
- Gemini AI integration
- Private messaging
- Reply system
- Online member tracking
- Colored usernames and messages
- Command-based interaction
- Timestamped messages
- Terminal-based interface

---

# Tech Stack

- Python
- Socket Programming
- Multithreading
- Google Gemini API
- dotenv
- Regular Expressions

---

# AI Integration

The chatroom includes built-in Gemini AI support.

Users can ask questions directly inside the chat using:

```text
/ai your question here
```

Example:

```text
/ai explain black holes simply
```

The server sends the prompt to Gemini and returns the AI-generated response back to the client.

---

# Project Structure

```text
socket-chatroom/
├── server.py
├── .env
├── requirements.txt
├── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/iamindra07/socket-chatroom-python.git
cd socket-chatroom-python
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

---

# Run The Server

```bash
python server.py
```

The server will start listening on:

```text
127.0.0.1:12345
```

---

# Available Commands

## General Commands

| Command | Description |
|---|---|
| `/help` | Show all available commands |
| `/online` | Display online members |
| `/quit` | Leave the chat |

---

## AI Commands

| Command | Description |
|---|---|
| `/ai question` | Ask Gemini AI a question |

Example:

```text
/ai what is machine learning?
```

---

## Messaging Commands

| Command | Description |
|---|---|
| `@username:message` | Reply to a user publicly |
| `p@username:message` | Send private message |

Examples:

```text
@john:hello
```

```text
p@john:this is private
```

---

## Color Commands

### Message Colors

| Command | Description |
|---|---|
| `/red` | Send red text |
| `/green` | Send green text |
| `/blue` | Send blue text |

Example:

```text
/red hello everyone
```

---

### Username Colors

| Command | Description |
|---|---|
| `/setcR` | Set username color to red |
| `/setcG` | Set username color to green |
| `/setcB` | Set username color to blue |
| `/resetc` | Reset username color |

---

# Concepts Used

- TCP socket programming
- Multithreading
- Client-server architecture
- Real-time communication
- Environment variables
- API integration
- Command parsing
- ANSI terminal colors

---

# Future Improvements

- GUI interface
- End-to-end encryption
- Chat history storage
- Voice chat
- File sharing
- AI memory support
- Local LLM support using Ollama
- User authentication
- WebSocket implementation
- FastAPI integration

---

# Author

Indranil Majumder

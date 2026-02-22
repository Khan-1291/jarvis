# jarvis# jarvis
# Moon Assistant (formerly JARVIS)

**Moon** is a modern, personal desktop AI assistant built in Python, designed to feel like a smart, chill companion on your Windows machine.

It combines:
- Voice & text input
- Groq-powered LLM responses (fast & capable models)
- Long-term memory (persistent facts & conversation history)
- Desktop automation skills (open apps, browser control, media, reminders, etc.)
- A sleek, animated face UI with chat history

The project is under active development — currently focused on making it more personal, reliable and fun to talk to.

### Current Features

- **Voice & Text Interaction**
  - Speech-to-Text (local)
  - Text-to-Speech (Microsoft Edge voice)
  - Text input fallback

- **LLM Backend**
  - Groq API (auto-selects best available model)
  - Long context + memory-aware prompting
  - Natural, warm, slightly playful personality

- **Long-term Memory**
  - SQLite-based persistent storage
  - Remembers name, likes, hobbies, favorites, location, birthday...
  - Appends to lists automatically (likes, hobbies, etc.)
  - Recent conversation history in prompts

- **Skills / Commands** (routed before LLM fallback)
  - Open/close applications
  - Browser & YouTube automation
  - File management
  - Media control (Spotify, system volume)
  - Reminders
  - WhatsApp messaging
  - System controls (shutdown, sleep, etc.)
  - Aircraft-related fun commands (custom skill)
  - More skills can be easily added

- **UI**
  - Modern PySide6 window
  - Animated face that reacts (planned improvements)
  - Chat history with sender tags
  - Start/stop voice listening button

### Project Structure (main folders)

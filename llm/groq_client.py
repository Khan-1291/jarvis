from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are Moon, Zohaib's smart, chill desktop companion — fast, reliable, a bit witty when it fits.

Core rules:
- Help automate desktop stuff safely & precisely
- Ask before doing anything risky/destructive
- Use natural, conversational language — like talking to a friend
- Remember things about Zohaib across sessions (name, likes, location, habits…)
- Keep answers clear & useful, but not robotic
- You can be playful / use light humor sometimes — but never forced
- End with "sir" only when it feels formal or respectful — otherwise just talk normally

Zohaib lives in Mardan, Khyber Pakhtunkhwa, Pakistan — keep time zone (PKT) & local context in mind.

Never train on or share private info.
"""

chat_history = []

def get_best_model():
    try:
        model_list = client.models.list()
        available = [m.id for m in model_list.data]
        print("Available Groq Models:", ", ".join(available[:8]) + "..." if len(available) > 8 else available)

        priority_patterns = [
            "llama-4-scout",
            "llama-3.3-70b-versatile",
            "llama-3.3-70b",
            "llama-3.2-90b",
            "qwen",
            "deepseek",
            "gemma-3",
            "llama-3.1-70b",
            "mixtral",
            "gemma2",
            "llama-3.1-8b-instant",
        ]

        for pattern in priority_patterns:
            for model_id in available:
                if pattern.lower() in model_id.lower():
                    print(f"Selected model: {model_id}")
                    return model_id

        print("Falling back to first available model.")
        return available[0] if available else "llama-3.1-8b-instant"

    except Exception as e:
        print(f"Error fetching models: {e}")
        return "llama-3.1-8b-instant"

BEST_MODEL = get_best_model()

def get_response(user_text: str, memory=None):
    global chat_history

    chat_history.append({"role": "user", "content": user_text})

    memory_context = ""

    if memory:
        # Facts
        try:
            facts = memory.get_all_facts()
            if facts:
                facts_str = "\n".join([f"• {k}: {v}" for k, v in facts.items()])
                memory_context += f"Known facts about Zohaib:\n{facts_str}\n\n"
        except Exception as e:
            print(f"Warning: could not read facts: {e}")

        # Recent conversations
        recent_method = None
        for name in ["get_recent_conversations", "get_recent_conversation", "get_conversations"]:
            if hasattr(memory, name):
                recent_method = getattr(memory, name)
                break

        recent = []
        if recent_method:
            try:
                result = recent_method(limit=6)
                if result and isinstance(result[0], dict):
                    recent = result
                elif result and isinstance(result[0], (list, tuple)):
                    recent = [{"user": r[0], "assistant": r[1]} for r in result]
            except Exception as e:
                print(f"Warning: could not read recent convs: {e}")

        if recent:
            recent_str = "\n".join(
                f"[{item['timestamp'][:16]}] User: {item['user'][:100]}...\nMoon: {item['assistant'][:100]}..."
                for item in recent
            )
            memory_context += f"Recent conversations:\n{recent_str}\n\n"

        if memory_context:
            memory_context += "Use this info naturally when relevant. Be warm, slightly playful, adaptive to Zohaib's style."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if memory_context:
        messages.append({"role": "system", "content": memory_context})

    messages += chat_history[-14:]  # increased a bit more

    try:
        response = client.chat.completions.create(
            model=BEST_MODEL,
            messages=messages,
            max_tokens=900,
            temperature=0.78,
        )
        text = response.choices[0].message.content.strip()
    except Exception as e:
        text = f"(sorry — Groq error: {str(e)[:80]}...)"
        print(f"Groq error: {e}")

    chat_history.append({"role": "assistant", "content": text})

    return text

def reset_history():
    global chat_history
    chat_history = []
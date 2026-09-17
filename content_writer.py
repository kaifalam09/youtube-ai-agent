"""
Uses Claude to generate a script (if not provided), a catchy title,
and a YouTube description with relevant hashtags.
"""
import json
import anthropic
import config


def _client():
    if not config.ANTHROPIC_API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not set. Add it to your .env file."
        )
    return anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def generate_script(topic: str, max_seconds: int = config.MAX_VIDEO_SECONDS) -> str:
    """Turn a topic into a short narration script that fits the time limit."""
    # Roughly 2.5 words per second of natural speech
    max_words = int(max_seconds * 2.3)

    client = _client()
    prompt = (
        f"Write a short, punchy narration script for a YouTube Short about: "
        f"'{topic}'. Maximum {max_words} words. No stage directions, "
        f"no headers, just the spoken narration text. Make it engaging "
        f"with a hook in the first sentence."
    )
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


def generate_title_and_description(script: str, topic: str) -> dict:
    """Ask Claude for a JSON object with 'title' and 'description'."""
    client = _client()
    prompt = (
        "You are writing YouTube metadata for a Short. Given the script "
        f"below, return ONLY a JSON object (no markdown, no preamble) with "
        f"keys 'title' (under 70 characters, catchy, no clickbait lies) and "
        f"'description' (2-3 sentences plus 3-5 relevant hashtags).\n\n"
        f"Topic: {topic}\n\nScript:\n{script}"
    )
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Fallback if the model wraps it in extra text
        data = {"title": topic[:70], "description": script[:200]}
    return data

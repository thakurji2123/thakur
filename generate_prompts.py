# generate_prompts.py
import os
import sys
import google.generativeai as genai
import json

# GitHub Secrets se API Key legi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ Gemini API Key missing!")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.6-flash')

TOPICS_FILE = "topics.txt"
PROMPTS_FILE = "prompts.txt"
META_FILE = "metadata.json"

def main():
    if not os.path.exists(TOPICS_FILE):
        print("❌ topics.txt not found!")
        sys.exit(1)

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f.readlines() if line.strip()]

    if not topics:
        print("❌ No topics left in topics.txt!")
        sys.exit(1)

    # Pehla topic uthao
    current_topic = topics[0]
    print(f"🚀 Generating script for topic: {current_topic}")

    # 1. GENERATE PROMPTS (Images + Voiceover)
    system_prompt = f"""
    You are a professional Christian/Educational YouTube scriptwriter. 
    Topic: "{current_topic}".
    Create exactly 100 scenes for a video.
    Strict Format: Image Description | Voiceover text
    Do not add numbers, markdown, intros, or blank lines. Just the exact format.
    Example:
    Jesus walking in Jerusalem, cinematic lighting, 16:9 | God has a plan for your life today.
    """
    
    response = model.generate_content(system_prompt)
    prompts_text = response.text.strip()

    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        f.write(prompts_text)
    print("✅ prompts.txt successfully created!")

    # 2. GENERATE VIRAL YOUTUBE METADATA
    meta_prompt = f"""
    Topic: "{current_topic}".
    Generate a viral YouTube Title (max 60 chars), Description, and Tags (comma separated) for a US Christian audience.
    Return strictly in JSON format like this:
    {{"title": "Title Here", "description": "Desc Here", "tags": "tag1, tag2, tag3"}}
    """
    meta_response = model.generate_content(meta_prompt)
    meta_json_str = meta_response.text.replace("```json", "").replace("```", "").strip()
    
    with open(META_FILE, "w", encoding="utf-8") as f:
        f.write(meta_json_str)
    print("✅ metadata.json successfully created!")

    # 3. UPDATE TOPICS.TXT (Delete used topic)
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        for topic in topics[1:]:
            f.write(topic + "\n")
    print(f"🗑️ Topic '{current_topic}' removed from topics.txt")

if __name__ == "__main__":
    main()

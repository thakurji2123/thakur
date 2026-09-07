import os
import random
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

VIDEO_FILE = "Final_Long_Educational_Video.mp4"
CATEGORY_ID = "22" # 22 is 'People & Blogs' (Best for Religious/Story channels)

# ==========================================
# 🎲 USA CHRISTIAN UNIQUE TITLE/DESC GENERATOR
# ==========================================

def generate_unique_metadata():
    hooks = ["A Message From God", "Jesus Says", "A Miracle Happened", "Words of Jesus", "God is Watching", "A Powerful Bible Story"]
    topics = ["Do Not Give Up", "The Power of Faith", "Overcoming Fear", "God's Love For You", "Finding Peace", "A Lesson for Your Soul"]
    emojis = ["✝️", "🙏", "🕊️", "✨", "❤️", "⛪"]

    # Generates: "A Message From God - The Power of Faith 🙏"
    unique_title = f"{random.choice(hooks)} - {random.choice(topics)} {random.choice(emojis)}"

    desc_intros = [
        "Welcome! If you found this video, it is not an accident. God led you here.", 
        "Take a moment to listen to this beautiful story of Jesus Christ.", 
        "May this message bring peace and blessings to your life today."
    ]
    desc_ctas = [
        "\n\nIf you believe in God, hit the LIKE button and SUBSCRIBE for daily blessings! 🙏", 
        "\n\nPlease SHARE this message with someone who needs it, and SUBSCRIBE to our channel! ✝️"
    ]
    tags = "\n\n#Jesus #ChristianMotivation #Faith #BibleStory #God #Christianity #Pray"

    unique_description = f"{random.choice(desc_intros)} {random.choice(desc_ctas)} {tags}"
    
    return unique_title, unique_description

def upload_video():
    if not os.path.exists(VIDEO_FILE):
        return

    selected_title, selected_desc = generate_unique_metadata()
    print(f"📌 FINAL TITLE: {selected_title}")
    
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.upload'])
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "categoryId": CATEGORY_ID,
            "title": selected_title,
            "description": selected_desc,
            "tags": ["Jesus Christ", "Christian Motivation", "Bible Stories", "Faith", "God", "Pray", "USA"]
        },
        "status": {
            "privacyStatus": "public", 
            "selfDeclaredMadeForKids": False
        }
    }

    media_file = MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file)
    response = request.execute()
    print(f"✅ VIDEO SUCCESSFULLY UPLOADED! Link: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    upload_video()

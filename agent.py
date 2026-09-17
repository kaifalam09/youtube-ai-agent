"""
Orchestrates the pipeline: topic -> script -> video -> title/description -> upload.
Keeps track of the last generated video so the user can say
"upload last video" without regenerating everything.
"""
import content_writer
import video_generator
import youtube_uploader


class Agent:
    def __init__(self):
        self.last_video_path = None
        self.last_title = None
        self.last_description = None
        self.last_script = None

    def generate(self, topic_or_script: str, is_full_script: bool = False) -> dict:
        print("📝 Writing script...")
        script = topic_or_script if is_full_script else content_writer.generate_script(
            topic_or_script
        )
        print(f"Script:\n{script}\n")

        print("🎬 Rendering video (max 50s)...")
        video_path = video_generator.generate_video(script)
        print(f"✅ Video saved: {video_path}")

        print("✍️  Writing title & description...")
        meta = content_writer.generate_title_and_description(script, topic_or_script)

        self.last_video_path = video_path
        self.last_script = script
        self.last_title = meta.get("title", topic_or_script[:70])
        self.last_description = meta.get("description", "")

        print(f"Title: {self.last_title}")
        print(f"Description: {self.last_description}")

        return {
            "video_path": video_path,
            "title": self.last_title,
            "description": self.last_description,
            "script": script,
        }

    def upload(self, privacy_status: str = "private") -> str:
        if not self.last_video_path:
            raise RuntimeError("No video generated yet. Generate one first.")

        print(f"⬆️  Uploading to YouTube as '{privacy_status}'...")
        url = youtube_uploader.upload_video(
            video_path=self.last_video_path,
            title=self.last_title,
            description=self.last_description,
            privacy_status=privacy_status,
        )
        print(f"✅ Uploaded: {url}")
        return url

    def generate_and_upload(self, topic_or_script: str, is_full_script: bool = False,
                             privacy_status: str = "private") -> str:
        self.generate(topic_or_script, is_full_script=is_full_script)
        return self.upload(privacy_status=privacy_status)

    def set_title(self, title: str):
        self.last_title = title
        print(f"Title updated: {title}")

    def set_description(self, description: str):
        self.last_description = description
        print(f"Description updated: {description}")

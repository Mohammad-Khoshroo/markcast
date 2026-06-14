import asyncio
import os
from bs4 import BeautifulSoup
import markdown
import edge_tts

# Supported voices for the requested languages
VOICES = {
    "en": "en-US-AvaNeural",       # English (US) - Female
    "fa": "fa-IR-DilaraNeural",    # Persian (Iran) - Female
    "es": "es-ES-ElviraNeural",    # Spanish (Spain) - Female
    "ko": "ko-KR-SunHiNeural",     # Korean (South Korea) - Female
    "ar": "ar-AE-FatimaNeural"     # Arabic (UAE) - Female
}

def markdown_to_plain_text(markdown_text):
    """Converts markdown formatted text into clean plain text."""
    html = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

async def generate_voice(text, output_file_path, voice):
    """Sends the clean text to Edge TTS and saves it as an audio file."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file_path)

def read_markdown_file(file_path):
    """Reads the content of a markdown file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

if __name__ == "__main__":
    # Configuration
    input_file = "input.md"          # Path to your input markdown file
    output_audio = "output.mp3"      # Path to the output audio file
    language_code = "fa"             # Options: 'en', 'fa', 'es', 'ko', 'ar'

    try:
        # 1. Read markdown from file
        print(f"Reading '{input_file}'...")
        markdown_content = read_markdown_file(input_file)

        # 2. Clean the markdown syntax
        cleaned_text = markdown_to_plain_text(markdown_content)

        # 3. Get the corresponding voice
        selected_voice = VOICES.get(language_code)
        if not selected_voice:
            raise ValueError(f"Language code '{language_code}' is not supported.")

        # 4. Generate the audio file
        print(f"Generating audio using voice '{selected_voice}'...")
        asyncio.run(generate_voice(cleaned_text, output_audio, selected_voice))
        print(f"Success! Audio saved to '{output_audio}'")

    except Exception as e:
        print(f"Error: {e}")

import asyncio
import os
import re
from bs4 import BeautifulSoup
import markdown
import edge_tts

# Default primary voices for each language
PRIMARY_VOICES = {
    "en": "en-US-AvaNeural",
    "fa": "fa-IR-DilaraNeural",
    "es": "es-ES-ElviraNeural",
    "ko": "ko-KR-SunHiNeural",
    "ar": "ar-AE-FatimaNeural"
}

ENGLISH_VOICE = "en-US-AvaNeural"

def markdown_to_plain_text(markdown_text):
    """Converts markdown formatted text into clean plain text."""
    html_content = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

def has_speakable_content(text):
    """Checks if the text contains at least one alphanumeric character."""
    # Matches any Persian/Arabic letters, English letters, or digits
    return bool(re.search(r'[\u0600-\u06FFa-zA-Z0-9]', text))

def split_text_by_language(text, primary_lang):
    """
    Splits the text into segments of English and non-English (primary) parts.
    Filters out segments that don't contain any pronounceable character to avoid API errors.
    """
    if primary_lang != "fa":
        return [(text, PRIMARY_VOICES[primary_lang])] if has_speakable_content(text) else []

    # Regex to detect English parts (words, phrases, numbers, etc.)
    pattern = r'([a-zA-Z][a-zA-Z0-9\s\-_.,!?\'"]*[a-zA-Z0-9]|[a-zA-Z])'
    parts = re.split(pattern, text)
    
    segments = []
    primary_voice = PRIMARY_VOICES["fa"]

    for part in parts:
        if not part:
            continue
        
        # Avoid sending pure punctuation/spaces to TTS
        if not has_speakable_content(part):
            continue
            
        trimmed = part.strip()
        
        # Check if segment is English
        if re.match(r'^[a-zA-Z0-9\s\-_.,!?\'"]+$', trimmed) and any(c.isalpha() for c in trimmed):
            segments.append((trimmed, ENGLISH_VOICE))
        else:
            segments.append((part, primary_voice))
            
    return segments

async def generate_segment_audio(text, voice, output_path):
    """Generates audio for a single segment using standard Edge TTS."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def concatenate_mp3_files(file_list, final_output_path):
    """Concatenates multiple MP3 files into a single MP3 file."""
    with open(final_output_path, 'wb') as outfile:
        for file_path in file_list:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as infile:
                    outfile.write(infile.read())
                # Delete temporary file after merging
                os.remove(file_path)

async def main():
    input_file = "input.md"          # Input markdown
    output_audio = "output.mp3"      # Final output audio
    language_code = "fa"             # Base language

    try:
        # 1. Read Markdown
        print(f"Reading '{input_file}'...")
        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found!")
            return
        with open(input_file, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # 2. Convert MD to text
        cleaned_text = markdown_to_plain_text(markdown_content)

        # 3. Split into language-specific segments
        print("Analyzing text and splitting into language segments...")
        segments = split_text_by_language(cleaned_text, language_code)
        
        temp_files = []
        total_segments = len(segments)
        print(f"Processing {total_segments} valid segments...")

        # 4. Generate individual audio for each segment
        for idx, (seg_text, seg_voice) in enumerate(segments):
            temp_filename = f"temp_{idx}.mp3"
            # Display a clean preview of the segment text
            preview = seg_text.strip().replace('\n', ' ')
            print(f" -> [{idx+1}/{total_segments}] Generating audio for: '{preview[:30]}...' using {seg_voice}")
            await generate_segment_audio(seg_text, seg_voice, temp_filename)
            temp_files.append(temp_filename)

        # 5. Merge all files into final output
        if temp_files:
            print("Merging audio segments into final output...")
            concatenate_mp3_files(temp_files, output_audio)
            print(f"Success! Audio successfully saved to '{output_audio}' ({os.path.getsize(output_audio) // 1024} KB)")
        else:
            print("No speakable text found to generate audio.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

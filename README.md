# MARKCast 🎙️📝

`MARKCast` is a lightweight, multi-lingual Python tool that converts Markdown documents into high-quality, natural-sounding speech (MP3). 

It automatically parses and strips Markdown syntax (headers, bold text, lists, links, etc.) from an input file, cleans the text, and converts it into audio using advanced neural Text-to-Speech (TTS) engines.

## Features
- **File-Based Input**: Reads directly from any `.md` file.
- **Clean Markdown Parsing**: Removes Markdown formatting seamlessly before synthesis to ensure smooth and uninterrupted reading.
- **Multi-Lingual Support**: Ready-to-use premium neural voices for English, Persian (Farsi), Spanish, Korean, and Arabic.
- **Premium Neural Voices**: Uses high-quality, natural-sounding Microsoft neural voices.
- **Free & No API Key Required**: Fully functional without any paid cloud subscriptions or API keys.
- **Fast and Async**: Built on top of Python's `asyncio` for rapid and non-blocking audio generation.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/vox-markdown.git
cd vox-markdown

### 2. Install dependencies
bash
pip install edge-tts markdown beautifulsoup4

---

## Usage

1. Create a file named `input.md` in the same directory as the script and write your markdown content inside it.
2. Open `main.py` and set the `language_code` to your desired language:
   - `"en"` for English
   - `"fa"` for Persian
   - `"es"` for Spanish
   - `"ko"` for Korean
   - `"ar"` for Arabic
3. Run the script:

bash
python main.py

---

## Supported Languages & Voices

This project configured the following default premium voices:

| Language | Code | Default Voice | Gender |
| :--- | :---: | :--- | :--- |
| **English** | `en` | `en-US-AvaNeural` | Female |
| **Persian** | `fa` | `fa-IR-DilaraNeural` | Female |
| **Spanish** | `es` | `es-ES-ElviraNeural` | Female |
| **Korean** | `ko` | `ko-KR-SunHiNeural` | Female |
| **Arabic** | `ar` | `ar-AE-FatimaNeural` | Female |

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

# Text Encoding Converter

A simple and user-friendly tool for converting text file encodings, with support for multiple language interfaces.

![Demo Screenshot](https://via.placeholder.com/800x450.png?text=Text+Encoding+Converter+Demo)

## Features

- 🔍 **Automatic Encoding Detection**: Uses chardet to automatically identify file encoding and confidence level
- 🔄 **Manual Encoding Selection**: Supports multiple encoding formats with the option to manually select the most suitable one
- 👁️ **Content Preview**: Displays the first five lines of content before conversion
- 🌐 **UTF-8 Conversion**: Converts any encoding format to the universal UTF-8 encoding
- 📋 **Copy and Download**: One-click copying or downloading of converted text
- 🌏 **Multi-language Support**: Provides Traditional Chinese, Simplified Chinese, and English interfaces
- 🧠 **Smart Encoding Suggestions**: Recommends relevant encodings based on the user's chosen language

## Installation and Execution

### Requirements

- Python 3.7+
- Streamlit
- chardet

### Installation Steps

1. Clone the repository

```bash
git clone https://github.com/planetoid/text-encoding-converter.git
cd text-encoding-converter
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
streamlit run app.py
```

## Usage Instructions

1. After launching the application, select your preferred interface language in the sidebar
2. Click the "Choose a text file" button to upload the file you want to convert
3. Check the automatically detected encoding format and confidence level
4. If needed, manually select a different encoding format from the dropdown menu
5. Preview the first five lines of content to ensure correct display
6. Use the "Copy to clipboard" button to copy the converted content, or click "Download as UTF-8" to save the file

## Supported Encodings

The application supports various encoding formats, including but not limited to:

### Basic Encodings
- UTF-8, ASCII, Latin-1, ISO-8859-1/2
- Windows-1250/1251/1252/1253
- UTF-16, UTF-16-LE, UTF-16-BE

### Chinese Encodings
- Big5 (Traditional Chinese)
- GB2312, GBK, GB18030 (Simplified Chinese)

### Japanese Encodings
- EUC-JP, Shift-JIS, ISO-2022-JP

### Korean Encodings
- EUC-KR, CP949, ISO-2022-KR

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

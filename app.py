import streamlit as st
import io
import chardet
from typing import Tuple, Optional
import base64
import subprocess
import os

# 語言選擇與翻譯功能 / Language selection and translations
TRANSLATIONS = {
    "zh_TW": {  # 繁體中文
        "page_title": "文字檔案編碼轉換工具",
        "page_icon_text": "📝",
        "title": "文字檔案編碼轉換工具",
        "description": "上傳文字檔案，偵測其編碼並轉換為 UTF-8",
        "choose_file": "選擇文字檔案",
        "detected_encoding": "偵測到的編碼：**{}**（準確度：{:.2%}）",
        "select_encoding": "選擇編碼（自動偵測或手動選擇）",
        "preview_title": "預覽（前 5 行）：",
        "full_content": "查看完整內容",
        "content_label": "內容",
        "actions": "操作：",
        "copy_button": "複製到剪貼簿",
        "copied_success": "內容已複製到剪貼簿！您可以從上方框中全選並複製。",
        "download_as_utf8": "下載為 UTF-8",
        "download_caption": "下載為 {}",
        "error_decoding": "使用 {} 解碼時發生錯誤：{}"
    },
    "zh_CN": {  # 簡體中文
        "page_title": "文本文件编码转换工具",
        "page_icon_text": "📝",
        "title": "文本文件编码转换工具",
        "description": "上传文本文件，检测其编码并转换为 UTF-8",
        "choose_file": "选择文本文件",
        "detected_encoding": "检测到的编码：**{}**（准确度：{:.2%}）",
        "select_encoding": "选择编码（自动检测或手动选择）",
        "preview_title": "预览（前 5 行）：",
        "full_content": "查看完整内容",
        "content_label": "内容",
        "actions": "操作：",
        "copy_button": "复制到剪贴板",
        "copied_success": "内容已复制到剪贴板！您可以从上方框中全选并复制。",
        "download_as_utf8": "下载为 UTF-8",
        "download_caption": "下载为 {}",
        "error_decoding": "使用 {} 解码时发生错误：{}"
    },
    "ja": {  # 日本語
        "page_title": "テキストファイルエンコーディング変換ツール",
        "page_icon_text": "📝",
        "title": "テキストファイルエンコーディング変換ツール",
        "description": "テキストファイルをアップロードし、エンコーディングを検出してUTF-8に変換します",
        "choose_file": "テキストファイルを選択",
        "detected_encoding": "検出されたエンコーディング：**{}**（信頼度：{:.2%}）",
        "select_encoding": "エンコーディングを選択（自動検出または手動選択）",
        "preview_title": "プレビュー（最初の5行）：",
        "full_content": "全内容を表示",
        "content_label": "内容",
        "actions": "アクション：",
        "copy_button": "クリップボードにコピー",
        "copied_success": "内容がクリップボードにコピーされました！上のボックスから全選択してコピーできます。",
        "download_as_utf8": "UTF-8としてダウンロード",
        "download_caption": "{}としてダウンロード",
        "error_decoding": "{}でのデコード中にエラーが発生しました：{}"
    },
    "ko": {  # 한국어
        "page_title": "텍스트 파일 인코딩 변환 도구",
        "page_icon_text": "📝",
        "title": "텍스트 파일 인코딩 변환 도구",
        "description": "텍스트 파일을 업로드하여 인코딩을 감지하고 UTF-8로 변환합니다",
        "choose_file": "텍스트 파일 선택",
        "detected_encoding": "감지된 인코딩: **{}**(신뢰도: {:.2%})",
        "select_encoding": "인코딩 선택(자동 감지 또는 수동 선택)",
        "preview_title": "미리보기(처음 5줄):",
        "full_content": "전체 내용 보기",
        "content_label": "내용",
        "actions": "작업:",
        "copy_button": "클립보드에 복사",
        "copied_success": "내용이 클립보드에 복사되었습니다! 위 상자에서 모두 선택하여 복사할 수 있습니다.",
        "download_as_utf8": "UTF-8로 다운로드",
        "download_caption": "{}로 다운로드",
        "error_decoding": "{} 디코딩 중 오류 발생: {}"
    },
    "en": {  # 英文
        "page_title": "Text File Encoding Converter",
        "page_icon_text": "📝",
        "title": "Text File Encoding Converter",
        "description": "Upload a text file to detect its encoding and convert it to UTF-8",
        "choose_file": "Choose a text file",
        "detected_encoding": "Detected encoding: **{}** (Confidence: {:.2%})",
        "select_encoding": "Select encoding (auto-detected or choose manually)",
        "preview_title": "Preview (first 5 lines):",
        "full_content": "View full content",
        "content_label": "Content",
        "actions": "Actions:",
        "copy_button": "Copy to clipboard",
        "copied_success": "Content copied to clipboard! You can select all and copy from the box above.",
        "download_as_utf8": "Download as UTF-8",
        "download_caption": "Download as {}",
        "error_decoding": "Error decoding with {}: {}"
    }
}


def detect_encoding(file_content: bytes) -> Tuple[str, float]:
    """
    Detect the encoding of the file content.

    Args:
        file_content: The binary content of the file

    Returns:
        A tuple containing the detected encoding and confidence
    """
    result = chardet.detect(file_content)
    return result['encoding'], result['confidence']


def decode_content(file_content: bytes, encoding: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Decode file content using the specified encoding.

    Args:
        file_content: The binary content of the file
        encoding: The encoding to use for decoding

    Returns:
        A tuple containing the decoded text and any error message
    """
    try:
        return file_content.decode(encoding), None
    except UnicodeDecodeError as e:
        return None, f"Error decoding with {encoding}: {str(e)}"


def get_download_link(text: str, filename: str, link_text: str) -> str:
    """
    Generate a download link for the converted text.

    Args:
        text: The text to download
        filename: The name of the file to download
        link_text: The text to display for the download link

    Returns:
        HTML for a download link
    """
    b64 = base64.b64encode(text.encode('utf-8')).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" target="_blank">{link_text}</a>'
    return href


def get_git_revision_info():
    """
    Get the current git revision information (commit hash and date)

    Returns:
        A tuple containing (commit hash, commit date, is_repo) or None if not a git repository
    """
    try:
        # Check if we're in a git repository
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.STDOUT)

        # Get short commit hash
        commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()

        # Get commit date
        commit_date = subprocess.check_output(
            ["git", "log", "-1", "--format=%cd", "--date=short"]
        ).decode("utf-8").strip()

        return (commit_hash, commit_date, True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Not a git repository or git is not installed
        return (None, None, False)


def main():
    # 獲取 Git 版本信息 / Get Git version info
    commit_hash, commit_date, is_git_repo = get_git_revision_info()

    # 設置頁面配置 / Set page config
    app_version = f"v{commit_hash} ({commit_date})" if is_git_repo else "Dev"

    st.set_page_config(
        page_title="Text Encoding Converter",
        page_icon="📝",
        layout="wide"
    )

    # 語言選擇 / Language selection
    language = st.sidebar.selectbox(
        "語言 / Language",
        ["zh_TW", "zh_CN", "ja", "ko", "en"],
        format_func=lambda x: "繁體中文" if x == "zh_TW" else
        "简体中文" if x == "zh_CN" else
        "日本語" if x == "ja" else
        "한국어" if x == "ko" else
        "English"
    )

    # 獲取翻譯字典 / Get translations
    t = TRANSLATIONS[language]

    st.title(t["title"])
    st.write(t["description"])

    # 顯示 Git 版本信息 / Display Git version info
    if is_git_repo:
        st.sidebar.markdown(f"**Version:** {app_version}")

    uploaded_file = st.file_uploader(t["choose_file"])

    if uploaded_file is not None:
        # 讀取檔案內容 / Read the file content
        file_content = uploaded_file.getvalue()

        # 偵測編碼 / Detect encoding
        detected_encoding, confidence = detect_encoding(file_content)

        st.info(t["detected_encoding"].format(detected_encoding, confidence))

        # 基本編碼列表 / Basic encodings list
        basic_encodings = [
            "utf-8", "ascii", "latin-1", "iso-8859-1", "iso-8859-2",
            "windows-1250", "windows-1251", "windows-1252", "windows-1253",
            "utf-16", "utf-16-le", "utf-16-be"
        ]

        # 中文相關編碼 / Chinese-related encodings
        chinese_encodings = ["big5", "gbk", "gb2312", "gb18030"]

        # 日語相關編碼 / Japanese-related encodings
        japanese_encodings = ["euc-jp", "shift-jis", "iso-2022-jp"]

        # 韓語相關編碼 / Korean-related encodings
        korean_encodings = ["euc-kr", "cp949", "iso-2022-kr"]

        # 根據選擇的語言重新排序編碼列表 / Reorder encodings based on selected language
        if language == "zh_TW":
            # 繁體中文優先 / Traditional Chinese priority
            priority_encodings = ["big5", "utf-8"]
            common_encodings = priority_encodings + [e for e in basic_encodings if e not in priority_encodings] + \
                               [e for e in chinese_encodings if e not in priority_encodings] + \
                               japanese_encodings + korean_encodings
        elif language == "zh_CN":
            # 簡體中文優先 / Simplified Chinese priority
            priority_encodings = ["gb2312", "gbk", "gb18030", "utf-8"]
            common_encodings = priority_encodings + [e for e in basic_encodings if e not in priority_encodings] + \
                               [e for e in chinese_encodings if e not in priority_encodings] + \
                               japanese_encodings + korean_encodings
        elif language == "ja":
            # 日語優先 / Japanese priority
            priority_encodings = ["shift-jis", "euc-jp", "iso-2022-jp", "utf-8"]
            common_encodings = priority_encodings + [e for e in basic_encodings if e not in priority_encodings] + \
                               [e for e in japanese_encodings if e not in priority_encodings] + \
                               chinese_encodings + korean_encodings
        elif language == "ko":
            # 韓語優先 / Korean priority
            priority_encodings = ["euc-kr", "cp949", "iso-2022-kr", "utf-8"]
            common_encodings = priority_encodings + [e for e in basic_encodings if e not in priority_encodings] + \
                               [e for e in korean_encodings if e not in priority_encodings] + \
                               chinese_encodings + japanese_encodings
        else:
            # 英文介面，使用標準順序 / English interface, use standard order
            common_encodings = basic_encodings + chinese_encodings + japanese_encodings + korean_encodings

        # 如果偵測到的編碼不在編碼列表中，添加它 / If detected encoding is not in the encoding list, add it
        if detected_encoding and detected_encoding.lower() not in [enc.lower() for enc in common_encodings]:
            common_encodings.insert(0, detected_encoding)

        # 允許使用者選擇編碼 / Allow user to select encoding
        selected_encoding = st.selectbox(
            t["select_encoding"],
            common_encodings,
            index=common_encodings.index(detected_encoding) if detected_encoding in common_encodings else 0
        )

        # 嘗試使用選定的編碼解碼內容 / Try to decode the content with the selected encoding
        decoded_text, error = decode_content(file_content, selected_encoding)

        if error:
            st.error(t["error_decoding"].format(selected_encoding, error))
        else:
            # 顯示預覽（前5行） / Show preview (first 5 lines)
            st.subheader(t["preview_title"])
            preview_lines = decoded_text.splitlines()[:5]
            for line in preview_lines:
                st.text(line)

            # 在可展開的部分顯示完整內容 / Show full content in an expandable section
            with st.expander(t["full_content"]):
                st.text_area(t["content_label"], decoded_text, height=300)

            # 複製按鈕 / Copy button
            st.subheader(t["actions"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button(t["copy_button"]):
                    # 使用 JavaScript 複製到剪貼簿 / This uses JavaScript to copy to clipboard
                    st.code(decoded_text)
                    st.success(t["copied_success"])

            with col2:
                # 下載按鈕 / Download button
                output_filename = f"utf8_{uploaded_file.name}"
                download_link = get_download_link(decoded_text, output_filename, t["download_as_utf8"])
                st.markdown(download_link, unsafe_allow_html=True)
                st.caption(t["download_caption"].format(output_filename))


if __name__ == "__main__":
    main()
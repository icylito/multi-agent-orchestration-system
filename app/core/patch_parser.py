import re


def extract_file_blocks(text: str):
    pattern = r"--- FILE: (.*?) ---\n(.*?)--- END FILE ---"

    matches = re.findall(pattern, text, re.DOTALL)

    extracted = []

    for file_path, content in matches:
        extracted.append({
            "file": file_path.strip(),
            "content": content.strip()
        })

    return extracted

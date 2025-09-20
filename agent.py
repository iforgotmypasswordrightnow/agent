import requests
import re
import datetime
import difflib
import os

CONTEXT_FILE = "context.txt"
DART_FILE = "masterbuku_repository.dart"
LOG_FILE = "context_log.txt"
DIFF_DIR = "changes_logs"
BACK_DIR = "files_backup"
# --------------------------
# File & Logging Utilities
# --------------------------

def load_context():
    with open(CONTEXT_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def backup_file(content: str):
    if not os.path.exists(BACK_DIR):
        os.makedirs(BACK_DIR)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # backup_path = f"{DART_FILE}.{timestamp}.bak"
    backup_path = os.path.join(BACK_DIR, f"{DART_FILE}_{timestamp}.bak")
    with open(backup_path, "w") as bf:
        bf.write(content)
    return backup_path

def log_change(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def generate_diff(old_code: str, new_code: str):
    """Generate a unified diff between old and new code"""
    diff = difflib.unified_diff(
        old_code.splitlines(),
        new_code.splitlines(),
        fromfile="old/masterbuku_repository.dart",
        tofile="new/masterbuku_repository.dart",
        lineterm=""
    )
    return "\n".join(diff)

def save_diff_file(diff_text: str):
    """Save diff to a timestamped file inside diff_logs/"""
    if not os.path.exists(DIFF_DIR):
        os.makedirs(DIFF_DIR)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    diff_path = os.path.join(DIFF_DIR, f"diff_{timestamp}.patch")

    with open(diff_path, "w") as df:
        df.write("EOF >>\n")
        df.write(diff_text + "\n")
        df.write("EOF <<\n")

    return diff_path

# --------------------------
# AI Agent Functions
# --------------------------

def call_ai(user_prompt: str, file_content: str):
    """Send prompt + file to ApiFreeLLM"""
    context_lines = load_context()
    system_prompt = "\n".join(context_lines)

    url = "https://apifreellm.com/api/chat"
    payload = {
        "message": f"{system_prompt}\n\nHere is the Dart file content:\n{file_content}\n\nUser request: {user_prompt}\n\nReturn ONLY the updated Dart code wrapped in ```dart ... ```."
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Error from ApiFreeLLM: {response.status_code} {response.text}")

    data = response.json()
    return data.get("response", "")

def extract_code(raw_response: str):
    """Extract Dart code block from AI response"""
    match = re.search(r"```dart\n([\s\S]*?)```", raw_response)
    if not match:
        raise ValueError("No Dart code found in AI response")
    return match.group(1).strip()

def overwrite_dart_file(new_code: str):
    """Backup + overwrite the Dart file with diff logging"""
    with open(DART_FILE, "r") as f:
        old_code = f.read()

    # Backup old version
    backup_path = backup_file(old_code)

    # Create diff
    diff_text = generate_diff(old_code, new_code)

    # Overwrite file
    with open(DART_FILE, "w") as f:
        f.write(new_code)

    # Save diff separately
    if diff_text.strip():
        diff_path = save_diff_file(diff_text)
        log_change(f"File {DART_FILE} updated. Backup: {backup_path}, Diff saved: {diff_path}")
    else:
        log_change("No actual code changes detected (AI returned same content).")

    return f"✅ File updated! Backup saved at {backup_path}\n📜 Diff saved at {diff_path if diff_text.strip() else 'N/A'}"

# --------------------------
# Main Loop
# --------------------------

if __name__ == "__main__":
    with open(DART_FILE, "r") as f:
        current_code = f.read()

    user_prompt = input("Enter your refactor request: ")

    # Get AI response
    raw_response = call_ai(user_prompt, current_code)

    # Extract Dart code
    new_code = extract_code(raw_response)

    # Save changes & diff
    print(overwrite_dart_file(new_code))

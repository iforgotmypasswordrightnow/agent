import requests
import re
import datetime

CONTEXT_FILE = "context.txt"
DART_FILE = "masterbuku_repository.dart"
LOG_FILE = "context_log.txt"

# --------------------------
# File & Logging Utilities
# --------------------------

def load_context():
    with open(CONTEXT_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def backup_file(content: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = f"{DART_FILE}.{timestamp}.bak"
    with open(backup_path, "w") as bf:
        bf.write(content)
    return backup_path

def log_change(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

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
    """Backup + overwrite the Dart file"""
    with open(DART_FILE, "r") as f:
        old_code = f.read()

    backup_path = backup_file(old_code)

    with open(DART_FILE, "w") as f:
        f.write(new_code)

    log_change(f"File {DART_FILE} updated. Backup: {backup_path}")
    return f"✅ File updated! Backup saved at {backup_path}"

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

    # Save changes
    print(overwrite_dart_file(new_code))

# 🧑‍💻 AI Refactor Agent

This project provides an **AI-powered code refactoring agent** that automatically updates your codebase based on user prompts.  
The agent sends your file to an LLM (via [ApiFreeLLM](https://www.apifreellm.com/)), receives the refactored code, and safely overwrites your file with backups.

---

## 🚀 Features
- ✅ Reads your file (`masterbuku_repository.dart`)  
- ✅ Sends code + user prompt to an AI API  
- ✅ Extracts updated code from the response  
- ✅ Overwrites your file with **automatic backups**  
- ✅ Keeps a change log (`context_log.txt`)  
- ✅ Context-driven behavior (`context.txt`)  

---

## 📂 Project Structure Examples

```
.
├── agent.py                   # Main Python script
├── masterbuku_repository.# Your file to refactor
├── context.txt                # Defines agent rules (editable)
├── context_log.txt            # Logs file changes
```

---

## ⚙️ Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/ai-refactor-agent.git
   cd ai-refactor-agent
   ```

2. **Install dependencies**
   ```bash
   pip install requests
   ```

3. **Prepare your files**
   - Put your code in `masterbuku_repository.dart`
   - Write agent rules in `context.txt`, for example:
     ```
     You are a Dart/Flutter programming assistant.
     Always return valid code.
     Do not explain, only return the refactored file.
     Suggest improvements in efficiency, readability, and maintainability.
     ```

---

## ▶️ Example of Usage

Run the agent:

```bash
python agent.py
```

You will be prompted to enter your refactor request, e.g.:

```
Enter your refactor request: Refactor to use proper naming conventions
```

The agent will:
- Send your file + prompt to the AI
- Save a backup of the original file (`.bak`)
- Overwrite `masterbuku_repository.dart` with the new code
- Log the change in `context_log.txt`

---

## 🛡️ Safety

- Every run creates a **timestamped backup**:
  ```
  masterbuku_repository.dart.2025-09-20_09-04-30.bak
  ```
- Logs are appended to `context_log.txt` with timestamps.

---

## 🌟 Prompt Example

**Input Prompt:**
```
Refactor to follow clean architecture principles.
```

**Result:**
- `masterbuku_repository.dart` updated with AI-refactored code
- Backup + log automatically generated

---

## 📜 License
MIT License. Use at your own risk.

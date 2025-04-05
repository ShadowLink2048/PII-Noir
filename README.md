# 🕵️ PII Noir

**An educational detective game exploring PII (Personally Identifiable Information) protection and privacy, built in a stylish noir world.**

## 🎯 What Is It?

**PII Noir** is a narrative-driven, point-and-click detective game where you play as a privacy investigator in a world leaking secrets.  
Each case teaches real-life lessons about how data can be exposed, misused, or protected — all while solving dramatic mysteries.

---

## 🎮 Features

- 🕵️ Case-based investigations with interactive choices
- 📚 Educational privacy tips and lessons
- 🎭 Story-driven gameplay powered by external JSON files
- 🖼 Built in Pygame with optional backgrounds and music
- 💾 Extendable with SQLite (progress tracking, glossary)

---

## 🛠 Tech Stack

| Layer       | Tool        |
|-------------|-------------|
| Engine      | Python      |
| Framework   | Pygame      |
| Data        | JSON        |
| Storage     | SQLite (optional) |

---

## 📂 Folder Structure

```
pii_noir/
├── game/               # Python source files
│   └── main.py         # Game loop logic
├── data/               # Case files written by story team
│   └── case1.json
├── db/                 # (Optional) SQLite progress save
├── assets/             # Backgrounds, music, sound
├── README.md           # You’re reading it!
```

---

## 👥 Contributors

| Role                        | Name                  |
|-----------------------------|------------------------|
| Lead Developer / Coder      | Bryan Harris           |
| Backup Coder / Helper       | Katherine Rodli        |
| Story Writers               | Dominic H/T, Morgan O'Neil |
| Music / Research / Backup Writer | Omar Mallouk        |

---

## 🧪 Educational Goals

- Teach players what PII is and how it’s used
- Show risks of poor privacy hygiene (e.g. cookies, password leaks)
- Encourage critical thinking around data dilemmas
- Deliver this in a narrative game format that's actually fun

---

## 📦 How to Run

Make sure you have Python and Pygame installed.

```bash
pip install pygame
python game/main.py
```

---

# 🕵️ PII Noir - Interactive Investigation System

## 💡 Overview
PII Noir is a noir-style investigative game where players explore digital environments to uncover data privacy breaches and digital clues. Designed around a rich narrative, the gameplay guides users through a structured sequence of dialogue, investigations, and moral decisions.

---

## ✅ Features

### Game Functionality
- **Resizable Window Support**
- **Dynamic Text Wrapping and Layout Adjustments**
- **Story-Class Architecture:**
  - Encapsulated story logic
  - Supports multiple case files using a unified interface
- **Dialogue Engine:**
  - Dialogue defined using `dialogue.py` or external files
  - Sequential display via speaker + lines
- **Interactive Investigations:**
  - One setting at a time
  - Sequential and non-sequential interactables
  - All interactables must be viewed before progressing
  - Per-setting progression control
- **Choices & Outcomes:**
  - Multiple endings per story
  - "Privacy Tip" shown after choice is made

### UI/UX
- **Dynamic Buttons** with text wrapping and height adjustment
- **Back Navigation** from interactable view
- **Click or Key to Advance** mechanic across all screens other than the last screen you will need to hit enter to move to the last screen
- **Case Selector Menu** with dynamic listing

---

## 📅 Story File Requirements
All story files are placed in the `../data/` folder and must follow this JSON structure:

```json
{
  "title": "Gone Phishing",
  "intro": "Text to display as introduction.",
  "settings": [
    {
      "name": "Setting Name",
      "sequential": true,
      "interactables": [
        "You investigate... you find...",
        "You investigate... you find..."
      ]
    }
  ],
  "choices": [
    {
      "text": "Your choice description.",
      "result": "Outcome of that choice.",
      "tip": "Optional privacy tip."
    }
  ],
  "tip": "Fallback tip if not defined per choice.",
  "dialogue": ["c2_d0", "c2_d1"]
}
```

---

## 📑 File Structure

```
pii-noir/
│-- game/
│   │-- main.py
│   │-- story.py
│   │-- dialogue.py
│-- data/
│   │-- cookies_and_cache.json
│   │-- gone_phishing.json
│-- README.md
```

---

## 🌐 Adding a New Story
1. Write a new JSON file based on the format above.
2. Add it to the `../data/` folder.
3. Add any needed dialogue entries in `dialogue.py` under the appropriate ID.
4. Launch the game. The case will appear in the menu automatically.

---

## 📉 Future Features
- Scroll support for very long text
- Save/load system
- Sound/Music integration
- Dialogue from file (optional)

---

## 📖 Credits
Designed and developed during a 24-hour Hackathon. Inspired by noir mystery, digital safety, and interactive fiction.

---

## 📣 Hackathon: CougHacks 2025

Created in 24 hours to make data privacy fun, memorable, and interactive.


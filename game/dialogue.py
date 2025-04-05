# dialogue.py

# This dictionary stores the dialogue for each case.
# It uses case_id (matching the JSON filename) and dialogue IDs as keys.

dialogues = {
    "cookies_and_cache": {
        "c2_d0": {
            "speaker": "You",
            "lines": [
                "Dock 23... not the nicest part of town.",
                "But then again, neither am I."
            ]
        },
        "c2_d1": {
            "speaker": "Narrator",
            "lines": [
                "The sticky note practically screams 'I am the password.'",
                "Criminals are so confident, it’s almost charming."
            ]
        },
        "c2_d2": {
            "speaker": "You",
            "lines": [
                "Cookies still in the browser.",
                "Amateurs. I’m in their email and it’s worse than I thought."
            ]
        },
        "c2_d3": {
            "speaker": "Narrator",
            "lines": [
                "The more I dig, the more I realize —",
                "these guns never left the dock. Only the loyalty did."
            ]
        }
    }
}


def get_dialogue(case_id, dialogue_id):
    """
    Retrieve a dialogue entry for the given case and ID.
    Also fixes curly quotes to avoid text rendering issues.
    """
    case_id = case_id.lower().replace(" ", "_").replace("&", "and")
    case_dialogues = dialogues.get(case_id, {})
    entry = case_dialogues.get(dialogue_id)

    if entry:
        # Normalize curly quotes
        cleaned_lines = [line.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"') for line in entry["lines"]]
        return {
            "speaker": entry["speaker"],
            "lines": cleaned_lines
        }
    return None

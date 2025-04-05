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
        }
    }
}

def get_dialogue(case_id, dialogue_id):
    return dialogues.get(case_id, {}).get(dialogue_id)
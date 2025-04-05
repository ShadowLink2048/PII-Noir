# dialogue.py

# This dictionary stores the dialogue for each case.
# It uses case_id (matching the JSON filename) and dialogue IDs as keys.

dialogues = {
    "cookies_and_cache": {
        "c2_d0": {
            "speaker": "Narrator",
            "lines": [
                "As a private eye, you often get hired to look into things the police usually won’t.",
                "Like a missing shipment of guns from the DeadLock Crew.",
                "It appears from the sparse information you were given — as usual — that one of the local mobs doesn’t want the police involved.",
                "You should start your search where the shipment vanished.",
                "Looks like you’re visiting Dock 23."
            ]
        },
        "c2_d1": {
            "speaker": "Narrator",
            "lines": [
                "Outside the dock house, fog rolls in thick — San Francisco style.",
                "The streetlamp flickers. Something smells... fishy, and not just from the harbor.",
                "A locked door greets you. No welcome mat here.",
                "The dumpster nearby? Ripe with secrets and something sharp — a crowbar."
            ]
        },
        "c2_d2": {
            "speaker": "Narrator",
            "lines": [
                "Inside now, facing the main dock door.",
                "A shipping terminal glows dim in the dark — it wants a password.",
                "Good thing the sticky note stuck to the monitor makes cybercrime feel like child’s play: 'pass123'.",
                "You mutter, 'They really do put the organized in organized crime.'",
                "Nearby, the digital truck scale shows the last load left feather-light.",
                "Something’s not adding up. You head deeper."
            ]
        },
        "c2_d3": {
            "speaker": "Narrator",
            "lines": [
                "The hallway creaks under your boots. You swing around to the back half of the warehouse.",
                "One door’s labeled 'Office'.",
                "Time to knock with a lockpick."
            ]
        },
        "c2_d4": {
            "speaker": "Narrator",
            "lines": [
                "Inside the office, dust motes dance in a sliver of light.",
                "Filing cabinets are stuffed with tallies — a paper trail of guns incoming.",
                "On the desk, a photo with a handwritten date. Sentimental? Or sloppy?",
                "You use the date as the password. Jackpot — the computer unlocks, logged into someone’s email.",
                "Cookies still active. The inbox? Smoking hot.",
                "An email exchange reveals it all — the guy running shipments is turning coat.",
                "He’s selling the entire shipment — and the warehouse’s contents — to a rival gang.",
                "You sit back in the creaky chair, weighing the next step."
            ]
        }
    }
}
dialogues["gone_phishing"] = {
    "c2_d0": {
        "speaker": "Narrator",
        "lines": [
            "Another missing person.",
            "More and more people are vanishing in this city these days.",
            "I doubt this case is going anywhere, but it’s hard to tell a mother that she will most likely never see her child again."
        ]
    },
    "c2_d1": {
        "speaker": "You",
        "lines": [
            "Luckily, we’ve got a little more to start with than most.",
            "The mother was willing to let me into her daughter’s computer.",
            "Let's pray there’s some sort of lead to find in there."
        ]
    },
    "c2_d2": {
        "speaker": "Narrator",
        "lines": [
            "The desktop lights up with a glow that’s too clean for this kind of dirty work.",
            "Apps scattered, files renamed, but something’s off—too off."
        ]
    },
    "c2_d3": {
        "speaker": "You",
        "lines": [
            "Let’s dig through the inbox, check the social feed, and peek inside the trash.",
            "Somewhere in this digital mess is the key to where Hannah went—and who took her."
        ]
    }
}
dialogues["big_brother"] = {
"bb_d0": {
    "speaker": "Narrator",
    "lines": [
        "It was a Wednesday—the kind where the rain taps like a snitch with a secret. I was nursing cold coffee when she walked in. Maya Hernandez. Movie star. Trouble wrapped in lipstick and heels.",
        "She didn’t sit. She hovered, as if she didn’t trust the chair, or maybe just the situation."
    ]
},
"bb_d1": {
    "speaker": "Maya Hernandez",
    "lines": [
        "I received a letter—anonymous. It quoted something I said on the phone. Something I never said out loud to anyone else.",
        "Whoever it is... they knew where I was. What I said. What I fear."
    ]
},
"bb_d2": {
    "speaker": "Narrator",
    "lines": [
        "A blackmail attempt. But not your usual paper-cutout psychopath. This one had tech. Access. And maybe a uniform.",
        "I lit a fresh cigarette. Time to follow the wires and find the eye behind the glass."
    ]
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

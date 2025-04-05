import json

class Story:
    def __init__(self, story_id, data):
        self.story_id = story_id
        self.title = data.get("title", "Untitled")
        self.intro = data.get("intro") or data.get("overview", "No intro available.")
        self.settings = data.get("settings", [])
        self.choices = data.get("choices", [])
        self.dialogue_ids = data.get("dialogue", [])
        self.tip = data.get("tip", "")

    @classmethod
    def from_file(cls, filename, story_id):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(story_id, data)

    def get_case_id(self):
        return self.story_id

    def get_title(self):
        return self.title

    def get_intro(self):
        return self.intro

    def get_dialogue_ids(self):
        return self.dialogue_ids

    def get_setting_names(self):
        return [setting.get("name", "Unknown Area") for setting in self.settings]

    def get_settings(self):
        return self.settings

    def get_choices(self):
        return self.choices

    def get_tip(self):
        return self.tip

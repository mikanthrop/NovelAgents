import json
import os
import ResponseFormats

from datetime import datetime

class StoryGlossary:

    def __init__(self):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"brainstorming_{timestamp}.json"
        self.filename : str = filename
        print(f"{filename} has been set up.")
        self.data: ResponseFormats.StoryGlossary = ResponseFormats.StoryGlossary(title=None, theme=None, characters=[], plot=None, setting=None)
        self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = []
        else:
            self.data = []

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def set_title(self, title: str): 
        """
        Set the title in the story glossary json file. Always overwrites.
        """
        self.data.title = title
        self._save()

    def set_theme(self, theme: str): 
        """
        Set the theme in the story glossary json file. Always overwrites.
        """
        self.data.theme = theme
        self._save()

    def add_character(self, character: ResponseFormats.CharacterFormat):
        """
        Adds a character to the story glossary json file.
        """
        self.data.characters.append(character)
        self._save()
    
    def set_setting(self, setting: ResponseFormats.SettingFormat):
        """
        Set the setting in the story glossary json file. Always overwrites.
        """
        self.data.setting = setting
        self._save()

    def set_plot(self, plot: ResponseFormats.PlotFormat):
        """
        Set the plot in the story glossary json file. Always overwrites. 
        """
        self.data.plot = plot
        self._save()

    def delete(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"{self.filename} has been deleted.")
        else: 
            print(f"{self.filename} does not exist.")
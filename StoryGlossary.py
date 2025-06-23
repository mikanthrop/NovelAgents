import json
import os
import ResponseFormats

from datetime import datetime
from camel.storages import BaseKeyValueStorage

class StoryGlossary(BaseKeyValueStorage):
    '''
    Manages all data concerning the brainstorming session that get stored into memory.
    '''

    def __init__(self):
        """_summary_
        """        
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"brainstorming_{timestamp}.json"
        self.filename : str = filename
        print(f"{filename} has been set up.")
        self.data: ResponseFormats.StoryGlossary = ResponseFormats.StoryGlossary(title="", theme="", characters=[], plot=None, setting=None)
        self.load()

    def load(self):
        """_summary_

        Raises:
            ValueError: _description_
        """        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                    print(f"Loaded data: {self.data}")  # Debugging line
                    if not isinstance(self.data, dict):
                        raise ValueError("Loaded data is not a valid StoryGlossary format.")
                    self.data = ResponseFormats.StoryGlossary(**self.data)  
                    print(f"Data after conversion: {self.data}")  # Debugging line
            except (json.JSONDecodeError, ValueError):
                print("Error loading or invalid data format, initializing with default values.")
                self.data = ResponseFormats.StoryGlossary(title="", theme="", characters=[], plot=None, setting=None)
        else:
            self.data = ResponseFormats.StoryGlossary(title="", theme="", characters=[], plot=None, setting=None)

    def save(self):
        """_summary_
        """        
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)

    def to_dict(self):
        """_summary_

        Returns:
            _type_: _description_
        """        
        return {
            "title": self.data.title,
            "theme": self.data.theme,
            "characters": [character.to_dict() if hasattr(character, 'to_dict') else character for character in self.data.characters],
            "setting": self.data.setting.to_dict() if hasattr(self.data.setting, 'to_dict') else self.data.setting,
            "plot": self.data.plot.to_dict() if hasattr(self.data.plot, 'to_dict') else self.data.plot
        }
    
    def set_title(self, title: str): 
        """Set the title in the story glossary json file. Always overwrites.

        Args:
            title (str): _description_
        """        
        self.data.title = title

    def set_theme(self, theme: str): 
        """Set the theme in the story glossary json file. Always overwrites.

        Args:
            theme (str): _description_
        """        
        self.data.theme = theme

    def add_character(self, character: dict):
        """Adds a character json to the story glossary json file.

        Args:
            character (dict): _description_
        """        
        # Check if it's a valid character
        if isinstance(character, dict):  
            self.data.characters.append(character)

        else:
            print(f"Invalid character format: {character}")
    
    def set_setting(self, setting: dict):
        """Set the setting in the story glossary json file. Always overwrites.

        Args:
            setting (dict): _description_
        """        
        # Check if it's a valid setting
        if isinstance(setting, dict):
            self.data.setting = setting
        else:
            print(f"Invalid setting format: {setting}")

    def set_plot(self, plot: dict):
        """Set the plot in the story glossary json file. Always overwrites. 

        Args:
            plot (dict): _description_

        Raises:
            SavingIssueException: _description_
        """        
        # Check if it's a valid plot
        if isinstance(plot, dict):
            self.data.plot = plot
        else: 
            raise SavingIssueException()

    def clear(self):
        """_summary_
        """        
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"{self.filename} has been deleted.")
        else: 
            print(f"{self.filename} does not exist.")
import json
import os
import ResponseFormats
from datetime import datetime
from camel.storages import BaseKeyValueStorage

class StoryGlossary(BaseKeyValueStorage):
    """
    Manages all data concerning the brainstorming session that get stored into memory.
    """

    def __init__(self) -> None:
        """Initializes a new StoryGlossary instance.

        Creates a timestamped filename for storing the brainstorming session, 
        initializes the data structure for storing story information, and 
        attempts to load any existing data from the file.

        Attributes:
            filename (str): The JSON filename used for saving and loading the session.
            data (ResponseFormats.StoryGlossary): The in-memory representation of the story glossary.
        """       
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"brainstorming_{timestamp}.json"
        self.filename : str = filename
        print(f"{filename} has been set up.")
        self.data: ResponseFormats.StoryGlossary = ResponseFormats.StoryGlossary(
            title="", 
            theme="", 
            audience="", 
            genre="", 
            characters=[], 
            plot=None, 
            setting=None)
        self.load()

    def load(self) -> None:
        """Loads the StoryGlossary data from the JSON file into memory.

        If the file exists, attempts to parse it and convert it into a 
        StoryGlossary object. If the file does not exist 
        or the content is invalid, initializes the data with default empty values.

        Raises:
        ValueError: If the loaded data is not a valid StoryGlossary format.
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
                self.data = ResponseFormats.StoryGlossary(title="", theme="", audience="", genre="", characters=[], plot=None, setting=None)
        else:
            self.data = ResponseFormats.StoryGlossary(title="", theme="", audience="", genre="", characters=[], plot=None, setting=None)

    def save(self) -> None:
        """Saves the current StoryGlossary data to the JSON file.

        The method serializes the in-memory story data into a dictionary 
        and writes it to the file specified by `self.filename` in JSON format.
        """        
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)

    def to_dict(self) -> dict[str, object]:
        """Converts the in-memory StoryGlossary data into a dictionary.

        Handles nested Pydantic models (Character, Setting, Plot) by 
        calling their `to_dict()` methods if available.

        Returns:
            dict[str, object]: A dictionary representation of the StoryGlossary,
            ready for JSON serialization.
        """        
        return {
            "title": self.data.title,
            "theme": self.data.theme,
            "audience": self.data.audience,
            "genre": self.data.genre,
            "characters": [character.to_dict() if hasattr(character, 'to_dict') else character for character in self.data.characters],
            "setting": self.data.setting.to_dict() if hasattr(self.data.setting, 'to_dict') else self.data.setting,
            "plot": self.data.plot.to_dict() if hasattr(self.data.plot, 'to_dict') else self.data.plot
        }
    
    def set_title(self, title: str) -> None: 
        """Sets the title in the StoryGlossary. It always overwrites the existing title.

        Args:
            title (str): The new title to set for the story.
        """       
        self.data.title = title
    
    def get_title(self) -> str:
        """Returns the title of the story from the StoryGlossary.

        Returns:
            str: The current title stored in the story glossary.
        """
        return self.data.title

    def set_theme(self, theme: str) -> None: 
        """Sets the theme in the StoryGlossary. It overwrites any existing theme.

        Args:
            theme (str): The new theme to set for the story.
        """       
        self.data.theme = theme

    def get_theme(self) -> str:
        """Returns the theme of the story from the StoryGlossary.

        Returns:
            str: The current theme stored in the story glossary.
        """
        return self.data.theme

    def set_audience(self, audience: str) -> None: 
        """Sets the target audience in the StoryGlossary. It overwrites any existing audience information.

        Args:
            audience (str): The new target audience for the story (e.g., children, young adults, adults).
        """
        self.data.audience = audience

    def get_audience(self) -> str:
        """Returns the target audience of the story from the StoryGlossary.

        Returns:
            str: The current audience stored in the story glossary.
        """
        return self.data.audience

    def set_genre(self, genre: str) -> None:
        """Sets the genre in the StoryGlossary. It overwrites any existing genre.

        Args:
            genre (str): The new genre of the story (e.g., fantasy, sci-fi, mystery).
        """
        self.data.genre = genre
    
    def get_genre(self) -> str:
        """Returns the genre of the story from the StoryGlossary.

        Returns:
            str: The current genre stored in the story glossary.
        """
        return self.data.genre

    def add_character(self, character: dict) -> None:
        """Adds a character to the StoryGlossary.

        This method appends a character represented as a dictionary to the 
        `characters` list in the in-memory story glossary. Only dictionaries 
        are accepted; other types are ignored with a warning.

        Args:
            character (dict): A dictionary representing a character with relevant 
                attributes (e.g., name, age, looks, skills).
        """        
        # Check if it's a valid character
        if isinstance(character, dict):  
            self.data.characters.append(character)

        else:
            print(f"Invalid character format: {character}")
    
    def get_characters(self) -> dict:
        """Returns all characters from the StoryGlossary as a formatted JSON string.

        Each character dictionary is serialized to JSON and separated by two newlines.

        Returns:
            str: A string containing all characters in JSON format, nicely indented.
        """
        return "\n\n".join(json.dumps(c, indent=2) for c in self.data.characters)
    
    def set_setting(self, setting: dict) -> None:
        """Sets the story setting in the StoryGlossary.

        This method updates the `setting` attribute of the in-memory story glossary.
        It overwrites any existing setting. Only dictionaries are accepted; other types
        are ignored with a warning.

        Args:
            setting (dict): A dictionary representing the story setting, 
                including attributes like time, location, geography, and other details.
        """        
        # Check if it's a valid setting
        if isinstance(setting, dict):
            self.data.setting = setting
        else:
            print(f"Invalid setting format: {setting}")

    def get_setting(self) -> dict:
        """Returns the story setting from the StoryGlossary.

        Returns:
            dict: The current setting stored in the story glossary, typically 
            containing attributes like time, location, geography, and other details.
        """
        return self.data.setting

    def set_plot(self, plot: dict) -> None:
        """Sets the plot in the StoryGlossary.

        This method updates the `plot` attribute of the in-memory story glossary.
        It overwrites any existing plot. Only dictionaries are accepted; otherwise, 
        a `SavingIssueException` is raised.

        Args:
            plot (dict): A dictionary representing the story plot, including attributes 
                such as genre, blurb, outline, acts, and misc information.

        Raises:
            SavingIssueException: Raised if the provided plot is not a dictionary.
        """       
        # Check if it's a valid plot
        if isinstance(plot, dict):
            self.data.plot = plot
        else: 
            raise SavingIssueException()
        
    def get_plot(self) -> dict:
        """Returns the story plot from the StoryGlossary.

        Returns:
            dict: The current plot stored in the story glossary, typically containing
            attributes such as genre, blurb, outline, acts, and miscellaneous information.
        """
        return self.data.plot

    def clear(self) -> None:
        """
        Has to be implemented for fully inheriting from BaseKeyValueStorage.
        """        
        pass
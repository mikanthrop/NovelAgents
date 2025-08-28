from pydantic import BaseModel
from typing import List, Optional, Dict

class Character(BaseModel):
    """Character model. Inherits from Pydantic's BaseModel.

    Attributes:
        name (str): The character's name.
        age (int): The character's age.
        looks (str): A description of the character's appearance.
        sacred_flaw (str): The character's defining weakness or flaw.
        temperament (str): The character's general disposition or personality.
        backstory_events (list[str]): Significant past events in the character's life.
        motivation (str): The character's main drive or goal.
        relationships (list[str]): Relationships the character maintains with others.
        skills (list[str]): Skills or abilities the character possesses.
        misc_information (Optional[dict[str, str]]): Additional information 
            about the character, stored as key-value pairs.
    """  
    name: str
    age: int
    looks: str
    sacred_flaw: str
    temperament: str
    backstory_events: List[str]
    motivation: str
    relationships: List[str]
    skills: List[str]
    misc_information: Optional[Dict[str, str]]

    def to_dict(self):
        """Converts the instance into a dictionary representation.

        Returns:
            dict[str, object]: A dictionary containing the main attributes 
            of the instance, including name, age, looks, sacred flaw, 
            temperament, backstory events, motivation, relationships, 
            skills, and misc information.
        """        
        return {
            "name": self.name,
            "age": self.age,
            "looks": self.looks,
            "sacred_flaw": self.sacred_flaw,
            "temperament": self.temperament,
            "backstory_events": self.backstory_events,
            "motivation": self.motivation,
            "relationships": self.relationships,
            "skills": self.skills,
            "misc_information": self.misc_information
        }

class Plot(BaseModel):
    """Plot model. Inherits from Pydantic's BaseModel.

    Attributes:
        genre (str): The narrative genre of the plot (e.g., fantasy, sci-fi, mystery).
        blurb (str): A short teaser text or summary for the plot.
        overall_outline (str): The overall story outline from start to finish.
        main_conflict (str): The central conflict driving the story.
        act_one_outline (str): The outline of the first act.
        act_two_outline (str): The outline of the second act.
        act_three_outline (str): The outline of the third act.
        act_four_outline (str): The outline of the fourth act.
        act_five_outline (str): The outline of the fifth act.
        misc_information (Optional[dict[str, str]]): Additional metadata or notes 
            about the plot, stored as key-value pairs.
    """     
    genre: str
    blurb: str
    overall_outline: str
    main_conflict: str
    act_one_outline: str
    act_two_outline: str
    act_three_outline: str
    act_four_outline: str
    act_five_outline: str
    misc_information: Optional[Dict[str, str]]

    def to_dict(self):
        """Converts the Plot instance into a dictionary representation.

        Returns:
            dict[str, object]: A dictionary containing all plot attributes.
        """        
        return {
            "genre": self.genre,
            "blurb": self.blurb,
            "outline": self.overall_outline,
            "main_conflict": self.main_conflict,
            "act_one_outline": self.act_one_outline,
            "act_two_outline": self.act_two_outline,
            "act_three_outline": self.act_three_outline,
            "act_four_outline": self.act_four_outline,
            "act_five_outline": self.act_five_outline,
            "misc_information": self.misc_information
        }

class Setting(BaseModel):
    """Setting model. Inherits from Pydantic's BaseModel.

    Attributes:
        time (str): The historical or fictional time period of the setting.
        location (str): The primary location or world where the story takes place.
        geography (str): Description of the geographical landscape.
        ecology (Optional[str]): Information about flora, fauna, and ecosystems.
        historical_events (Optional[list[str]]): Significant past events that shaped the setting.
        cultural_customs (Optional[list[str]]): Traditions and rituals of the setting.
        cultural_structures (Optional[list[str]]): Social or political structures and hierarchies.
        social_dynamics (Optional[list[str]]): Interactions between groups, classes, or species.
        infrastructure (Optional[list[str]]): Buildings, roads, and general societal infrastructure.
        current_tension (Optional[list[str]]): Present-day conflicts or unresolved tensions.
        magic_system (str | dict[str, str] | None): Description of magic, or detailed 
            rules in a structured format.
        misc_information (Optional[dict[str, str]]): Additional key-value metadata about the setting.
    """    
    time: str
    location: str
    geography: str
    ecology: Optional[str]
    historical_events: Optional[List[str]]
    cultural_customs: Optional[List[str]]
    cultural_structures: Optional[List[str]]
    social_dynamics: Optional[List[str]]
    infrastructure: Optional[List[str]]
    current_tension: Optional[List[str]]
    magic_system: Optional[str] | Optional[Dict[str, str]]
    misc_information: Optional[Dict[str, str]]
    
    def to_dict(self):
        """Converts the Setting instance into a dictionary representation.

        Returns:
            dict[str, object]: A dictionary containing all attributes of the setting.
        """        
        return {
            "time": self.time,
            "location": self.location,
            "geography": self.geography,
            "ecology": self.ecology,
            "historical_events": self.historical_events,
            "cultural_customs": self.cultural_customs,
            "cultural_structures": self.cultural_structures,
            "social_dynamics": self.social_dynamics,
            "infrastructure": self.infrastructure,
            "current_tension": self.current_tension,
            "magic_system": self.magic_system,
            "misc_information": self.misc_information
        }

class StoryGlossary(BaseModel): 
    """StoryGlossary model. Inherits from Pydantic's BaseModel.

    Represents the top-level container for a story concept, 
    combining metadata with its core components.

    Attributes:
        title (str): The working title of the story.
        theme (str): The central theme or underlying message of the story.
        audience (str): The intended target audience (e.g., children, young adults, adults).
        genre (str): The narrative genre (e.g., fantasy, sci-fi, mystery).
        characters (list[Character]): A list of character objects that appear in the story.
        setting (Setting | None): The story's setting, or None if not defined.
        plot (Plot | None): The story's plot outline, or None if not defined.
    """   
    title: str
    theme: str
    audience: str
    genre: str
    characters: list[Character] 
    setting: Setting | None
    plot: Plot | None

    
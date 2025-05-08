from pydantic import BaseModel
from typing import List, Optional

class Character(BaseModel):
    name: str
    age: int
    looks: str
    sacred_flaw: str
    temperament: str
    backstory_events: List[str]
    motivation: str
    relationships: List[str]
    skills: List[str]
    misc_information: Optional[dict]

    def to_dict(self):
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
    genre: str
    blurb: str
    overall_outline: str
    main_conflict: str
    act_one_outline: str
    act_two_outline: str
    act_three_outline: str
    act_four_outline: str
    act_five_outline: str
    misc_information: Optional[dict]

    def to_dict(self):
        return {
            "genre": self.genre,
            "blurb": self.blurb,
            "outline": self.outline,
            "main_conflict": self.main_conflict,
            "act_one_outline": self.act_one_outline,
            "act_two_outline": self.act_two_outline,
            "act_three_outline": self.act_three_outline,
            "act_four_outline": self.act_four_outline,
            "act_five_outline": self.act_five_outline,
            "misc_information": self.misc_information
        }

class Setting(BaseModel):
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
    magic_system: Optional[str] | Optional[dict]
    misc_information: Optional[dict]
    
    def to_dict(self):
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
    title: str
    theme: str
    characters: List[Character] 
    setting: Setting | None
    plot: Plot | None

    
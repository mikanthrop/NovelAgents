from pydantic import BaseModel
from typing import List, Optional

class CharacterFormat(BaseModel):
    name: str
    age: int
    looks: str
    sacred_flaw: str
    temperament: str
    backstory_events: List[str]
    motivation: str
    relationships: List[str]
    skills: List[str]

class PlotFormat(BaseModel):
    genre: str
    blurb: str
    outline: str
    main_conflict: str
    act_one_outline: str
    act_two_outline: str
    act_three_outline: str
    act_four_outline: str
    act_five_outline: str

class SettingFormat(BaseModel):
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
    magic_system: Optional[str]

class StoryGlossary(BaseModel): 
    title: str
    theme: str
    characters: List[CharacterFormat]
    setting: SettingFormat
    plot: PlotFormat
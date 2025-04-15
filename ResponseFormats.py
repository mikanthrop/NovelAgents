from pydantic import BaseModel
from typing import List

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
    act_one_outline: str
    act_two_outline: str
    act_three_outline: str
    act_four_outline: str
    act_five_outline: str

class SettingFormat(BaseModel):
    time: str
    special_features: List[str]

class ConflictFormat(BaseModel):
    main_conflict: str

class StoryGlossary(BaseModel): 
    title: str
    characters: List[CharacterFormat]
    plot: PlotFormat
    setting: SettingFormat
    conflict: ConflictFormat
    theme: str
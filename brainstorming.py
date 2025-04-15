from pydantic import BaseModel
from typing import List
from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse

import os
import json
from datetime import datetime
import re
import traceback


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


## Opens a new json file named with a timestamp of creation and saves the first json into it
# potentially needs a pathfile in provided variables
def create_brainstorm_json():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"brainstorming_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4)
    print(f"{filename} has been set up.")
    return filename


## Deletes a file with the provided name if it exists
# potentially needs to delete a file at a specific path
def delete_brainstorm_json(filename:str):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} has been deleted.")
    else: 
        print(f"{filename} does not exist.")


## Using regex to get pure json from answer of planner model
def extract_json_from_response(text: str): 
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.DOTALL)
    if match: 
        json_str = match.group(1)
    else: 
        json_str = text
    try: 
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e)
        print(traceback.format_exc())
    return json.loads(json_str)


## Setting up the cycle in which the planner and critic build a character
def makeCharacter(planner: ChatAgent, critic: ChatAgent, 
                  initial_message: str, round_limit: int = 2) -> str:
    """
    Cycle in which planner and critic agent design one character.
    """

    if round_limit < 1: 
            ValueError("round_limit must be at least 1.")
            print(f"round_limit is {round_limit}")

    character_data: str 
    input_msg: ChatAgentResponse = planner.step(initial_message, response_format=
                             CharacterFormat)
    character_data: str = extract_json_from_response(input_msg.msg.content) # making answer to raw json
    print(f"Response of character planner: {character_data}.\n")

    # looping through to iterate the character and make general 
    # statements more specific with the critic's feedback
    for _ in range(round_limit):
        critic_response : ChatAgentResponse = critic.step(input_msg.msg),
        critic_msg: ChatAgentResponse = critic_response[0] # Getting first object in tuple of critic_response 
        print(f"Response of critic: {critic_msg.msg.content}.\n")

        # Break Criteria 
        # [TO DO]: should be changed to other criteria, for example time spent on this task
        if 'CAMEL_TASK_DONE' in critic_msg.msgs[0].content:
            break

        planner_response = planner.step(critic_msg.msg, CharacterFormat)
        input_msg = planner_response
        # Making sure only plain json gets passed along
        character_data = extract_json_from_response(planner_response.msg.content)
        print(f"Response of character planner: {character_data}.\n")

    print(f"The finished character json: {character_data}")
    return character_data # should be pure str


## Writing down overall plot structure in json
def makePlot(planner: ChatAgent, critic: ChatAgent, initial_message: str, round_limit: int = 2) -> str: 
    """
    Cycle in which planner and critic agent specify a plot. 
    """

    if round_limit < 1: 
        ValueError("round_limit must be at least 1.")
        print(f"round_limit is {round_limit}")

    input_msg = planner.step(initial_message, PlotFormat)
    plot_json = extract_json_from_response(input_msg.msg.content)
    
    print(f"The finished plot: {plot_json}")
    return plot_json


## Brainstorms the important facts for a story and adds them to a json
#  glossary that functions as memory storage
def brainstormStory(planner: ChatAgent, critic: ChatAgent, genre: str, character_count: int) -> None: 
    """
    Process in which critic and planner generate a memory json file filled with characters, setting and plot. 
    This json file can be loaded into the next step. 
    """
    memory_file_name = create_brainstorm_json()
    characters_array = []
    # creates character_count characters to use in the story
    for _ in range(character_count):
        character_prompt = f"make a {_+1}. character for a {genre} story."
        print(character_prompt)
        character = makeCharacter(planner, critic, character_prompt, 1)
        characters_array.append(character)
        print(f"Characters array consists of: {characters_array}")
    # Opens the memory file to write into 
    with open(memory_file_name, "w", encoding="utf-8") as memory: 
        json.dump(f"{characters_array}\n\n", memory, indent=4, ensure_ascii=False)
    print(f"written all characters to {memory_file_name}.\n")

    # creates plot of story
    plot_prompt = f"write an innovative but engaging plot for a {genre} story."
    print(plot_prompt)
    plot = makePlot(planner, critic, plot_prompt)
    with open(memory_file_name, "w", encoding="utf-8") as memory: 
        json.dump(f"{plot}\n\n", memory, indent=4, ensure_ascii=False)
    print(f"Written plot to {memory_file_name}.\n")

   
    return None


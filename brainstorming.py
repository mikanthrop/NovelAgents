from pydantic import BaseModel
from typing import List
from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse

import os
import json
from datetime import datetime
import re


class CharacterFormat(BaseModel):
    name: str
    role: str
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
    match = re.search(r"```(?:json)?s*(\{.*?})\s*```", text, re.DOTALL)
    if match: 
        json_str = match.group(1)
    else: 
        json_str = text
    return json.loads(json_str)


## Setting up the cycle in which the planner and critic build a character
def makeCharacter(planner: ChatAgent, critic: ChatAgent, initial_message: str, round_limit: int = 2) -> str:
    character_data: str 
    input_msg = planner.step(initial_message, response_format=
                             CharacterFormat)
    # Checking if answer is raw json. If not, converting it to raw json
    character_data = extract_json_from_response(input_msg.msg.content)
    print(f"Response of character planner: {character_data}.\n")

    # looping through to iterate the character and make general 
    # statements more specific with the critic's feedback
    for _ in range(round_limit):
        critic_response : ChatAgentResponse = critic.step(character_data),
        # Getting the first object in the tuple of critic_response 
        # (because it is a tuple of ChatAgentReponse and info)
        critic_msg = critic_response[0]
        print(f"Response of critic: {critic_msg.msgs[0].content}.\n")

        # Checking if the taks is finished as the critic is advised to 
        # write CAMEL_TASK_DONE when the task is done
        if 'CAMEL_TASK_DONE' in critic_msg.msgs[0].content:
            break

        planner_response = planner.step(critic_msg.msg, 
                                        response_format=CharacterFormat)
        # Making sure only plain json gets passed along
        character_data = extract_json_from_response(planner_response.msg.content)
        print(f"Response of character planner: {character_data}.\n")

        # # Giving the planner_response into the loop
        # input_msg = planner_response
    print(f"The finished character json: {character_data}")
    return character_data

#makeCharacter(planner, critic, initial_message="Make a compelling protagonist")


## Brainstorms the important facts for a story and adds them to a json
#  glossary that functions as memory storage
def brainstormStory(planner: ChatAgent, critic: ChatAgent, genre: str, character_count: int): 
    memory_file_name = create_brainstorm_json()
    characters = []
    # creates character_count characters to use in the story
    for _ in range(character_count):
        character_prompt = f"make a {character_count}. character for a {genre} story."
        print(character_prompt)
        character = makeCharacter(planner, critic, initial_message=character_prompt)
        characters.append(character)
    # Opens the memory file to write into 
    with open(memory_file_name, "w", encoding="utf-8") as memory: 
        json.dump(characters, memory, indent=4, ensure_ascii=False)
    print(f"written all characters to {memory_file_name}.\n")
    return None


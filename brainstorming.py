from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse
from StoryGlossary import StoryGlossary

import ResponseFormats
import json
import re
import traceback


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
        print(json_str)
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
    input_msg: ChatAgentResponse = planner.step(initial_message, 
                             ResponseFormats.CharacterFormat)
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

        planner_response = planner.step(critic_msg.msg, ResponseFormats.CharacterFormat)
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
        print(f"round_limit is {round_limit}.")

    input_msg = planner.step(initial_message, ResponseFormats.PlotFormat)
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
    memory_file: StoryGlossary = StoryGlossary()
    # creates character_count characters to use in the story
    for _ in range(character_count):
        character_prompt = f"make a {_+1}. character for a {genre} story."
        print(character_prompt)
        character = makeCharacter(planner, critic, character_prompt, 1)
        memory_file.add_character(character)
    print(f"written all characters to {memory_file.filename}.\n")

    # creates plot of story
    plot_prompt = f"write an innovative but engaging plot for a {genre} story."
    print(plot_prompt)
    plot = makePlot(planner, critic, plot_prompt)
    memory_file.set_plot(plot)
    print(f"Written plot to {memory_file.filename}.\n")

    return None

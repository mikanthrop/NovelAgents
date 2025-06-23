from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse
from StoryGlossary import StoryGlossary
from camel.memories import AgentMemory, MemoryRecord
from camel.models.model_manager import ModelProcessingError
from typing import Dict

import ResponseFormats as format
import json
import StringParseUtility as util
from Drafting import restart_model


## Setting up the cycle in which the planner and critic build a character
def makeCharacter(planner: ChatAgent, critic: ChatAgent, 
                  initial_message: str, round_limit: int = 2) -> dict:
    """
    Cycle in which planner and critic agent design one character.

    Args:
        planner (ChatAgent): _description_
        critic (ChatAgent): _description_
        initial_message (str): _description_
        round_limit (int, optional): _description_. Defaults to 2.

    Returns:
        dict: _description_
    """

    if round_limit < 1: 
            ValueError("round_limit must be at least 1.\n")
            print(f"round_limit is {round_limit}.\n")

    planner_msg: ChatAgentResponse = planner.step(initial_message, format.Character)
    character_data: json = util.clean_response_to_str(planner_msg.msg.content) # making answer to raw json
    print(f"-----Response of character planner:-----\n{character_data}\n")

    # looping through to iterate the character and make general 
    # statements more specific with the critic's feedback
    for _ in range(round_limit):
        critic_response : ChatAgentResponse = critic.step(planner_msg.msg),
        critic_msg: ChatAgentResponse = critic_response[0] # Getting first object in tuple of critic_response 
        print(f"-----Response of critic:-----\n{critic_msg.msg.content}\n")

        planner_msg = planner.step(critic_msg.msgs[0], format.Character) 
        cleaned_str : str = util.clean_response_to_str(planner_msg.msg.content)
        clean_character: dict = json.loads(cleaned_str)
        print(f"-----Response of character planner:-----\n{clean_character}\n")

    return clean_character # should be dict


## Writing down overall plot structure in json
def makePlot(planner: ChatAgent, critic: ChatAgent, initial_message: str, round_limit: int = 2) -> dict: 
    """
    Cycle in which planner and critic agent specify a plot. 

    Args:
        planner (ChatAgent): _description_
        critic (ChatAgent): _description_
        initial_message (str): _description_
        round_limit (int, optional): _description_. Defaults to 2.

    Returns:
        dict: Dictionary filled with plot details.
    """
    if round_limit < 1: 
        ValueError("round_limit must be at least 1.\n")
        print(f"round_limit is {round_limit}.\n")

    while True: 
        try: 
            planner_msg : ChatAgentResponse= planner.step(initial_message, format.Plot)
            break
        except ModelProcessingError as e: 
            print(f"Initial planner step failed: {e}. Restarting model.")
            restart_model(planner)
    
    plot_json : json = util.clean_response_to_str(planner_msg.msg.content)
    print(f"-----Response of plot planner:-----\n{plot_json}\n")

    for _ in range(round_limit):
        while True: 
            try: 
                critic_msg : ChatAgentResponse = critic.step(planner_msg.msg)
                break
            except ModelProcessingError as e: 
                print(f"Critic step {_+1} failed: {e}. Restarting model.")
                restart_model(critic)

        print(f"-----Response of critic:-----\n{critic_msg.msg.content}\n")

        while True: 
            try: 
                planner_msg = planner.step(critic_msg.msg, format.Plot)
                break
            except ModelProcessingError as e: 
                print(f"Planner step {_+1} failed: {e}. Restarting model.")
                restart_model(planner)

        cleaned_str : str = util.clean_response_to_str(planner_msg.msg.content)
        clean_plot : dict = json.loads(cleaned_str)
        print(f"-----Response of plot planner:-----\n{clean_plot}\n")
    
    return clean_plot # should be dict


## Thinking up the overall setting in json, then honing in on one specific part
def makeSetting(planner: ChatAgent, critic: ChatAgent, initial_message: str, round_limit: int = 2) -> dict: 
    """
    Cycle in which planner and critic agent brainstorm setting and choose a specific part to further develop.

    Args:
        planner (ChatAgent): _description_
        critic (ChatAgent): _description_
        initial_message (str): _description_
        round_limit (int, optional): _description_. Defaults to 2.

    Returns:
        dict: _description_
    """
    if round_limit < 1: 
        ValueError("round_limit must be at least 1.\n")
        print(f"round_limit is {round_limit}.\n")
    
    # First json answer that needs refinement
    planner_msg = planner.step(initial_message, format.Setting)
    setting_data : dict = util.clean_response_to_str(planner_msg.msg.content)
    print(f"-----Response of setting planner:-----\n{setting_data}\n")

    for _ in range(round_limit):
        critic_msg : ChatAgentResponse = critic.step(planner_msg.msg)
        print(f"-----Response of critic:-----\n{critic_msg.msg.content}\n")

        planner_msg = planner.step(critic_msg.msg, format.Setting)
        cleaned_str : str = util.clean_response_to_str(planner_msg.msg.content)
        clean_setting: dict = json.loads(cleaned_str) 
        print(f"-----Response of setting planner:-----\n{clean_setting}")
    
    return clean_setting

def makeTitle(planner: ChatAgent) -> str:
    title_msg = planner.step("Give the story we have created a title.")
    return title_msg.msg.content


## Brainstorms the important facts for a story and adds them to a json
#  glossary that functions as memory storage
def brainstormStory(planner: ChatAgent, critic: ChatAgent, genre: str, audience: str, theme: str, character_count: int) -> str: 
    """_summary_

    Args:
        planner (ChatAgent): The agent that plans the story, only answers in json.
        critic (ChatAgent): The agent that gives feedback to the json anwers.
        genre (str): The genre of the story that the agents should brainstorm.
        audience (str): The audience of the story that the agents should brainstorm.
        theme (str): The theme of the story that the agents should brainstorm.
        character_count (int): Number of characters the agents should brainstorm for the story.

    Returns:
        None
    """
    memory_file: StoryGlossary = StoryGlossary()
    memory_file.set_theme(theme)

    # creates character_count characters to use in the story
    for _ in range(character_count):
        character_prompt = f"Make a {_+1}. character for a {genre} story aimed at {audience} with a theme of {theme}."
        print(f"{character_prompt}\n")
        character: format.Character = makeCharacter(planner, critic, character_prompt, 1)
        memory_file.add_character(character)
    print(f"Finished brainstorming characters.\n")

    # creates setting of story
    setting_prompt = f"Create an innovative but engaging setting for a {genre} story aimed at {audience} with a theme of {theme}."
    print(f"{setting_prompt}\n")
    setting : format.Setting = makeSetting(planner, critic, setting_prompt, 1)
    memory_file.set_setting(setting)
    print(f"Finished brainstorming setting.\n")

    # creates plot of story
    plot_prompt = f"Write an innovative but engaging plot for a {genre} story aimed at {audience} with a theme of {theme}."
    print(f"{plot_prompt}\n")
    plot : format.Plot = makePlot(planner, critic, plot_prompt, 1)
    memory_file.set_plot(plot)
    print(f"Finished brainstorming plot.\n")

    # gives the story a title
    title = makeTitle(planner)
    if title is Dict:
        title = title("title")
    if title is str: 
        memory_file.set_title(title)

    print(f"the whole story glossary: {memory_file.to_dict()}")
    memory_file.save()

    return memory_file.filename

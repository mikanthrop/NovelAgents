from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse
from StoryGlossary import StoryGlossary

import ResponseFormats as format
import json
import utility as util


## Setting up the cycle in which the planner and critic build a character
def make_character(
    planner: ChatAgent, 
    critic: ChatAgent, 
    initial_message: str, 
    round_limit: int = 2
) -> dict:
    """
    Generates a character through iterative feedback between a planner and a critic agent.

    The planner agent initially creates a character based on `initial_message`.
    The critic provides feedback, which the planner then uses to refine the character.
    This process is repeated up to `round_limit` rounds to produce a more detailed and polished character.

    Args:
        planner (ChatAgent): Agent responsible for creating the character.
        critic (ChatAgent): Agent responsible for providing feedback on the character.
        initial_message (str): Instructions or prompt for the planner agent.
        round_limit (int, optional): Number of feedback and rewrite iterations. Defaults to 2.

    Returns:
        dict: A dictionary representing the character, conforming to the `Character` Pydantic schema.
    """

    planner_msg: ChatAgentResponse = planner.step(initial_message, format.Character)
    character_data: str = util.clean_response_to_str(planner_msg.msg.content) # making answer to raw json
    print(f"-----Response of character planner:-----\n{character_data}\n")
    
    if round_limit < 1: 
        return json.loads(character_data)

    # looping through to iterate the character and make general 
    # statements more specific with the critic's feedback
    clean_character: dict = json.loads(character_data)
    for _ in range(round_limit):
        critic_response : ChatAgentResponse = critic.step(planner_msg.msg),
        critic_msg: ChatAgentResponse = critic_response[0] # Getting first object in tuple of critic_response, just in case it is a tuple
        print(f"-----Response of critic:-----\n{critic_msg.msg.content}\n")

        planner_msg = planner.step(critic_msg.msgs[0], format.Character) 
        cleaned_str : str = util.clean_response_to_str(planner_msg.msg.content)
        clean_character = json.loads(cleaned_str)
        print(f"-----Response of character planner:-----\n{clean_character}\n")

    return clean_character


## Writing down overall plot structure in json
def make_plot(planner: ChatAgent, critic: ChatAgent, initial_message: str, round_limit: int = 2) -> dict: 
    """
    Generates a plot through iterative feedback between a planner and a critic agent.

    The planner agent initially creates a plot based on `initial_message`.
    The critic provides feedback, which the planner then uses to refine the plot.
    This process is repeated up to `round_limit` rounds to produce a detailed and coherent plot.

    Args:
        planner (ChatAgent): Agent responsible for creating the plot.
        critic (ChatAgent): Agent responsible for providing feedback on the plot.
        initial_message (str): Instructions or prompt for the planner agent.
        round_limit (int, optional): Number of feedback and rewrite iterations. Defaults to 2.

    Returns:
        dict: A dictionary representing the plot, conforming to the `Plot` Pydantic schema.
    """
    planner_msg : ChatAgentResponse= planner.step(initial_message, format.Plot)
    plot_data : str = util.clean_response_to_str(planner_msg.msg.content)
    print(f"-----Response of plot planner:-----\n{plot_data}\n")

    if round_limit < 1: 
        return json.loads(plot_data)

    clean_plot : dict = json.loads(plot_data)
    for _ in range(round_limit):
        critic_msg : ChatAgentResponse = critic.step(planner_msg.msg)
        print(f"-----Response of critic:-----\n{critic_msg.msg.content}\n")

        planner_msg = planner.step(critic_msg.msg, format.Plot)
        cleaned_str : str = util.clean_response_to_str(planner_msg.msg.content)
        clean_plot = json.loads(cleaned_str)
        print(f"-----Response of plot planner:-----\n{clean_plot}\n")
    
    return clean_plot # should be dict


## Thinking up the overall setting in json, then honing in on one specific part
def make_setting(planner: ChatAgent, critic: ChatAgent, initial_message: str, round_limit: int = 2) -> dict: 
    """
    Generates a setting through iterative feedback between a planner and a critic agent.

    The planner agent initially creates a setting based on `initial_message`.
    The critic provides feedback, which the planner then uses to refine the setting.
    This process is repeated up to `round_limit` rounds to produce a detailed and coherent setting.

    Args:
        planner (ChatAgent): Agent responsible for creating the setting.
        critic (ChatAgent): Agent responsible for providing feedback on the setting.
        initial_message (str): Instructions or prompt for the planner agent.
        round_limit (int, optional): Number of feedback and rewrite iterations. Defaults to 2.

    Returns:
        dict: A dictionary representing the setting, conforming to the `Setting` Pydantic schema.
    """

    # First json answer that needs refinement
    planner_msg = planner.step(initial_message, format.Setting)
    setting_data : str = util.clean_response_to_str(planner_msg.msg.content)
    print(f"-----Response of setting planner:-----\n{setting_data}\n")

    if round_limit < 1: 
        return json.loads(setting_data)

    clean_setting: dict = json.loads(setting_data) 
    for _ in range(round_limit):
        critic_msg : ChatAgentResponse = critic.step(planner_msg.msg)
        print(f"-----Response of critic:-----\n{critic_msg.msg.content}\n")

        planner_msg = planner.step(critic_msg.msg, format.Setting)
        cleaned_str : str = util.clean_response_to_str(planner_msg.msg.content)
        clean_setting = json.loads(cleaned_str) 
        print(f"-----Response of setting planner:-----\n{clean_setting}")
    
    return clean_setting

def makeTitle(planner: ChatAgent) -> str:
    """
    Generates a title for the story using the planner agent.

    The planner agent is prompted to create a title based on the story content 
    it has generated or been provided with.

    Args:
        planner (ChatAgent): The agent responsible for creating the title.

    Returns:
        str: The title generated by the planner agent.
    """
    title_msg : ChatAgentResponse = planner.step("Give the story we have created a title.")
    return title_msg.msg.content


## Brainstorms the important facts for a story and adds them to a json
#  glossary that functions as memory storage
def brainstorm_story(planner: ChatAgent, critic: ChatAgent, genre: str, audience: str, theme: str, character_count: int, revision_number: int) -> dict: 
    """
    Orchestrates the brainstorming of a story by creating characters, setting, plot, and title.

    The planner agent generates content, and the critic provides feedback in multiple 
    iterative rounds. The story glossary stores all generated information.

    Args:
        planner (ChatAgent): The agent responsible for generating story elements in JSON format.
        critic (ChatAgent): The agent responsible for providing feedback on JSON outputs.
        genre (str): The genre of the story to be brainstormed.
        audience (str): The intended audience of the story.
        theme (str): The theme of the story.
        character_count (int): Number of characters to generate for the story.
        revision_number (int): Number of feedback/revision rounds for each generated element.

    Returns:
        StoryGlossary: An object containing the complete story data, including characters, setting, plot, and title.
    """
    story_glossary: StoryGlossary = StoryGlossary()
    story_glossary.set_theme(theme)
    story_glossary.set_audience(audience)
    story_glossary.set_genre(genre)

    # Generate characters
    for _ in range(character_count):
        if _ == 0:
            character_prompt = f"Make a {_+1}. character for a {genre} story aimed at {audience} with a theme of {theme}."
        else: 
            character_prompt = f"Brainstorm a character that surrounds the character of {main_character['name']} in this {genre} story aimed at {audience} with a theme of {theme}. It's best if you flesh out a character that already ties into the main character but hasn't been worked on already. Think about what characters the story already has and what kind of character it still needs to make a compelling story."
        print(f"{character_prompt}\n")
        
        character: dict = make_character(planner, critic, character_prompt, revision_number)
        if _ == 0: 
            main_character = character
        story_glossary.add_character(character)
    print(f"Finished brainstorming characters.\n")

    # Generate setting
    setting_prompt = f"Create an innovative but engaging setting for a {genre} story aimed at {audience} with a theme of {theme}."
    print(f"{setting_prompt}\n")
    setting : dict = make_setting(planner, critic, setting_prompt, revision_number)
    story_glossary.set_setting(setting)
    print(f"Finished brainstorming setting.\n")

    # Generate story
    plot_prompt = f"Write an innovative but engaging plot for a {genre} story aimed at {audience} with a theme of {theme}."
    print(f"{plot_prompt}\n")
    plot : dict = make_plot(planner, critic, plot_prompt, revision_number)
    story_glossary.set_plot(plot)
    print(f"Finished brainstorming plot.\n")

    # gives the story a title
    title = makeTitle(planner)
    if isinstance(title, dict) and "title" in title:
        title = title["title"]
    story_glossary.set_title(title)

    print(f"the whole story glossary: {story_glossary.to_dict()}")
    return story_glossary
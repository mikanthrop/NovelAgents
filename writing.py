
from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse
from camel.prompts import TextPrompt
from StoryGlossary import StoryGlossary
from Prompts import scene_writing_prompt

def set_writer_prompt(story_glossary: StoryGlossary) -> TextPrompt: 
    """Generates a TextPrompt for a writer agent based on a StoryGlossary.

    This function extracts the setting, characters, and plot from a StoryGlossary 
    instance and formats them into a prompt that can be used by a writer agent 
    for scene generation. If any component is missing, a placeholder instruction 
    is used instead.

    Args:
        story_glossary (StoryGlossary): The story glossary containing metadata, 
            characters, setting, and plot.

    Returns:
        TextPrompt: A formatted text prompt ready for input into the writer agent.
    """
    setting = StoryGlossary.get_setting(story_glossary) or "Make something up that fits the characters and the plot."
    characters = StoryGlossary.get_characters(story_glossary) or "Make up characters that fit the setting and plot."
    plot = StoryGlossary.get_plot(story_glossary) or "Make up a plot that fits both the setting and the characters."

    return scene_writing_prompt.format(
        characters=characters,
        setting=setting,
        plot=plot
    )

def write_scenes(writer: ChatAgent, critic: ChatAgent, scene_prompts: list[str], round_limit: int = 2) -> dict:
    """Generates story scenes from prompts using a writer agent and optional critic feedback.

    For each prompt in `scene_prompts`, the writer agent generates content. 
    Optionally, the generated text is rewritten with feedback from the critic 
    agent using multiple iterations (`round_limit`). The resulting scenes are 
    stored in a dictionary with keys like "Chapter1", "Chapter2", etc.

    Args:
        writer (ChatAgent): The agent responsible for generating scene drafts.
        critic (ChatAgent): The agent providing feedback for rewrites.
        scene_prompts (list[str]): A list of prompts, one per scene to generate.
        round_limit (int, optional): Number of feedback + rewrite iterations per scene. Defaults to 2.

    Returns:
        dict[str, str]: A dictionary mapping chapter keys (e.g., "Chapter1") to 
        the generated scene content.
    """
    writing: dict = {}

    for i, prompt in enumerate(scene_prompts):
        
        try:
            writer_msg = writer.step(prompt)
            print(f"\n------\nScene Prompt: \n{prompt}\n")

            # Handle multiple messages
            if isinstance(writer_msg, list):
                print(f"Warning: Multiple messages returned for scene {i+1}. Selecting the first one.")
                selected_msg = writer_msg[0]  
                writer.record_message(selected_msg)
            else:
                selected_msg = writer_msg

            content = getattr(selected_msg.msg, 'content', None)
            print(f"\n------\nWriter Draft: \n{content}")

            if content is None:
                print(f"Warning: No content generated for scene {i+1}. Skipping...")
                continue  

            chapter_key = f"Chapter{i+1}"
            writing[chapter_key] = content
            print(f"\n{chapter_key}: \n{content}")

            rewrite(writer, critic, content, round_limit)

        except AttributeError as e:
            print(f"AttributeError in scene {i+1}: {e}. Possibly missing message content.")
        
    return writing


def rewrite(rewriter: ChatAgent, critic: ChatAgent, writing_file: str, round_limit: int = 2) -> str:
    """Iteratively rewrites a text file or string using a rewriter agent and feedback from a critic agent.

    The function reads a text either from a file or directly from a string, 
    then performs multiple rounds (controlled by `round_limit`) where:
        1. The critic provides feedback on the current text.
        2. The rewriter rewrites the text based on the critic's feedback.
    The final rewritten text is returned.

    Args:
        rewriter (ChatAgent): The agent responsible for rewriting the text.
        critic (ChatAgent): The agent responsible for providing feedback on the text.
        writing_file (str): Path to a text file or a raw string containing the text to rewrite.
        round_limit (int, optional): Number of feedback + rewrite iterations. Defaults to 2.

    Returns:
        str: The final rewritten text after all iterations.
    """       
    ## TODO: Check if writing_file is a path to a valid txt file
    text: str
    if ".txt" in writing_file:
        with open(writing_file, "r") as f:
            text = f.read()

    else:
        text = writing_file
        
    for _ in range(round_limit):
        critic_msg: ChatAgentResponse = critic.step(f"\nGive feedback to the following text: {text}")
        print(f"\n------\nCritic Response: \n{critic_msg.msg.content}")

        rewriter_msg: ChatAgentResponse = rewriter.step(f"\nCritic feedback: {critic_msg.msg.content}\nText to rewrite: {text}")
        print(f"\n------\nRewriter Response: \n{rewriter_msg.msg.content}")
        text = rewriter_msg.msg.content
    return text

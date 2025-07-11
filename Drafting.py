
from camel.agents import ChatAgent, TaskPlannerAgent
from camel.prompts import TextPrompt
from camel.models.model_manager import ModelProcessingError
from StoryGlossary import StoryGlossary
import Prompts
import Rewriting
import json
import time
import subprocess
from datetime import datetime


def split_scenes(all_scenes: str) -> list[str]:
    """_summary_

    Args:
        all_scenes (str): _description_

    Returns:
        list[str]: _description_
    """    
    scene_prompts = all_scenes.strip().split("New Scene")
    if scene_prompts[0].strip() == '':
        scene_prompts.pop(0)
    return scene_prompts


def restart_model(model):
    """_summary_

    Args:
        model (_type_): _description_

    Raises:
        ValueError: _description_
    """    
    model_type: str = getattr(model, "model_type", None)
    if model_type is None: 
        raise ValueError("Model name not found in agent. Expected `model_name` attribute.")
    print(f"Restarting Ollama model: {model_type}")

    try:
        subprocess.Popen(["ollama", "run", model_type], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)  # Wait for the model to initialize
    except Exception as e:
        print(f"[ERROR] Failed to restart model: {e}")


def set_writer_prompt(story_glossary: StoryGlossary) -> TextPrompt: 
    setting = StoryGlossary.get_setting(story_glossary) or "Make something up that fits the characters and the plot."
    characters = StoryGlossary.get_characters(story_glossary) or "Make up characters that fit the setting and plot."
    plot = StoryGlossary.get_plot(story_glossary) or "Make up a plot that fits both the setting and the characters."

    return Prompts.scene_writing_prompt.format(
        characters=characters,
        setting=setting,
        plot=plot
    )


## approach of loading the json memory file into the task planner prompt: 
def set_planner_prompt(story_glossary: StoryGlossary, scene_number: int) -> TextPrompt: 
    """_summary_

    Args:
        memory_path (str): _description_

    Returns:
        TextPrompt: _description_
    """    
  
    setting = StoryGlossary.get_setting(story_glossary) or "Make something up that fits the characters and the plot."
    characters = StoryGlossary.get_characters(story_glossary) or "Make up characters that fit the setting and plot."
    plot = StoryGlossary.get_plot(story_glossary) or "Make up a plot that fits both the setting and the characters."

    return Prompts.scene_planning_prompt.format(
        setting=setting, 
        characters=characters,
        plot=plot,
        scene_number=scene_number
    )
    

def save_scene_prompts_to_txt(scene_prompts: list[str]) -> str: 
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scene_planning_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f: 
        for _ in range(len(scene_prompts)):
            f.write(f"Szene {_}: {scene_prompts[_]}\n")


def run_planner(task_master: TaskPlannerAgent, story_glossary: StoryGlossary, scene_number: int) -> list[str]:
    """_summary_

    Args:
        task_master (TaskPlannerAgent): _description_
        memory_path (str): _description_

    Returns:
        list[str]: _description_
    """    
    planner_prompt: TextPrompt = set_planner_prompt(story_glossary, scene_number)

    all_scenes = task_master.run(planner_prompt)
    scene_prompts : list[str] = split_scenes(all_scenes)
    print(f"Scene writing prompts: {all_scenes}")

    return scene_prompts


def write_scenes(writer: ChatAgent, critic: ChatAgent, scene_prompts: list[str]) -> dict:
    """_summary_

    Args:
        writer (ChatAgent): _description_
        critic (ChatAgent): _description_
        rewriter (ChatAgent): _description_
        scene_prompts (list[str]): _description_

    Returns:
        dict: _description_
    """
    writing: dict = {}
    loop_nr: int = 1

    for i, prompt in enumerate(scene_prompts):
        
        try:
            writer_msg = writer.step(prompt)
        except ModelProcessingError as e:
            print(f"Error in scene {i+1}: {e}. Restarting model...")
            restart_model(writer)

        writing[f"Chapter{i+1}"] = writer_msg.msg.content
        print(f"\nChapter {loop_nr}: \n{writer_msg.msg.content}")
        
        Rewriting.rewrite(writer, critic, writing[f"Chapter{i+1}"])

        loop_nr += 1
        
    return writing







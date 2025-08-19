from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent, TaskPlannerAgent
from datetime import datetime

import Prompts
import Brainstorming
import Drafting
import Rewriting
import os

open_api_key = os.environ["OPENAI_API_KEY"]

# BRAINSTORMING
# Defining the model to use for writing, using olmo2 as llama3 did not 
# write that well
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type="gpt-4o-mini", 
    model_config_dict={"temperature": 0.6},
)

## Create the planner AI agent with a designated system message 
planner = ChatAgent(
    system_message=Prompts.planner_prompt, 
    model=model
)

critic = ChatAgent(
    system_message=Prompts.critic_prompt, 
    model=model
)

#--------------------

## WRITING

# model = ModelFactory.create(
#     model_platform=ModelPlatformType.OLLAMA,
#     model_type="olmo2", 
#     model_config_dict={"temperature": 0.7},
# )

taskmaster1 : TaskPlannerAgent = TaskPlannerAgent(
    model=model
)

writing_model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI, 
    model_type="gpt-4o-mini", 
    model_config_dict={"temperature": 0.65},
)

writer = ChatAgent(
    system_message=Prompts.scene_writing_prompt,
    model=writing_model,
    token_limit=None
)

# --------

## FEEDBACKING
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI, 
    model_type="gpt-4o-mini"
)

feedback_agent: ChatAgent = ChatAgent(
    system_message=Prompts.feedback_prompt, 
    model=model
)

rewrite_agent: ChatAgent = ChatAgent(
    system_message=Prompts.rewrite_prompt,
    model=model
)




# the algorithm that actually does stuff
start = datetime.now()

## BRAINSTORMING
memory_file = Brainstorming.brainstorm_story(planner, critic, "science fiction thriller", "adults, aged 25 and up", "murder on a space station", 2)

## WRITING

scene_prompts: list[str] = Drafting.run_planner(taskmaster1, memory_file)

written_scenes: dict = Drafting.write_scenes(writer, feedback_agent, rewrite_agent, scene_prompts)
Rewriting.save_to_txt(written_scenes)

## FEEDBACKING


end = datetime.now()

print(f"Started at: {start.strftime('%H:%M:%S')}")
print(f"Ended at: {end.strftime('%H:%M:%S')}")
print(f"Duration: {((end - start)/60).total_seconds():.2f} minutes")
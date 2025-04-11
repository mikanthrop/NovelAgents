from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.messages import BaseMessage
from camel.types import RoleType
from camel.agents import ChatAgent
import brainstorming
from datetime import datetime

# Prompt for the Planner since System Message isn't enough
planner_prompt : BaseMessage = BaseMessage(
    role_name="story planner",
    role_type=RoleType.ASSISTANT,
    meta_dict=None, #dict["sacred_flaw": "important"],
    content="You are a professional story planner. Your job is to make " \
    "compelling and well-thought out characters that can tell a compelling" \
    " story. Also you should take feedback from me and incorparate it " \
    "into the character. You should answer only in raw JSON."
)

critic_prompt : BaseMessage = BaseMessage(
    role_name="picky editor", 
    role_type=RoleType.USER,
    meta_dict=None, 
    content="You are a picky editor working together with a character " \
    "generating AI. Your job is to give honest feedback to the character json " \
    "format you are given. You have to make sure all the aspects of the " \
    "character make sense, for example the heroine shouldn't have trust issues " \
    "but one of her outstanding qualities is her loyalty. You have to spot these " \
    "inconsistencies. You should also ask the character generating AI to be " \
    "more specific."
)

## Defining the model to use for writing, using olmo2 as llama3 did not 
# write that well
model = ModelFactory.create(
    model_platform=ModelPlatformType.OLLAMA,
    model_type="olmo2", 
    model_config_dict={"temperature": 0.6},
)

## Create the planner AI agent with a designated system message 
planner = ChatAgent(
    system_message=planner_prompt, 
    model=model,
    token_limit=10000,
)

critic = ChatAgent(
    system_message=critic_prompt, 
    model=model, 
    token_limit=10000,
)

start = datetime.now()
brainstorming.brainstormStory(planner, critic, "romantasy", 2)
end = datetime.now()

print(f"Started at: {start.strftime('%H:%M:%S')}")
print(f"Ended at: {end.strftime('%H:%M:%S')}")
print(f"Duration: {((end - start)/60).total_seconds():.2f} minutes")
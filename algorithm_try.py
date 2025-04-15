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
    content="You are a professional story planner and I am your picky " \
    "editor. Your job is to make compelling and well thought-out characters, " \
    "story and setting that make a compelling and investing story. Be " \
    "precise in your ideas. Write in absolutes, no maybes. You should take " \
    "feedback from me and incorparate it into the character, the story "
    "or setting. You should answer only in raw JSON."
)

critic_prompt : BaseMessage = BaseMessage(
    role_name="picky editor", 
    role_type=RoleType.USER,
    meta_dict=None, 
    content="You are a picky editor working together with me, a story planner." \
    " Your job is to give me your honest feedback to the json formats I provide you " \
    "with. You have to make sure all the aspects of the character, story or setting " \
    "make sense in itself. For example the heroine shouldn't have trust issues but" \
    " one of her outstanding qualities is her loyalty. You have to spot" \
    " inconsistencies. You should ask me to be more specific in my general statements." \
    "You should spot and eliminate clichés. You must not use the json format."
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
# brainstorming.makePlot(planner, critic, "Write a romantasy plot", 2)
#brainstorming.makeCharacter(planner, critic, "Write a romantasy story protagonist")
end = datetime.now()

print(f"Started at: {start.strftime('%H:%M:%S')}")
print(f"Ended at: {end.strftime('%H:%M:%S')}")
print(f"Duration: {((end - start)/60).total_seconds():.2f} minutes")
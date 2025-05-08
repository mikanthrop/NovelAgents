from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent
from datetime import datetime

import Brainstorming
import Prompts


## Defining the model to use for writing, using olmo2 as llama3 did not 
# write that well
model = ModelFactory.create(
    model_platform=ModelPlatformType.OLLAMA,
    model_type="olmo2", 
    model_config_dict={"temperature": 0.6},
)

## Create the planner AI agent with a designated system message 
planner = ChatAgent(
    system_message=Prompts.planner_prompt, 
    model=model,
    token_limit=10000,
)

critic = ChatAgent(
    system_message=Prompts.critic_prompt, 
    model=model, 
    token_limit=10000,
)





start = datetime.now()
Brainstorming.brainstormStory(planner, critic, "dark romance", "females 20 - 24", "drama", 2)
#Brainstorming.makeCharacter(planner, critic, "Write a children's book story protagonist for ages 5 to 8.",1)
#Brainstorming.makePlot(planner, critic, "Write a romantasy plot", 2)
#Brainstorming.makeSetting(planner, critic, "Make up a setting for a childrens book for ages 5 to 8.")
end = datetime.now()

print(f"Started at: {start.strftime('%H:%M:%S')}")
print(f"Ended at: {end.strftime('%H:%M:%S')}")
print(f"Duration: {((end - start)/60).total_seconds():.2f} minutes")
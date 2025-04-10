from pydantic import BaseModel
from typing import List
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse
from camel.messages import BaseMessage
from camel.types import RoleType



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


# Prompt for the Planner since System Message isn't enough
planner_prompt : BaseMessage = BaseMessage(
    role_name="story planner",
    role_type=RoleType.ASSISTANT,
    meta_dict=None, #dict["sacred_flaw": "important"],
    content="You are a professional story planner. Your job is to make " \
    "compelling and well-thought out characters that can tell a compelling" \
    " story. Also you should take feedback from me and incorparate it " \
    "into the character."
)

critic_prompt : BaseMessage = BaseMessage(
    role_name="picky editor", 
    role_type=RoleType.USER,
    meta_dict=None, 
    content="You are a picky editor working together with a character " \
    "generating AI. Your job is to give feedback to the character json " \
    "format you are given. You have to make sure all the aspects of the " \
    "character make sense. You should also ask the character generating " \
    "AI to be more specific."
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

initial_message= "Make a compelling character."

## Setting up the cycle in which the planner and critic build a character
def makeCharacter(planner: ChatAgent, critic: ChatAgent, initial_message: str, round_limit: int = 2):
    input_msg = planner.step(initial_message, response_format=
                             CharacterFormat)
    print(f"Response of character planner: {input_msg.msg.content}.\n")

    # looping through to iterate the character and make general 
    # statements more specific with the critic's feedback
    for _ in range(round_limit):
        critic_response : ChatAgentResponse = critic.step(input_msg.msg.
                                                          content),
        # Getting the first object in the tuple of critic_response 
        # (because it is a tuple of ChatAgentReponse and info)
        critic_msg = critic_response[0]
        print(f"Response of critic: {critic_msg.msgs[0].content}.\n")

        planner_response = planner.step(critic_msg.msg, 
                                        response_format=CharacterFormat)
        print(f"Response of character planner: {planner_response.msg.content}.\n")

        # Checking if the taks is finished as the critic is advised to 
        # write CAMEL_TASK_DONE when the task is done
        if 'CAMEL_TASK_DONE' in critic_msg.msgs[0].content:
            break

        # Giving the planner_response into the loop
        input_msg = planner_response.msg
    print(f"The finished character json: {input_msg}")
    return None

makeCharacter(planner, critic, initial_message)
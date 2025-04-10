## Importing libraries for defining which model to use 
from camel.models import ModelFactory
from camel.types import ModelPlatformType, TaskType #, ModelType
## Importing libraries for communicating with the ChatAgent
#from camel.agents import ChatAgent
#from camel.messages import BaseMessage
from camel.societies import RolePlaying
from camel.prompts.ai_society import AISocietyPromptTemplateDict
## Importing libraries for Task Specifying
from camel.agents import TaskSpecifyAgent
## Importing libraries for Usage of Critic Agent
from camel.agents import CriticAgent
from camel.generators import SystemMessageGenerator as sys_msg_gen
from camel.types import RoleType

#openai api key
import os
from getpass import getpass

# Prompt for the API key securely
openai_api_key = getpass('Enter your API key: ')
os.environ["OPENAI_API_KEY"] = openai_api_key


## Defining the model to use for planning, using llama3 from ollama hosted locally as it performed well so far
# planner_model = ModelFactory.create(
#     model_platform=ModelPlatformType.OLLAMA,
#     model_type="llama3",
#     model_config_dict={"temperature": 1},
# )

## Setting up the roles of the AI user and AI assistant
user_role = "editor"
assistant_role = "author"
critic_role = "a picky book critic"
loop_number = 1


## Defining custom prompts for AI user and AI assistant
custom_user_prompt = "You are a meticulous editor who asks claryfying questions and suggests improvements."
custom_assistant_prompt = "You are a creative author who writes engaging narratives with vivid details."


## Defining the model to use for writing, using olmo2 as llama3 did not write that well
model = ModelFactory.create(
    model_platform=ModelPlatformType.OLLAMA,
    model_type="olmo2", 
    model_config_dict={"temperature": 0.6},
)


## Defining a broad task with a task specify agent to gain a more comprehensive and thorough prompt
task_specify_agent = TaskSpecifyAgent(
    model=model, task_type=TaskType.AI_SOCIETY
)
task_prompt="Writing a short fantasy novel together. Give details about writing style, what genres the novel uses, and how to keep the reader's attention."
specified_task_prompt = task_specify_agent.run(
    task_prompt=task_prompt,
    meta_dict=dict(
        assistant_role=assistant_role, user_role= user_role, word_limit=250
    ),
)
print(f"Specified task prompt:\n{specified_task_prompt}")


## Defining the name and the role of the critic to use in the AI Society loop
meta_dict = dict(critic_role=critic_role,
                 criteria="improve story quality")
role_tuple = (critic_role, RoleType.CRITIC)
sys_msg = sys_msg_gen().from_dict(meta_dict=meta_dict,
                                  role_tuple=role_tuple)
critic_agent = CriticAgent(system_message=sys_msg, model=model, verbose=True)
print(critic_agent.system_message.content)


## Defining the task the agents are working on together and what models are used
task_kwargs = {
    'task_prompt': specified_task_prompt,
    'with_task_specify': True,
    'task_specify_agent_kwargs': {'model': model}
}

## Setting the User arguments (this is the instruction sender)
user_role_kwargs = {
    "user_role_name": user_role,
    "user_agent_kwargs": {
        "model": model, 
        #"system_message": user_sys_msg,
        }
}


## Setting the Assistant arguments (this is the instruction executor)
assistant_role_kwargs = {
    "assistant_role_name": assistant_role,
    "assistant_agent_kwargs": {
        "model": model,
        #"system_message": assistant_sys_msg,
        }
}

## Setting the Critic arguments (this is a helper for making text more interesting)
critic_role_kwargs = {
    "with_critic_in_the_loop": True, 
    "critic_criteria": "improve the story quality",
    "critic_kwargs": dict(verbose=True)
}

## Putting the society together
society = RolePlaying(
    **task_kwargs,
    **user_role_kwargs,
    **assistant_role_kwargs,
    **critic_role_kwargs
)

## Helper function that ends the exchange between the agents
def is_terminated(response):
    """
    Give alerts when the session should be terminated.
    """
    if response.terminated:
        role = response.msg.role_type.name
        reason = response.info['termination_reasons']
        print(f'AI {role} terminated due to {reason}')
    return response.terminated

## Simple loop for our society to communicate
def run(society, round_limit: int = loop_number): 
    # Get the initial message from the ai assistant to the ai user
    input_msg = society.init_chat()

    # Starting the interactive session
    for _ in range(round_limit):
        # Get both responses for this round
        assistant_response, user_response = society.step(input_msg)

        # Check the termination condition
        if is_terminated(assistant_response) or is_terminated(user_response):
            break

        # Get the results
        print(f'[AI User] {user_response.msg.content}.\n')
        print(f'[AI Assistant] {assistant_response.msg.content}.\n')

        # Check if the task is finished
        if 'CAMEL_TASK_DONE' in user_response.msg.content:
            break


        # Get the input message for the next round
        input_msg = assistant_response.msg

    return None

run(society)

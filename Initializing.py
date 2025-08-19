from Enums import Model
import os
from camel.models import ModelFactory, BaseModelBackend
from camel.types import ModelPlatformType
from camel.agents import ChatAgent, TaskPlannerAgent
from Exceptions import ModelNotFoundError
from StoryGlossary import StoryGlossary
from Drafting import set_planner_prompt, set_writer_prompt
import Prompts


def initialize_chosen_model(model: str, key_or_path: str) -> BaseModelBackend:
        agent : BaseModelBackend
        
        # check for empty fields
        try: 
            if not model or model.strip() == "":
                raise ModelNotFoundError("Modellwahl fehlt.")
            if model not in [m.value for m in Model]:
                raise ValueError("Unbekanntes Modell ausgewählt.")
        except ModelNotFoundError as error: 
            raise RuntimeError("Bitte wähle ein gültiges KI-Modell aus.")
        except ValueError as error: 
            raise RuntimeError("Bitte wähle ein gültiges KI-Modell aus.")
        
        # initialize models and catch errors to give to the UI
        # for OpenAI platform
        if model == Model.CHATGPT4OMINI.value:
            if not key_or_path.strip():
                raise ValueError("API-Key fehlt.")
            os.environ["OPENAI_API_KEY"] = key_or_path
            agent = ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI,
                model_type="gpt-4o-mini",
                model_config_dict={"temperature": 0.6},
            )
            return agent
    
       
        # for OLLAMA platform       
        elif model in [m.value for m in Model]: 
            if not key_or_path.strip():
                raise ValueError("OLLAMA Pfad fehlt.")
            os.environ["OLLAMA_PATH"] = key_or_path

            if model == Model.MISTRAL.value: 
                agent = ModelFactory.create(
                    model_platform=ModelPlatformType.OLLAMA,
                    model_type="mistral",
                    model_config_dict={"temperature": 0.6},
                )
                return agent
            
            elif model == Model.LLAMA32.value:
                agent = ModelFactory.create(
                    model_platform=ModelPlatformType.OLLAMA,
                    model_type="llama3.2:3b",
                    model_config_dict={"temperature": 0.6},
                )
                return agent
            
            elif model == Model.QWEN25.value:
                agent = ModelFactory.create(
                    model_platform=ModelPlatformType.OLLAMA,
                    model_type="qwen2.5:14b",
                    model_config_dict={"temperature": 0.6},
                )
                return agent
            
            elif model == Model.OLMO2.value:
                agent = ModelFactory.create(
                    model_platform=ModelPlatformType.OLLAMA,
                    model_type="olmo2",
                    model_config_dict={"temperature": 0.9},
                )
                return agent
            
        raise ModelNotFoundError("Unbekanntes Modell oder Plattform.")
            

def initialize_brainstorming_agents(model:BaseModelBackend) -> dict[ChatAgent]:
    planner_agent = ChatAgent(
        system_message=Prompts.planner_prompt, 
        model=model, 
        output_language="german"
    )   

    critic_agent = ChatAgent(
        system_message=Prompts.critic_prompt, 
        model=model,
        output_language="german"
    )

    return {
        "planner":planner_agent,
        "critic":critic_agent
    }


def initialize_writing_agents(model:BaseModelBackend, story_glossary: StoryGlossary, scene_nr: int) -> dict[ChatAgent]:
    taskmaster_agent : TaskPlannerAgent = TaskPlannerAgent(
        model=model,
        output_language="german"
    )

    writer_agent = ChatAgent(
        system_message=set_writer_prompt(story_glossary),
        model=model,
        token_limit=None,
        output_language="german"
    )

    feedback_agent: ChatAgent = ChatAgent(
        system_message=Prompts.feedback_prompt, 
        model=model,
        output_language="german"
    )
    
    return {
        "taskmaster": taskmaster_agent,
        "writer": writer_agent,
        "feedback": feedback_agent,
    }
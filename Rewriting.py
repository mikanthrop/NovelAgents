
from camel.agents import ChatAgent
from camel.responses import ChatAgentResponse
from datetime import datetime


def rewrite(rewriter: ChatAgent, critic: ChatAgent, writing_file: str) -> str:
    """_summary_

    Args:
        rewriter (ChatAgent): _description_
        critic (ChatAgent): _description_
        writing_file (str): _description_

    Returns:
        str: _description_
    """        
    ## TODO: Check if writing_file is a path to a valid txt file
    text: str
    if ".txt" in writing_file:
        with open(writing_file, "r") as f:
            text = f.read()

    else:
        text = writing_file
        
    loop_nr = 1
    for _ in range(loop_nr):
        critic_msg: ChatAgentResponse = critic.step(f"\nGive feedback to the following text: {text}")
        print(f"\n------\nCritic Response: \n{critic_msg.msg.content}")

        rewriter_msg: ChatAgentResponse = rewriter.step(f"\nCritic feedback: {critic_msg.msg.content}\nText to rewrite: {text}")
        print(f"\n------\nRewriter Response: \n{rewriter_msg.msg.content}")
        text = rewriter_msg.msg.content
    return text


def save_to_txt(written_scenes: dict) -> None:
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"writing_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for key, value in written_scenes.items():
            f.write(f"{key}: {value}\n")

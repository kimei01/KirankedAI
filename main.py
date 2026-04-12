import json
import os
from pathlib import Path
from anthropic import Anthropic as anth
from anthropic.types import Message
from tools import get_ranked_player_details
from toolschema import ALL_TOOLS

client = anth(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(assistant_message)

def add_tool_result_message(messages, result, tool_use_id, is_error):
    messages.append({"role": "user", 
        "content": [{
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": result,
        "is_error": is_error
        }]
    })
    return messages 
def mainChat(messages):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        temperature=0,
        tools = ALL_TOOLS,
        messages=messages,
    )
    return response
def finalChat(messages): 
    finalresponse = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        temperature=0,
        messages=messages,
    )
    return finalresponse.content[0].text

messages = []
while True:
    user_input = input("Enter a Question regarding MCSR Ranked: ")
    if user_input.lower() == "exit":
        break

    if not user_input:
        continue
    #First user message(ignore)
    add_user_message(messages, user_input)
    #Ai response
    response = mainChat(messages)

    #Add assistant message(ignore)
    add_assistant_message(messages, response)
    if response.stop_reason != "tool_use":
        print(messages)
        continue
    if response.stop_reason == "tool_use":
        tool_block = tool_block = next(b for b in response.content if b.type == "tool_use")
        tool_name = tool_block.name
        tool_input = tool_block.input

        result = None
        if tool_name == "get_ranked_player_details":
            try:
                result = get_ranked_player_details(**tool_input)
                is_error = False
            except Exception as e:
                result = str(e)
                is_error = True
        else:
            result = f"Unknown tool: {tool_name}"
            is_error = True
        add_tool_result_message(messages, result, tool_block.id, is_error)
        finalchat = finalChat(messages)
        print(finalchat)




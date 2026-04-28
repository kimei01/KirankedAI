
import os
from pathlib import Path
from anthropic import Anthropic as anth
from anthropic.types import Message
from functions.toolschema import app_tools  



client = anth(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
messages = []
#Loads tools for the session
tools_loader = {tool.name: tool.fn for tool in app_tools}

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

def add_tool_result_message(messages, tool_results):
    content = []
    for res in tool_results: 
        content.append({
            "type": "tool_result",
            "tool_use_id": res['tool_id'],
            "content": res['result'],
            "is_error": res['is_error']
        })
    messages.append({
        "role": "user", 
        "content": content,
    })
    return messages 
def mainChat(messages):
    system_instruction = (
        "You are an expert assistant specializing in Minecraft Speedrunning (MCSR) Ranked. "
        "You have access to tools that fetch player details and leaderboard stats. "
        "Be concise, professional, and use the provided history for context."
        "If you are generating a large table or list, keep it concise to avoid being cut off."
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        temperature=0,
        system=system_instruction,
        tools = app_tools,
        messages=messages,
    )
    return response

def claude():   
    while True:
        user_input = input("Enter a Question regarding MCSR Ranked: ")
        if user_input.lower() == "exit":
            break
        if user_input.lower() == "continue":
            add_user_message(messages, "Please continue your previous response.")
        elif not user_input.strip():
            continue
        else: 
            add_user_message(messages, user_input)

        #If the conversation history exceeds 20 messages, keep only the last 20 to stay within context limits. 
        if len(messages) > 20:
            messages = messages[-20:]
            #Checks if messages contains any text at all and if the first message is a tool result
            while messages and messages[0]['content'][0]['type'] == ["tool_result"]:
                messages = messages[1:]

            
        # This loop keeps going until Claude stops asking for tools
        while True:
            response = mainChat(messages)
            add_assistant_message(messages, response)

            if response.stop_reason == "end_turn": 
                final_text = "".join([b.text for b in response.content if b.type == "text"])
                print(f"\n {final_text}\n")
                break # Exit the loop and wait for the next input()
            if response.stop_reason == "max_tokens":
                final_text = "".join([b.text for b in response.content if b.type == "text"])
                print(f"\n {final_text}")
                print("\n Response reached the limit. Type 'continue' if you need the rest.")  
                break # Exit the loop and wait for the next input()
                
            #Claude wants to use a tool
            if response.stop_reason == "tool_use":
                tool_results = [] 
                # Get tool call (handling multiple tools)
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_id = block.id
                        
                        # Execute tool
                        tool_fn = tools_loader.get(tool_name)
                        try:
                            if tool_fn is None: 
                                raise Exception(f"Tool '{tool_name}' not found.")
                            result = tool_fn(**tool_input)
                            is_error = False
                            
                        except Exception as e:
                            result = str(e)
                            is_error = True
                        
                        # Add result back to messages
                        tool_response_message = { 
                            "result": result, 
                            "tool_id": tool_id,
                            "is_error": is_error,
                        }
                        tool_results.append(tool_response_message)
                add_tool_result_message(messages, tool_results)
                
                
                continue 
            if response.stop_reason not in ("tool_use", "end_turn", "max_tokens"):
                print(f"\n Claude stopped unexpectedly with reason: {response.stop_reason}. Please try again.\n")
                break 
        
     



    




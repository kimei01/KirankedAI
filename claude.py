
import os
from anthropic import Anthropic as anth
from anthropic.types import Message
from functions.tools import tools_loader   
from functions.toolschema import app_tools


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

def process_chat(question, history):  
        add_user_message(history, question)
        # This loop keeps going until Claude stops asking for tools
        while True:
            response = mainChat(history)
            add_assistant_message(history, response)

            if response.stop_reason == "end_turn": 
                final_text = "".join([b.text for b in response.content if b.type == "text"])
                return {"response": final_text, "history": history}
                
            if response.stop_reason == "max_tokens":
                final_text = "".join([b.text for b in response.content if b.type == "text"])
                return {"response": final_text, "history": history, "Error": "Response reached max token limit. Consider rephrasing for a more concise answer."}
            
                
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
                add_tool_result_message(history, tool_results)
                
                
                continue 
            if response.stop_reason not in ("tool_use", "end_turn", "max_tokens"):
                return {"response": response.stop_reason}
                
        
     



    




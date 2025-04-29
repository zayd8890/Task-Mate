# agent.py - Core agent logic
import json
import re
from typing import Dict, Callable, Any
import os
import toml
from deepseek import ChatModel
import toml

config = toml.load('config.toml')
DEEPSEEK_API = config['secrets']['DEEPSEEK_API']


class Agent:
    def __init__(self, tools: Dict[str, Callable],api_key=DEEPSEEK_API):
        self.tools = tools
        self.conversation_history = []
        self.api_key = api_key

        self.deepseek_model = ChatModel(
                    api_key=api_key,  
                    model="deepseek-chat",             
                )
        
        
    def process(self, user_input: str) -> str:
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
         
        # Create system message with tool descriptions
        system_message = self._create_system_message()
        
        # Generate response from LLM
        messages = [system_message] + self.conversation_history
        
        try:
            # Call DeepSeek API to get the response
            completion = self.deepseek_model.chat(
                messages=messages,
                temperature=0.7,  # You can tweak these parameters as needed
                max_tokens=512
            )

            
            # Extract the assistant's response
            assistant_response = completion['choices'][0]['message']['content']
            
            # Check if the response contains a tool call
            tool_call_match = re.search(r'```tool\s+(.*?)\s+(.*?)```', assistant_response, re.DOTALL)
            
            if tool_call_match:
                # Extract tool name and parameters
                tool_name = tool_call_match.group(1).strip()
                tool_params_str = tool_call_match.group(2).strip()
                
                # Execute the tool
                tool_result = self._execute_tool(tool_name, tool_params_str)
                
                # Replace the tool call with the result
                clean_response = assistant_response.replace(tool_call_match.group(0), f"I used {tool_name} and got: {tool_result}")
            else:
                clean_response = assistant_response
                
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": clean_response})
            
            return clean_response
            
        except Exception as e:
            error_message = f"Error processing request: {str(e)}"
            self.conversation_history.append({"role": "assistant", "content": error_message})
            return error_message
    
    def _create_system_message(self) -> dict:
        tools_description = ""
        for tool_name, tool_func in self.tools.items():
            tools_description += f"- {tool_name}: {tool_func.__doc__ or 'No description available'}\n"
        
        system_content = f"""
        You are SmolaGent, a helpful AI assistant with access to tools.
        
        Available tools:
        {tools_description}
        
        When you need to use a tool, use the following format:
        ```tool tool_name
        parameters in JSON format
        ```
        
        Always respond in a helpful, safe, and ethical manner.
        """
        
        return {"role": "system", "content": system_content.strip()}
    
    def _execute_tool(self, tool_name: str, params_str: str) -> Any:
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        
        try:
            # Parse parameters as JSON
            params = json.loads(params_str)
            
            # Execute the tool with the parameters
            result = self.tools[tool_name](**params)
            
            return result
        except json.JSONDecodeError:
            return f"Error: Invalid JSON parameters for tool '{tool_name}'"
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
# main.py - Main orchestration script with task management integration
import os
import json
from tools import web_search, calculator, file_operations, task_manager
from agent import Agent
import toml

config = toml.load('config.toml')
DEEPSEEK_API = config['secrets']['DEEPSEEK_API']
def main():
    # Initialize agent with available tools
    agent = Agent(
        tools={
            # Original tools
            "web_search": web_search.search,
            "calculator": calculator.calculate,
            "read_file": file_operations.read_file,
            "write_file": file_operations.write_file,
            
            # Task management tools
            "decompose_task": task_manager.decompose_task,
            "prioritize_tasks": task_manager.prioritize_tasks,
            "schedule_tasks": task_manager.schedule_tasks,
            "visualize_tasks": task_manager.visualize_tasks,
            "run_task_script": task_manager.run_task_script
        },
        api_key=DEEPSEEK_API
    )
    
    print("🤖 SmolaGent AI Assistant initialized. Type 'exit' to quit.")
    print("🔧 Enhanced with Task Management capabilities!")
    
    while True:
        user_input = input("\n👤 User: ")
        if user_input.lower() == 'exit':
            print("🤖 SmolaGent: Goodbye!")
            break
            
        response = agent.process(user_input)
        print(f"\n🤖 SmolaGent: {response}")

if __name__ == "__main__":
    main()
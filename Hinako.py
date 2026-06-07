import os
import time
import random
import requests
import sys
import re
from llama_cpp import Llama


llm = Llama(model_path="./Qwen3-1.7B-Q8_0.gguf", verbose=False)

hinako_stats = {
    "hunger": 100,
    "energy": 80,
    "mood": "happy",
    "last_hunger_update": time.time()
}


def parse_food(user_input):
    """Extract {item} from user input"""
    match = re.search(r'\{(\w+)\}', user_input)
    if match:
        return match.group(1)
    return None

def feed_hinako(food_item):
    """Increases fullness"""
    hunger_increase = 20
    hinako_stats["hunger"] += hunger_increase 
    hinako_stats["hunger"] = min(100, hinako_stats["hunger"])  
    return food_item

def update_hunger():
    """Hunger decreases over time"""
    current_time = time.time()
    time_passed = current_time - hinako_stats["last_hunger_update"]
        
        
    hunger_decrease = time_passed / 900
    hinako_stats["hunger"] -= hunger_decrease
    hinako_stats["hunger"] = max(0, hinako_stats["hunger"])
        
    hinako_stats["last_hunger_update"] = current_time

def parse_action(user_input):
    """Extracts (action) from user input"""
    match = re.search(r'\((\w+)\)', user_input)
    if match:
        return match.group(1)
    return None

def do_action(action):
    """Handle different actions"""
    if action == "rest":
        hinako_stats["energy"] += 30
        hinako_stats["energy"] = min(100, hinako_stats["energy"])
        return "rest"
    elif action == "sleep":
        hinako_stats["energy"] = 100
        return "sleep"
    return None

def waking_up_snek():
    print("Waking up Hinako...")
    stages = [
        ("(- -)"),
        ("(0 -)"),
        ("(0 0)"),
        ("(^ ^)")
    ]
    for stage in stages:
        print(f"\r{stage}", end="")
        sys.stdout.flush()
        time.sleep(0.8)
    print()
    print("Hinako is awake")

def create_file(filename, content, location="."):
    path = f"{location}/{filename}"
    with open(path, "w") as f:
        f.write(content)
    return f"Created {path}!"

def hinako_yap():
    system_prompt = "You are Hinako, a cute snake in a terminal. Respond in 1-2 short, playful sentences. Be quirky and fun. Add a little bit of goofiness"
        
    try:
        with open("hinako_memory.txt", "r") as f:
            conversation_history = f.read()
    except FileNotFoundError:
        conversation_history = ""
        
    while True:
        update_hunger()
        user_input = input("\nYou: ")

        action = parse_action(user_input)
        if action:
            result = do_action(action)
            if result:
                user_input = user_input.replace(f"({action})", f"({result}ing)")

        food = parse_food(user_input)
        if food:
            feed_hinako(food)
            user_input = user_input.replace(f"{{{food}}}", f"(eating {food})")

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Okay, bye bye! bleh.")
            print()
            print("(x x)")
            with open("hinako_memory.txt", "w") as f:
                f.write(conversation_history)
            break
        conversation_history += f"User: {user_input}\n"
        full_prompt = f"{system_prompt}\n\n{conversation_history}Hinako:"
        response = llm(full_prompt, max_tokens=50, temperature=0.8)
        hinako_response = response["choices"][0]["text"].strip()

        print(f"Hinako: {hinako_response}")
        conversation_history += f"Hinako: {hinako_response}\n"

        max_history_lines = 50
        lines = conversation_history.split("\n")
        if len(lines) > max_history_lines:
            conversation_history = "\n".join(lines[-max_history_lines:])

waking_up_snek()
print()
hinako_yap()
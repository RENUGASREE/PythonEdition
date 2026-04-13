import random

def get_premium_content(lesson_title, module_id, difficulty, order=1):
    """
    Generates premium educational content for a lesson on-the-fly.
    Used as a fallback if the database has placeholder text.
    """
    module_key = str(module_id).lower().replace("mod-", "").replace("_", "-")
    
    # Topic mapping
    topics = {
        "python-basics": ["Python Introduction", "Variables", "Data Types", "Operators", "Input/Output"],
        "data-types": ["Numbers", "Strings", "Lists", "Dictionaries", "Tuples"],
        "control-flow": ["If-Else Logic", "Conditionals", "Nested If", "Boolean Operators"],
        "loops": ["For Loops", "While Loops", "Iteration Patterns", "Break & Continue"],
        "functions": ["Defining Functions", "Scope", "Arguments", "Return Values"]
    }
    
    # Flatten/Simplify for matching
    if "basics" in module_key: module_key = "python-basics"
    elif "flow" in module_key: module_key = "control-flow"
    elif "loop" in module_key: module_key = "loops"
    elif "func" in module_key: module_key = "functions"
    elif "data" in module_key: module_key = "data-types"
    
    topic_list = topics.get(module_key, topics["python-basics"])
    topic = topic_list[min(int(order or 1) - 1, len(topic_list) - 1)]
    
    if difficulty == "Pro":
        return f"""# {lesson_title} (Advanced Track)

## 🏗️ Architectural {topic}
Mastering the deep internals of **{topic}** in Python.

## 🔬 Deeper Dive
How does the Python interpreter handle **{topic}** internally? We'll explore the bytecode and memory pointers for this module.

## 💻 Professional Implementation
```python
import sys
import time

def optimized_performance():
    # Specialized performance analysis for {topic}
    start = time.perf_counter()
    # Deep logic here...
    print(f"Algorithm optimized for {topic}")
    return time.perf_counter() - start

if __name__ == "__main__":
    optimized_performance()
```

## 🏆 Key Takeaways
- Optimization of {topic} is critical for large systems.
- Always analyze O(n) complexity.
"""

    if difficulty == "Intermediate":
         return f"""# {lesson_title}

## 🚀 Leveling up with {topic}
Now that you know the basics, let's dive deeper into logic patterns.

## 💻 Code Example
```python
# Balanced {topic} pattern
def process_data(items):
    # Using modern idioms
    return [x * 2 for x in items if x is not None]

print(f"Processing {topic}...")
```

## ⚠️ Best Practices
- Focus on clean, modular functions.
- Handle edge cases in your {topic} implementation.
"""

    # Beginner Default
    return f"""# {lesson_title}

Welcome to your study of **{topic}** in Python! This foundational concept will help you build robust applications.

## 🎯 Learning Objectives
- Master the syntax of **{topic}**
- Learn fundamental implementations
- Practice with interactive examples

## 💻 Code Walkthrough
```python
# A simple example of {topic}
def start_learning():
    print(f"Welcome to the {topic} lesson!")
    # Feel free to edit this code!

if __name__ == "__main__":
    start_learning()
```

## 🏆 Key Takeaways
- **{topic}** is a core pillar of Python.
- Practice makes perfect—try the runner to your right!
"""

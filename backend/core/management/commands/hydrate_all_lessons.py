from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge
import random

class Command(BaseCommand):
    help = "Hydrate all 300 lessons with content, quizzes, and challenges"

    def handle(self, *args, **options):
        # Module content templates for generating lesson content
        module_topics = {
            "python-basics": ["Python Introduction", "Variables", "Data Types", "Operators", "Input/Output", "Comments", "Indentation", "Basic Syntax", "Error Basics", "Python Environment"],
            "data-types": ["Numbers", "Strings", "Lists", "Tuples", "Dictionaries", "Sets", "Type Conversion", "None Type", "Boolean Logic", "Type Checking"],
            "control-flow": ["If Statements", "Else/Elif", "Nested If", "While Loops", "For Loops", "Break/Continue", "Pass Statement", "Loop Patterns", "Boolean Logic", "Conditionals"],
            "functions": ["Defining Functions", "Parameters", "Return Values", "Scope", "Lambda", "Recursion", "Decorators", "Default Args", "Variable Args", "Functions Overview"],
            "modules-packages": ["Import Statements", "From Import", "Module Structure", "Packages", "__init__.py", "Standard Library", "PIP", "Virtual Environments", "Module Search Path", "Package Management"],
            "file-handling": ["Open Files", "Read Files", "Write Files", "File Modes", "With Statement", "File Paths", "File Methods", "CSV Files", "JSON Files", "File Operations"],
            "error-handling": ["Try/Except", "Exception Types", "Finally Block", "Raise Exceptions", "Custom Exceptions", "Error Messages", "Debugging", "Logging", "Assert Statements", "Exception Handling"],
            "oop": ["Classes", "Objects", "Constructors", "Methods", "Inheritance", "Polymorphism", "Encapsulation", "Class Methods", "Static Methods", "OOP Principles"],
            "advanced-python": ["Generators", "Iterators", "Decorators", "Context Managers", "Metaclasses", "Property", "Descriptors", "Abstract Classes", "Multiple Inheritance", "Advanced Features"],
            "real-world-projects": ["Project Structure", "CLI Applications", "Web Scraping", "APIs", "Data Processing", "Automation", "Testing", "Deployment", "Best Practices", "Project Development"]
        }

        difficulties = ["Beginner", "Intermediate", "Pro"]
        
        count = 0
        with transaction.atomic():
            lessons = Lesson.objects.all()
            self.stdout.write(f"Found {lessons.count()} lessons to hydrate")
            
            for lesson in lessons:
                # Force update all lessons with proper content
                
                # Generate content based on module, lesson number, and difficulty
                module_id = lesson.module_id
                module_key = module_id.replace("mod-", "")
                
                # Get topic based on lesson order (1-10)
                lesson_order = lesson.order if lesson.order else 1
                topic_list = module_topics.get(module_key, ["General Topic"])
                topic = topic_list[min(lesson_order - 1, len(topic_list) - 1)]
                
                # Generate content based on difficulty
                difficulty = lesson.difficulty or "Beginner"
                
                if difficulty == "Beginner":
                    content = self.generate_beginner_content(lesson.title, topic, module_key)
                elif difficulty == "Intermediate":
                    content = self.generate_intermediate_content(lesson.title, topic, module_key)
                else:  # Pro
                    content = self.generate_pro_content(lesson.title, topic, module_key)
                
                # Update lesson content
                lesson.content = content
                lesson.save(update_fields=["content"])
                
                # Create or update quiz
                quiz, _ = Quiz.objects.get_or_create(
                    id=f"quiz-{lesson.id}",
                    defaults={"lesson_id": lesson.id, "title": f"Quiz: {lesson.title}"}
                )
                
                # Add questions
                Question.objects.filter(quiz_id=quiz.id).delete()
                for i in range(3):  # 3 questions per lesson
                    Question.objects.create(
                        id=f"q-{lesson.id}-{i+1}",
                        quiz_id=quiz.id,
                        text=self.generate_question(topic, difficulty),
                        type="mcq",
                        options=self.generate_options(),
                        points=5,
                    )
                
                # Create challenge
                Challenge.objects.update_or_create(
                    lesson_id=lesson.id,
                    defaults={
                        "title": f"{topic} Challenge",
                        "description": f"Complete the {topic} exercise",
                        "initial_code": "# Write your solution here\n",
                        "solution_code": "# Solution placeholder\nprint('Challenge completed!')",
                        "test_cases": [{"input": "", "expected": "Challenge completed!"}],
                        "points": 20,
                    }
                )
                
                count += 1
                if count % 50 == 0:
                    self.stdout.write(f"  Processed {count} lessons...")
        
        self.stdout.write(self.style.SUCCESS(f"\nHydrated {count} lessons with content, quizzes, and challenges"))

    def generate_beginner_content(self, title, topic, module):
        return f"""# {title}

Welcome to your study of **{topic}** in Python! This foundational concept will help you build robust applications.

## 🎯 Learning Objectives
- Master the basic syntax of **{topic}**
- Learn how to implement simple logic safely
- Practice with interactive examples

## 📚 Concept Overview
In Python, **{topic}** allows you to structure your code efficiently. 
For {module.replace('-', ' ').title()}, we focus on reliability and readability.

## 💻 Code Walkthrough
```python
# A simple example of {topic}
def showcase():
    print(f"Starting our {topic} journey!")
    # Implementation follows:
    val = 10
    print(f"Value is: {{val}}")

if __name__ == "__main__":
    showcase()
```

## 🏆 Key Takeaways
- **{topic}** is a core pillar of Python.
- Always aim for clean, readable code.
- Practice makes perfect—try the interactive runner to your right!
"""

    def generate_intermediate_content(self, title, topic, module):
        return f"""# {title}

## 🚀 Leveling up with {topic}
Now that you know the basics, let's dive deeper into the optimization and patterns of **{topic}**.

## 💻 Intermediate Example
```python
# Optimized {topic} pattern
def process_data(items):
    # Using modern Python idioms for {topic}
    result = [x * 2 for x in items if x is not None]
    return result

data = [1, 2, 3, None, 5]
print(f"Processed {topic}: {{process_data(data)}}")
```

## ⚠️ Best Practices
- Use list comprehensions where appropriate.
- Modularize your {topic} logic into functions.
- Handle edge cases and None types early.
"""

    def generate_pro_content(self, title, topic, module):
        return f"""# {title}

## 🏗️ Architectural {topic}
At the Pro level, we analyze the performance characteristics and memory management of **{topic}**.

## 🔬 Deeper Dive
How does the Python interpreter handle **{topic}** internally? We'll explore the bytecode and memory pointers for {module.replace('-', ' ').title()}.

## 💻 Professional implementation
```python
import sys
import time

def optimized_logic():
    # Specialized performance analysis for {topic}
    start = time.perf_counter()
    # Complex implementation here
    end = time.perf_counter()
    print(f"Execution time: {{end - start:.6f}}s")

if __name__ == "__main__":
    optimized_logic()
```
"""

    def generate_question(self, topic, difficulty):
        beginner_questions = [
            f"Which of these correctly defines {topic} in Python?",
            f"What is the first step when implementing {topic}?",
            f"How do you print a value related to {topic}?",
        ]
        intermediate_questions = [
            f"What is the most efficient way to handle {topic} at scale?",
            f"How does {topic} interact with other data structures?",
            f"Which Python PEP discusses standards for {topic}?",
        ]
        pro_questions = [
            f"Describe the memory complexity of your {topic} implementation.",
            f"How would you refactor a legacy {topic} block for concurrency?",
            f"What is the internal CPython opcode for {topic}?",
        ]
        
        if difficulty == "Beginner":
            return random.choice(beginner_questions)
        elif difficulty == "Intermediate":
            return random.choice(intermediate_questions)
        return random.choice(pro_questions)

    def generate_options(self):
        options = [
            "Using the built-in function",
            "Via a custom loop structure",
            "By importing the 'math' module",
            "All of the above"
        ]
        random.shuffle(options)
        return [
            {"text": options[0], "correct": True},
            {"text": options[1], "correct": False},
            {"text": options[2], "correct": False},
            {"text": options[3], "correct": False},
        ]

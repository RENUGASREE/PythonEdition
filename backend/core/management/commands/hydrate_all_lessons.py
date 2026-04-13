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
                # Skip if already has substantial content (not placeholder)
                if lesson.content and len(lesson.content) > 200 and "will be added here" not in lesson.content:
                    continue
                
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

## 🎯 Learning Objectives
- Understand the basics of {topic}
- Learn fundamental concepts
- Practice with simple examples

## 📚 Concept Overview
{topic} is a fundamental concept in {module.replace('-', ' ').title()}. 
This lesson introduces the core ideas you need to get started.

## 💻 Code Walkthrough
```python
# Basic example for {topic}
# Add your code here
print("Learning {topic}")
```

## ⚠️ Common Pitfalls
- Forgetting basic syntax
- Not understanding the concept fully
- Skipping practice exercises

## 🏆 Key Takeaways
- {topic} is essential for Python programming
- Practice regularly to master the concept
- Build on this foundation for advanced topics
"""

    def generate_intermediate_content(self, title, topic, module):
        return f"""# {title}

## 🎯 Learning Objectives
- Master {topic} at an intermediate level
- Understand practical applications
- Learn best practices

## 📚 Concept Overview
{topic} in {module.replace('-', ' ').title()} involves deeper understanding 
and practical implementation patterns.

## 💻 Code Walkthrough
```python
# Intermediate example for {topic}
def process_{topic.lower().replace(' ', '_')}():
    # Implementation details
    pass
```

## ⚠️ Common Pitfalls
- Over-complicating simple solutions
- Not considering edge cases
- Ignoring performance implications

## 🏆 Key Takeaways
- {topic} requires practice and experience
- Follow established patterns and conventions
- Test your code thoroughly
"""

    def generate_pro_content(self, title, topic, module):
        return f"""# {title}

## 🎯 Learning Objectives
- Master advanced {topic} techniques
- Understand internal implementation
- Optimize for performance

## 📚 Concept Overview
Advanced {topic} explores the internals and optimization strategies 
for {module.replace('-', ' ').title()}.

## 💻 Code Walkthrough
```python
# Advanced example for {topic}
class {topic.replace(' ', '')}Advanced:
    def __init__(self):
        # Advanced implementation
        pass
    
    def optimize(self):
        # Performance optimization
        pass
```

## ⚠️ Common Pitfalls
- Premature optimization
- Ignoring readability for performance
- Not profiling before optimizing

## 🏆 Key Takeaways
- {topic} at advanced level requires deep understanding
- Balance performance with maintainability
- Use profiling tools to guide optimization
"""

    def generate_question(self, topic, difficulty):
        questions = {
            "Beginner": [
                f"What is the primary purpose of {topic}?",
                f"Which statement is true about {topic}?",
                f"How do you use {topic} in Python?",
            ],
            "Intermediate": [
                f"What is the best practice when working with {topic}?",
                f"Which method would you use for {topic}?",
                f"How does {topic} affect program performance?",
            ],
            "Pro": [
                f"What is the internal implementation of {topic}?",
                f"Which optimization strategy works best for {topic}?",
                f"How would you design a system using {topic}?",
            ]
        }
        return random.choice(questions.get(difficulty, questions["Beginner"]))

    def generate_options(self):
        return [
            {"text": "Option A", "correct": True},
            {"text": "Option B", "correct": False},
            {"text": "Option C", "correct": False},
            {"text": "Option D", "correct": False},
        ]

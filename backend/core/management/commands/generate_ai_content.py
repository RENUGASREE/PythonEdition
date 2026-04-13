from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Module
import openai
import os
from django.conf import settings

class Command(BaseCommand):
    help = "Generate lesson content using OpenAI API"

    def handle(self, *args, **options):
        # Get OpenAI API key from environment
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            self.stdout.write(self.style.ERROR("OPENAI_API_KEY environment variable not set"))
            return
        
        openai.api_key = api_key

        # Get all lessons
        lessons = Lesson.objects.all()
        self.stdout.write(f"Generating content for {lessons.count()} lessons using OpenAI...")
        
        # Module topics for content generation
        module_topics = {
            "python-basics": ["Variables and Data Types", "Operators", "Input/Output", "Comments", "Indentation", "Basic Syntax", "String Operations", "Number Operations", "Type Conversion", "Basic Operations"],
            "data-types": ["Lists", "Tuples", "Sets", "Dictionaries", "Strings", "Numbers", "Boolean", "None Type", "Type Checking", "Data Type Conversion"],
            "control-flow": ["If Statements", "If-Else", "If-Elif-Else", "Nested If", "Logical Operators", "Comparison Operators", "Ternary Operator", "Match Case", "Short-circuiting", "Condition Best Practices"],
            "loops": ["For Loops", "While Loops", "Range Function", "Break Statement", "Continue Statement", "Nested Loops", "Loop Else", "Iterators", "Comprehensions", "Loop Patterns"],
            "functions": ["Function Definition", "Parameters", "Return Values", "Default Parameters", "Keyword Arguments", "Variable Arguments", "Lambda Functions", "Scope", "Closures", "Decorators"],
            "modules-packages": ["Import Statements", "From Import", "Import Alias", "Standard Library Modules", "Creating Modules", "Packages", "__init__.py", "Relative Imports", "Absolute Imports", "Package Distribution"],
            "file-handling": ["Open Files", "Read Files", "Write Files", "File Modes", "With Statement", "File Methods", "File Paths", "Directory Operations", "File Permissions", "Error Handling"],
            "error-handling": ["Try-Except", "Exception Types", "Finally Block", "Raise Exceptions", "Custom Exceptions", "Exception Chaining", "Context Managers", "Debugging", "Logging", "Error Best Practices"],
            "oop": ["Classes and Objects", "Constructors", "Instance Methods", "Class Methods", "Static Methods", "Inheritance", "Polymorphism", "Encapsulation", "Abstraction", "OOP Principles"],
            "advanced-python": ["Generators", "Iterators", "Decorators", "Context Managers", "Metaclasses", "Descriptors", "Property Decorators", "Class Methods", "Static Methods", "Advanced Patterns"],
            "real-world-projects": ["Project Structure", "CLI Applications", "Web Scraping", "Data Analysis", "API Integration", "Database Projects", "Automation Scripts", "Testing", "Deployment", "Project Documentation"]
        }

        count = 0
        with transaction.atomic():
            for lesson in lessons:
                module_key = lesson.module_id.replace("mod-", "")
                topic_list = module_topics.get(module_key, ["General Topic"])
                topic = topic_list[min(lesson.order - 1, len(topic_list) - 1)]
                
                difficulty = lesson.difficulty or "Beginner"
                module_obj = Module.objects.filter(id=lesson.module_id).first()
                module_name = module_obj.title if module_obj else "Python"
                
                # Generate content based on difficulty
                if difficulty == "Beginner":
                    content = self.generate_beginner_content(lesson.title, topic, module_name)
                elif difficulty == "Intermediate":
                    content = self.generate_intermediate_content(lesson.title, topic, module_name)
                else:
                    content = self.generate_pro_content(lesson.title, topic, module_name)
                
                # Update lesson content
                lesson.content = content
                lesson.save(update_fields=["content"])
                
                count += 1
                if count % 10 == 0:
                    self.stdout.write(f"  Generated content for {count} lessons...")
        
        self.stdout.write(self.style.SUCCESS(f"\nGenerated AI content for {count} lessons"))

    def generate_beginner_content(self, title, topic, module):
        prompt = f"""Generate a beginner-friendly Python lesson about "{topic}" in the context of "{module}".
        
The lesson title is "{title}".

Generate comprehensive educational content including:
1. Clear explanation of the concept
2. Simple code examples with explanations
3. Step-by-step breakdown
4. Common mistakes to avoid
5. Practice exercise

Format the content in Markdown with proper headings, code blocks, and examples.
Keep it simple and easy to understand for beginners."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Python programming instructor creating educational content for beginners."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"OpenAI API error for {title}: {e}"))
            return self.generate_fallback_beginner_content(title, topic, module)

    def generate_intermediate_content(self, title, topic, module):
        prompt = f"""Generate an intermediate-level Python lesson about "{topic}" in the context of "{module}".
        
The lesson title is "{title}".

Generate comprehensive educational content including:
1. In-depth explanation of the concept
2. Real-world use cases
3. Code examples with explanations
4. Best practices
5. Advanced techniques
6. Practice challenge

Format the content in Markdown with proper headings, code blocks, and examples.
Target audience: Developers with some Python experience."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Python programming instructor creating educational content for intermediate developers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"OpenAI API error for {title}: {e}"))
            return self.generate_fallback_intermediate_content(title, topic, module)

    def generate_pro_content(self, title, topic, module):
        prompt = f"""Generate an advanced/pro-level Python lesson about "{topic}" in the context of "{module}".
        
The lesson title is "{title}".

Generate comprehensive educational content including:
1. Advanced concepts and patterns
2. Performance optimization techniques
3. Production-ready code examples
4. Edge cases and error handling
5. Integration with other Python features
6. Complex practice challenge

Format the content in Markdown with proper headings, code blocks, and examples.
Target audience: Experienced Python developers."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Python programming instructor creating educational content for advanced developers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"OpenAI API error for {title}: {e}"))
            return self.generate_fallback_pro_content(title, topic, module)

    def generate_fallback_beginner_content(self, title, topic, module):
        return f"""# {title}

## Overview
This lesson covers {topic} in the context of {module}. This is a beginner-friendly introduction to help you understand the fundamentals.

## What You'll Learn
- Basic concepts of {topic}
- Simple examples and use cases
- How to apply {topic} in your code

## Explanation
{topic} is an important concept in {module}. Understanding this will help you write better Python code.

## Code Example
```python
# Example of {topic}
def example_function():
    # Your code here
    pass

# Call the function
example_function()
```

## Practice Exercise
Try implementing a simple example of {topic} in your own code.

## Summary
In this lesson, you learned the basics of {topic} and how to use it in your Python programs.
"""

    def generate_fallback_intermediate_content(self, title, topic, module):
        return f"""# {title}

## Overview
This intermediate lesson explores {topic} in the context of {module}. You'll learn advanced techniques and best practices.

## Learning Objectives
- Deep understanding of {topic}
- Real-world applications
- Performance considerations
- Best practices

## In-Depth Explanation
{topic} is a powerful feature in {module} that allows you to write more efficient and maintainable code.

## Advanced Examples
```python
# Advanced example of {topic}
class AdvancedExample:
    def __init__(self):
        self.data = []
    
    def process_data(self):
        # Implementation
        pass

# Usage
example = AdvancedExample()
example.process_data()
```

## Best Practices
- Always consider performance implications
- Handle edge cases properly
- Write clean, readable code
- Test thoroughly

## Practice Challenge
Create a project that uses {topic} to solve a real-world problem.

## Summary
You've now mastered intermediate concepts of {topic} and can apply them in production code.
"""

    def generate_fallback_pro_content(self, title, topic, module):
        return f"""# {title}

## Overview
This advanced lesson covers {topic} at a professional level in the context of {module}. You'll learn production-ready techniques.

## Advanced Concepts
- Deep dive into {topic} internals
- Performance optimization
- Memory management
- Concurrency considerations
- Integration patterns

## Production-Ready Examples
```python
# Production example of {topic}
import asyncio
from typing import Optional

class ProductionClass:
    def __init__(self, config: dict):
        self.config = config
        self._cache = dict()
    
    async def process(self, data: dict) -> Optional[dict]:
        # Async implementation
        pass

# Usage
async def main():
    instance = ProductionClass(dict())
    result = await instance.process(dict())
```

## Performance Optimization
- Use appropriate data structures
- Minimize memory usage
- Implement caching strategies
- Profile and optimize hot paths

## Edge Cases & Error Handling
- Handle all possible exceptions
- Validate inputs thoroughly
- Implement graceful degradation
- Add comprehensive logging

## Complex Challenge
Build a production system that leverages {topic} to handle high-scale operations.

## Summary
You've mastered advanced {topic} concepts and can implement production-grade solutions.
"""

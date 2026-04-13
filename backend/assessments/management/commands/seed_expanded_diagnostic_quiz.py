from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import DiagnosticQuiz, DiagnosticQuestion

class Command(BaseCommand):
    help = "Seed 50 diagnostic questions covering all 10 modules"

    def handle(self, *args, **options):
        quiz, _ = DiagnosticQuiz.objects.get_or_create(title="Python Placement Diagnostic - Expanded")
        DiagnosticQuestion.objects.filter(quiz=quiz).delete()

        def q(text, opts, correct_letter, difficulty, topic, points):
            letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}
            return DiagnosticQuestion(
                quiz=quiz,
                text=text.strip(),
                options=opts,
                correct_index=letter_to_index[correct_letter],
                difficulty=difficulty,
                topic=topic,
                points=points,
            )

        questions = [
            # Module 1: Python Basics (5 questions)
            q("What is the correct way to assign a value to a variable?", ["int x = 5", "x = 5", "var x = 5", "let x = 5"], "B", "easy", "Python Basics", 1),
            q("What is the output of print(type(3.14)) ?", ["float", "<class 'float'>", "decimal", "number"], "B", "easy", "Python Basics", 1),
            q("Which data type is immutable?", ["list", "dictionary", "tuple", "set"], "C", "medium", "Python Basics", 2),
            q('What is the result of "5" + "5" ?', ["10", "55", "Error", "5"], "B", "medium", "Python Basics", 2),
            q("What does `len('hello')` return?", ["4", "5", "6", "Error"], "B", "easy", "Python Basics", 1),
            
            # Module 2: Data Types (5 questions)
            q("What is the result of `type([1, 2, 3])`?", ["list", "tuple", "array", "set"], "A", "easy", "Data Types", 1),
            q("Which data structure stores key-value pairs?", ["list", "dictionary", "tuple", "set"], "B", "easy", "Data Types", 1),
            q("What does `set([1, 2, 2, 3])` return?", ["[1, 2, 2, 3]", "{1, 2, 3}", "(1, 2, 3)", "[1, 2, 3]"], "B", "medium", "Data Types", 2),
            q("How do you access the first element of a list?", ["list[0]", "list[1]", "list.first()", "list.get(0)"], "A", "easy", "Data Types", 1),
            q("What is a tuple in Python?", ["Mutable list", "Immutable sequence", "Key-value store", "Mutable set"], "B", "medium", "Data Types", 2),
            
            # Module 3: Control Flow (5 questions)
            q("Which keyword is used for condition checking?", ["switch", "if", "case", "loop"], "B", "easy", "Control Flow", 1),
            q("What prints?\nif 0:\n    print(\"Yes\")\nelse:\n    print(\"No\")", ["Yes", "No", "Error", "Nothing"], "B", "medium", "Control Flow", 2),
            q("Equality operator?", ["=", "==", ":=", "!="], "B", "medium", "Control Flow", 2),
            q("What does pass do?", ["Skips program", "Placeholder statement", "Ends loop", "Continues loop"], "B", "hard", "Control Flow", 3),
            q("Nested loop complexity n x n?", ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "C", "hard", "Control Flow", 3),
            
            # Module 4: Loops (5 questions)
            q("range(3) produces?", ["1,2,3", "0,1,2", "0,1,2,3", "3 values undefined"], "B", "easy", "Loops", 1),
            q("break does what?", ["Stops loop entirely", "Skips iteration", "Pauses loop", "Restarts loop"], "A", "medium", "Loops", 2),
            q("continue does what?", ["Ends program", "Skips current iteration", "Restarts loop", "Stops loop"], "B", "medium", "Loops", 2),
            q("Infinite loop example?", ["while True:", "for i in range(0)", "if True", "break"], "A", "hard", "Loops", 3),
            q("Output of for i in range(1,4)?", ["1 2 3", "0 1 2", "1 2 3 4", "Error"], "A", "easy", "Loops", 1),
            
            # Module 5: Functions (5 questions)
            q("Correct function definition?", ["function myFunc()", "def myFunc():", "define myFunc():", "func myFunc():"], "B", "easy", "Functions", 1),
            q("Return without value returns?", ["0", "None", "False", "Error"], "B", "medium", "Functions", 2),
            q("Lambda is?", ["Loop", "Anonymous function", "Class", "Module"], "B", "medium", "Functions", 2),
            q("Default mutable argument issue example?", ["It resets each call", "It persists between calls", "It raises error", "It returns copy"], "B", "hard", "Functions", 3),
            q("Recursion means?", ["Loop", "Function calling itself", "Condition", "Class"], "B", "hard", "Functions", 3),
            
            # Module 6: Modules & Packages (5 questions)
            q("How do you import a module?", ["import module", "require module", "include module", "using module"], "A", "easy", "Modules & Packages", 1),
            q("What does `from math import sqrt` do?", ["Imports entire math", "Imports only sqrt", "Creates math module", "Errors"], "B", "medium", "Modules & Packages", 2),
            q("What is __init__.py used for?", ["Package initialization", "Main function", "Class definition", "Variable declaration"], "A", "medium", "Modules & Packages", 2),
            q("How do you create a package?", ["Folder with __init__.py", "Single .py file", "Folder without __init__.py", "Any folder"], "A", "medium", "Modules & Packages", 2),
            q("What is pip used for?", ["Package management", "Code execution", "Testing", "Documentation"], "A", "easy", "Modules & Packages", 1),
            
            # Module 7: File Handling (5 questions)
            q("How do you open a file for reading?", ["open('file.txt', 'r')", "read('file.txt')", "file('file.txt')", "load('file.txt')"], "A", "easy", "File Handling", 1),
            q("What method reads entire file as string?", ["read()", "readline()", "readlines()", "load()"], "A", "easy", "File Handling", 1),
            q("How do you close a file?", ["file.close()", "close(file)", "file.end()", "file.stop()"], "A", "easy", "File Handling", 1),
            q("What is the with statement used for?", ["Automatic file closing", "File opening only", "File deletion", "File copying"], "A", "medium", "File Handling", 2),
            q("What does 'w' mode do?", ["Write (overwrite)", "Write (append)", "Read only", "Read and write"], "A", "medium", "File Handling", 2),
            
            # Module 8: Error Handling (5 questions)
            q("How do you handle exceptions?", ["try/except", "if/else", "catch/throw", "error/handle"], "A", "easy", "Error Handling", 1),
            q("What exception is raised for division by zero?", ["ZeroDivisionError", "DivisionError", "MathError", "ValueError"], "A", "medium", "Error Handling", 2),
            q("What does finally block do?", ["Always executes", "Only on error", "Only on success", "Never executes"], "A", "medium", "Error Handling", 2),
            q("How do you raise an exception?", ["raise Exception()", "throw Exception()", "error Exception()", "throw new Exception()"], "A", "medium", "Error Handling", 2),
            q("What is the purpose of custom exceptions?", ["Handle specific errors", "Replace all errors", "Ignore errors", "Speed up code"], "A", "hard", "Error Handling", 3),
            
            # Module 9: OOP (5 questions)
            q("Class is?", ["Object", "Blueprint for objects", "Variable", "Loop"], "B", "easy", "OOP", 1),
            q("__init__ is?", ["Destructor", "Constructor", "Loop", "Variable"], "B", "medium", "OOP", 2),
            q("Inheritance means?", ["Copy code", "Child derives from parent", "Delete class", "Override variable"], "B", "medium", "OOP", 2),
            q("Method overriding means?", ["Duplicate method", "Child redefines parent method", "Delete method", "None"], "B", "hard", "OOP", 3),
            q("Encapsulation means?", ["Hide internal implementation", "Delete variables", "Loop logic", "Multiple inheritance"], "A", "hard", "OOP", 3),
            
            # Module 10: Advanced Python (5 questions)
            q("What is a decorator?", ["Function modifier", "Data type", "Loop", "Variable"], "A", "medium", "Advanced Python", 2),
            q("What does @property do?", ["Creates property method", "Private variable", "Static method", "Class method"], "A", "medium", "Advanced Python", 2),
            q("What is a generator?", ["Function with yield", "Loop", "Class", "Variable"], "A", "medium", "Advanced Python", 2),
            q("What is list comprehension?", ["Inline list creation", "List sorting", "List copying", "List deletion"], "A", "medium", "Advanced Python", 2),
            q("What is __main__ used for?", ["Script execution check", "Main function", "Class definition", "Import check"], "A", "medium", "Advanced Python", 2),
        ]

        with transaction.atomic():
            DiagnosticQuestion.objects.bulk_create(questions)
            # Create DiagnosticOption records and persist JSONField for compatibility
            from assessments.models import DiagnosticOption
            for qobj, spec in zip(DiagnosticQuestion.objects.filter(quiz=quiz).order_by("id"), questions):
                opts = spec.options
                qobj.options = opts
                qobj.save(update_fields=["options"])
                correct_idx = spec.correct_index if hasattr(spec, "correct_index") else 0
                for i, text in enumerate(opts):
                    obj, _ = DiagnosticOption.objects.get_or_create(question=qobj, text=text)
                    obj.is_correct = (i == correct_idx)
                    obj.save(update_fields=["is_correct"])

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(questions)} diagnostic questions covering all 10 modules"))

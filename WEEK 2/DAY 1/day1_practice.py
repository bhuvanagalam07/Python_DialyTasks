

name = "Bhuvana"
age = 22
salary = 25000.50
is_employee = True
result = None

print("Name:", name)
print("Age:", age)
print("Salary:", salary)
print("Employee:", is_employee)
print("Result:", result)

print(type(name))
print(type(age))
print(type(salary))
print(type(is_employee))
print(type(result))






# List
skills = ["Python", "SQL", "HTML"]
skills.append("Java")
skills[0] = "Python Basics"
print("List:", skills)

# Tuple
coordinates = (10, 20)
print("Tuple:", coordinates)
print("First coordinate:", coordinates[0])

# Set
numbers = {1, 2, 2, 3, 4, 4}
print("Set:", numbers)

# Dictionary
employee = {
    "name": "Bhuvana",
    "department": "IT",
    "salary": 25000
}
employee["salary"] = 30000
print("Employee:", employee)
print("Name:", employee["name"])
print("Updated salary:", employee["salary"])




marks = 75

if marks >= 90:
    print("Grade A")
elif marks >= 70:
    print("Grade B")
elif marks >= 40:
    print("Pass")
else:
    print("Fail")




# For loop
for number in range(1, 6):
    print(number)

# While loop
count = 1

while count <= 3:
    print("Count:", count)
    count += 1




# Create squares
squares = [n * n for n in range(1, 6)]
print("Squares:", squares)

# Keep only even numbers
even_numbers = [
    n for n in range(1, 11)
    if n % 2 == 0
]
print("Even numbers:", even_numbers)

# Convert names to uppercase
names = ["ravi", "priya", "anil"]
upper_names = [name.upper() for name in names]
print("Uppercase:", upper_names)




numbers = [1, 2, 3, 4, 5]

square_dict = {
    n: n * n for n in numbers
}
print(square_dict)

# Employee marks: retain passing students
marks = {
    "Ravi": 75,
    "Priya": 35,
    "Anil": 80,
    "Divya": 45
}

passed = {
    name: score
    for name, score in marks.items()
    if score >= 40
}
print(passed)




def add(a, b):
    return a + b


def is_even(number):
    return number % 2 == 0


def calculate_average(numbers):
    if not numbers:
        return 0

    return sum(numbers) / len(numbers)


result = add(10, 20)
print("Sum:", result)

print("Is 8 even?", is_even(8))

average = calculate_average([10, 20, 30])
print("Average:", average)




# Positional arguments
def introduce(name, age):
    print(name, age)

introduce("Bhuvana", 22)

# Default argument
def greet(name, message="Welcome"):
    print(message, name)

greet("Bhuvana")
greet("Bhuvana", "Hello")

# Keyword arguments
introduce(age=22, name="Bhuvana")




company = "ABC Technologies"  # Global variable


def display_employee():
    name = "Bhuvana"  # Local variable

    print("Employee:", name)
    print("Company:", company)


display_employee()
print("Outside function:", company)





def outer():
    message = "Hello from outer function"

    def inner():
        print(message)

    inner()


outer()





count = 0


def increase_count():
    global count
    count += 1


increase_count()
increase_count()

print("Count:", count)

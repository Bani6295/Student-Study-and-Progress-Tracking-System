
import json
import os
from datetime import datetime, date
from colorama import Fore, Style, init

init(autoreset=True)

FILE_NAME = "study_tasks.json"
tasks = []

# Colour theme
PURPLE = Fore.MAGENTA
BLUE = Fore.CYAN
PINK = Fore.LIGHTMAGENTA_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.YELLOW
RED = Fore.LIGHTRED_EX
WHITE = Fore.WHITE
RESET = Style.RESET_ALL

# Decorative heading
def heading():
    print("\n" + PURPLE + "=" * 55)
    print(PINK + Style.BRIGHT +
          "             STUDY PLANNER")
    print(BLUE + "       STUDENT STUDY & PROGRESS TRACKING")
    print(PURPLE + "=" * 55)

# Load saved tasks
def load_tasks():
    global tasks

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                tasks = json.load(file)

            # Support tasks from older versions
            for task in tasks:
                task.setdefault("priority", "Medium")
                task.setdefault("deadline", "")
                task.setdefault("completed", False)

        except (json.JSONDecodeError, OSError):
            tasks = []
            print(RED + "Could not load saved tasks!")

# Save tasks
def save_tasks():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        print(RED + "Error saving tasks!")

# Find next available ID
def next_id():
    return max([task["id"] for task in tasks], default=0) + 1

# Get deadline
def get_deadline():
    while True:
        deadline = input(
            "Enter deadline (YYYY-MM-DD) or press Enter to skip: "
        ).strip()

        if deadline == "":
            return ""

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
            return deadline
        except ValueError:
            print(RED + "Invalid date! Use YYYY-MM-DD.")

# Get priority
def get_priority():
    print("\n" + YELLOW + "SELECT PRIORITY")
    print(GREEN + "1. Low")
    print(YELLOW + "2. Medium")
    print(RED + "3. High")

    options = {
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    while True:
        choice = input("Choose priority: ")

        if choice in options:
            return options[choice]

        print(RED + "Please choose 1, 2 or 3.")

# Display dashboard
def dashboard():
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed

    progress = completed / total * 100 if total else 0

    today = date.today()
    overdue = 0
    upcoming = 0

    for task in tasks:
        if not task["completed"] and task["deadline"]:
            due = datetime.strptime(
                task["deadline"], "%Y-%m-%d"
            ).date()

            if due < today:
                overdue += 1
            elif due == today:
                upcoming += 1

    print("\n" + BLUE + "                 DASHBOARD")
    print(PURPLE + "-" * 55)

    print(WHITE + "  Total Tasks       : " + str(total))
    print(GREEN + "  Completed         : " + str(completed))
    print(YELLOW + "  Pending           : " + str(pending))
    print(RED + "  Overdue           : " + str(overdue))
    print(YELLOW + "  Due Today         : " + str(upcoming))

    print("\n" + PINK + "  OVERALL PROGRESS")
    print(GREEN + "  {:.1f}%".format(progress))

    filled = int(progress / 5)
    bar = "#" * filled + "-" * (20 - filled)

    print(GREEN + "  [" + bar + "]")
    print(PURPLE + "-" * 55)

# Add a task
def add_task():
    print(PINK + "\n--- ADD NEW STUDY TASK ---")

    title = input("Enter task name: ").strip()

    if not title:
        print(RED + "Task name cannot be empty!")
        return

    subject = input("Enter subject: ").strip()

    if not subject:
        print(RED + "Subject cannot be empty!")
        return

    priority = get_priority()
    deadline = get_deadline()

    task = {
        "id": next_id(),
        "title": title,
        "subject": subject,
        "priority": priority,
        "deadline": deadline,
        "completed": False
    }

    tasks.append(task)
    save_tasks()

    print(GREEN + "\nTask added successfully!")

# Display tasks
def view_tasks(task_list=None):
    if task_list is None:
        task_list = tasks

    print(PINK + "\n--- YOUR STUDY TASKS ---")

    if not task_list:
        print(YELLOW + "No tasks found!")
        return

    for task in task_list:
        status = (
            GREEN + "COMPLETED"
            if task["completed"]
            else YELLOW + "PENDING"
        )

        colors = {
            "High": RED,
            "Medium": YELLOW,
            "Low": GREEN
        }

        priority = colors.get(
            task["priority"], WHITE
        ) + task["priority"].upper()

        print(BLUE + "\n" + "-" * 45)
        print(WHITE + "  Task ID  : " + str(task["id"]))
        print(WHITE + "  Title    : " + task["title"])
        print(WHITE + "  Subject  : " + task["subject"])
        print("  Priority : " + priority)
        print("  Deadline : " +
              (task["deadline"] or "Not specified"))
        print("  Status   : " + status)

    print(BLUE + "-" * 45)

# Find task by ID
def find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

# Mark task completed
def complete_task():
    view_tasks()

    if not tasks:
        return

    try:
        task_id = int(input("\nEnter task ID: "))
    except ValueError:
        print(RED + "Enter a valid number!")
        return

    task = find_task(task_id)

    if task is None:
        print(RED + "Task not found!")
    elif task["completed"]:
        print(YELLOW + "Task is already completed!")
    else:
        task["completed"] = True
        save_tasks()
        print(GREEN + "Congratulations! Task completed!")

# Edit a task
def edit_task():
    view_tasks()

    if not tasks:
        return

    try:
        task_id = int(input("\nEnter task ID to edit: "))
    except ValueError:
        print(RED + "Enter a valid number!")
        return

    task = find_task(task_id)

    if task is None:
        print(RED + "Task not found!")
        return

    print(YELLOW + "\nPress Enter to keep the existing value.")

    title = input("New task name: ").strip()
    if title:
        task["title"] = title

    subject = input("New subject: ").strip()
    if subject:
        task["subject"] = subject

    print("\nCurrent priority:", task["priority"])
    change = input("Change priority? (y/n): ").lower()

    if change == "y":
        task["priority"] = get_priority()

    print("\nCurrent deadline:",
          task["deadline"] or "Not specified")

    change = input("Change deadline? (y/n): ").lower()

    if change == "y":
        task["deadline"] = get_deadline()

    save_tasks()
    print(GREEN + "\nTask updated successfully!")

# Search tasks
def search_tasks():
    keyword = input(
        "\nEnter task name or subject to search: "
    ).strip().lower()

    if not keyword:
        print(RED + "Search cannot be empty!")
        return

    results = [
        task for task in tasks
        if keyword in task["title"].lower()
        or keyword in task["subject"].lower()
    ]

    view_tasks(results)

# Filter tasks
def filter_tasks():
    print(PINK + "\n--- FILTER TASKS ---")
    print("1. Pending Tasks")
    print("2. Completed Tasks")
    print("3. High Priority Tasks")

    choice = input("Enter choice: ")

    if choice == "1":
        results = [
            t for t in tasks if not t["completed"]
        ]
    elif choice == "2":
        results = [
            t for t in tasks if t["completed"]
        ]
    elif choice == "3":
        results = [
            t for t in tasks if t["priority"] == "High"
        ]
    else:
        print(RED + "Invalid choice!")
        return

    view_tasks(results)

# Delete task
def delete_task():
    view_tasks()

    if not tasks:
        return

    try:
        task_id = int(input("\nEnter task ID to delete: "))
    except ValueError:
        print(RED + "Enter a valid number!")
        return

    task = find_task(task_id)

    if task is None:
        print(RED + "Task not found!")
        return

    confirm = input(
        "Are you sure you want to delete this task? (y/n): "
    ).lower()

    if confirm == "y":
        tasks.remove(task)
        save_tasks()
        print(GREEN + "Task deleted successfully!")
    else:
        print(YELLOW + "Deletion cancelled.")

# Progress report
def show_progress():
    dashboard()

    if not tasks:
        return

    print(PINK + "\n--- SUBJECT-WISE PROGRESS ---")

    subjects = {}

    for task in tasks:
        subject = task["subject"]

        if subject not in subjects:
            subjects[subject] = [0, 0]

        subjects[subject][0] += 1

        if task["completed"]:
            subjects[subject][1] += 1

    for subject, count in subjects.items():
        percentage = count[1] / count[0] * 100

        print(WHITE + "\n" + subject)
        print(GREEN + "Completed: " +
              str(count[1]) + "/" + str(count[0]))
        print(YELLOW + "Progress: {:.1f}%".format(percentage))

# Main menu
def main():
    load_tasks()

    while True:
        heading()
        dashboard()

        print(PINK + "\n               MAIN MENU")
        print(BLUE + "-" * 55)

        print(WHITE + "  [1]  Add New Study Task")
        print(WHITE + "  [2]  View All Tasks")
        print(WHITE + "  [3]  Mark Task Completed")
        print(WHITE + "  [4]  Edit Existing Task")
        print(WHITE + "  [5]  Search Tasks")
        print(WHITE + "  [6]  Filter Tasks")
        print(WHITE + "  [7]  View Progress Report")
        print(WHITE + "  [8]  Delete Task")
        print(WHITE + "  [9]  Exit")

        print(BLUE + "-" * 55)

        choice = input(YELLOW + "\n  Enter your choice: ")

        if choice == "1":
            add_task()

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            complete_task()

        elif choice == "4":
            edit_task()

        elif choice == "5":
            search_tasks()

        elif choice == "6":
            filter_tasks()

        elif choice == "7":
            show_progress()

        elif choice == "8":
            delete_task()

        elif choice == "9":
            print(GREEN + "\nThank you for using Study Planner!")
            print(PINK + "Keep learning. Keep growing!")
            break

        else:
            print(RED + "\nInvalid choice! Try again.")

        input(YELLOW + "\nPress Enter to return to menu...")

# Start application
if __name__ == "__main__":
    main()

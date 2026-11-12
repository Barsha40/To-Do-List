
import json
import os
import sys


FILE_NAME = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file."""

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read tasks.json. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""

    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

    except OSError as error:
        print("Error saving tasks:", error)


def add_task(tasks, task_name):
    """Add a new task."""

    if not task_name.strip():
        print("Task cannot be empty.")
        return

    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "task": task_name,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully: {task_name}")


def list_tasks(tasks):
    """Display all tasks."""

    if not tasks:
        print("Your to-do list is empty.")
        return

    print("\n========== YOUR TASKS ==========")

    for task in tasks:
        status = "Done" if task["completed"] else "Pending"

        print(
            f"{task['id']}. [{status}] {task['task']}"
        )

    print("================================")


def complete_task(tasks, task_id):
    """Mark a task as completed."""

    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print("Task is already completed.")
            else:
                task["completed"] = True
                save_tasks(tasks)
                print("Task marked as completed!")
            return

    print("Task ID not found.")


def main():

    tasks = load_tasks()

    if len(sys.argv) < 2:
        print("""
========== TO-DO LIST CLI ==========

Commands:
  python todo.py add "Buy milk"
  python todo.py list
  python todo.py done 1

====================================
""")
        return

    command = sys.argv[1].lower()

    if command == "add":

        if len(sys.argv) < 3:
            print("Please provide a task name.")
            return

        task_name = " ".join(sys.argv[2:])
        add_task(tasks, task_name)

    elif command == "list":

        list_tasks(tasks)

    elif command == "done":

        if len(sys.argv) < 3:
            print("Please provide a task ID.")
            return

        try:
            task_id = int(sys.argv[2])
            complete_task(tasks, task_id)

        except ValueError:
            print("Task ID must be a number.")

    else:
        print("Invalid command. Use add, list, or done.")


if __name__ == "__main__":
    main()

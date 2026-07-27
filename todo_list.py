"""
To-Do List Application
-----------------------
A command-line To-Do List manager built with Python.
Supports: adding, viewing, updating (marking complete), and deleting tasks.
Tasks are saved to a local JSON file so your list persists between runs.
"""

import json
import os

DATA_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks)
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def view_tasks(tasks):
    if not tasks:
        print("\nYour to-do list is empty!\n")
        return
    print("\nYour To-Do List:")
    print("-" * 30)
    for i, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else " "
        print(f"[{status}] {i}. {task['title']}")
    print("-" * 30 + "\n")


def add_task(tasks):
    title = input("Enter the new task: ").strip()
    if title:
        tasks.append({"title": title, "done": False})
        save_tasks(tasks)
        print(f"Added: \"{title}\"\n")
    else:
        print("Task cannot be empty.\n")


def mark_done(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter the task number to mark as done: "))
        tasks[num - 1]["done"] = True
        save_tasks(tasks)
        print(f"Marked \"{tasks[num - 1]['title']}\" as done.\n")
    except (ValueError, IndexError):
        print("Invalid task number.\n")


def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter the task number to delete: "))
        removed = tasks.pop(num - 1)
        save_tasks(tasks)
        print(f"Deleted: \"{removed['title']}\"\n")
    except (ValueError, IndexError):
        print("Invalid task number.\n")


def main():
    tasks = load_tasks()
    menu = """
========== TO-DO LIST ==========
1. View tasks
2. Add a task
3. Mark a task as done
4. Delete a task
5. Exit
=================================
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1-5.\n")


if __name__ == "__main__":
    main()
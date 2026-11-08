
tasks = []
completed = []

while True:
    print("\n--- STUDENT STUDY PLANNER ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("4. View Progress")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter study task: ")
        tasks.append(task)
        completed.append(False)
        print("Task added successfully!")

    elif choice == "2":
        for i in range(len(tasks)):
            status = "Completed" if completed[i] else "Pending"
            print(i + 1, tasks[i], "-", status)

    elif choice == "3":
        for i in range(len(tasks)):
            print(i + 1, tasks[i])
        number = int(input("Enter task number: "))
        if 1 <= number <= len(tasks):
            completed[number - 1] = True
            print("Task marked as completed!")
        else:
            print("Invalid task number.")

    elif choice == "4":
        total = len(tasks)
        done = completed.count(True)
        print("Total Tasks:", total)
        print("Completed Tasks:", done)
        print("Pending Tasks:", total - done)
        if total > 0:
            print("Progress:", done / total * 100, "%")
        else:
            print("Progress: 0%")

    elif choice == "5":
        print("Thank you for using Student Study Planner!")
        break

    else:
        print("Invalid choice. Try again.")

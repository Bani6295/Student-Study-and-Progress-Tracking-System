
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Student Study Planner</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f0ff;
            margin: 0;
            padding: 25px;
            color: #30264a;
        }
        .container {
            max-width: 700px;
            margin: 30px auto;
            background: white;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 5px 20px #ddd;
        }
        h1 { color: #7047b8; text-align: center; }
        .subtitle { text-align: center; color: #777; }
        input, select, button {
            padding: 12px;
            margin: 6px 0;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 15px;
        }
        input, select { box-sizing: border-box; }
        #taskInput { width: 100%; }
        .form-row { display: flex; gap: 8px; }
        .form-row input, .form-row select { min-width: 0; flex: 1; }
        button {
            background: #7952bd;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover { background: #603b9d; }
        .stats {
            display: flex;
            justify-content: space-around;
            background: #f1ebff;
            padding: 15px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
        }
        .stats strong { display: block; font-size: 23px; color: #7047b8; }
        .task {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            background: #faf9ff;
            padding: 12px;
            margin: 10px 0;
            border-radius: 10px;
        }
        .task-name { flex: 1; overflow-wrap: anywhere; }
        .completed { text-decoration: line-through; color: #999; }
        .delete { background: #e46b79; }
        .progress-bg {
            background: #e7e0f5;
            height: 12px;
            border-radius: 10px;
            overflow: hidden;
        }
        #progressBar {
            background: #7952bd;
            height: 100%;
            width: 0%;
        }
        #empty { text-align: center; color: #999; padding: 20px; }
        @media(max-width: 500px) {
            body { padding: 10px; }
            .container { padding: 18px; }
            .form-row { flex-wrap: wrap; }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>My Study Planner 📚</h1>
    <p class="subtitle">Plan your day. Complete your goals. Track your progress.</p>

    <h3>Add a New Study Task</h3>
    <input id="taskInput" placeholder="Enter your study task">

    <div class="form-row">
        <input type="date" id="taskDate">
        <select id="priority">
            <option value="Normal">Normal</option>
            <option value="High">High Priority</option>
            <option value="Low">Low Priority</option>
        </select>
    </div>
    <button onclick="addTask()">+ Add Task</button>

    <div class="stats">
        <div><strong id="total">0</strong>Total</div>
        <div><strong id="done">0</strong>Completed</div>
        <div><strong id="remaining">0</strong>Remaining</div>
    </div>

    <h3>Overall Progress</h3>
    <div class="progress-bg">
        <div id="progressBar"></div>
    </div>
    <p id="progressText">0% completed</p>

    <h3>My Tasks</h3>
    <div id="taskList"></div>
    <p id="empty">No tasks yet. Add your first task!</p>
</div>
<div class="container">
    <h2>⏱️ Study Timer</h2>
    <h1 id="timer">25:00</h1>
    <button onclick="startTimer()">Start</button>
    <button onclick="pauseTimer()">Pause</button>
    <button onclick="resetTimer()">Reset</button>
    <p id="timerMessage">Ready to study?</p>
</div>
<script>
let tasks = JSON.parse(localStorage.getItem("studyTasks") || "[]");

let timeLeft = 25 * 60;
let timerInterval = null;

function updateTimer() {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;

    document.getElementById("timer").textContent =
        String(minutes).padStart(2, "0") + ":" +
        String(seconds).padStart(2, "0");
}

function startTimer() {
    if (timerInterval !== null || timeLeft === 0) return;

    document.getElementById("timerMessage").textContent = "Focus on your studies!";

    timerInterval = setInterval(function() {
        if (timeLeft > 0) {
            timeLeft--;
            updateTimer();
        } else {
            clearInterval(timerInterval);
            timerInterval = null;
            document.getElementById("timerMessage").textContent =
                "Session completed! Great work!";
            alert("Your 25-minute study session is complete!");
        }
    }, 1000);
}

function pauseTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    document.getElementById("timerMessage").textContent = "Timer paused.";
}

function resetTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    timeLeft = 25 * 60;
    updateTimer();
    document.getElementById("timerMessage").textContent = "Ready to study?";
}

updateTimer();
function saveTasks() {
    localStorage.setItem("studyTasks", JSON.stringify(tasks));
}

function addTask() {
    const name = document.getElementById("taskInput").value.trim();
    const date = document.getElementById("taskDate").value;
    const priority = document.getElementById("priority").value;

    if (!name) {
        alert("Please enter a task!");
        return;
    }

    tasks.push({
        name: name,
        date: date,
        priority: priority,
        completed: false
    });

    document.getElementById("taskInput").value = "";
    saveTasks();
    showTasks();
}

function toggleTask(index) {
    tasks[index].completed = !tasks[index].completed;
    saveTasks();
    showTasks();
}

function deleteTask(index) {
    if (confirm("Are you sure you want to delete this task?")) {
        tasks.splice(index, 1);
        saveTasks();
        showTasks();
    }
}

function showTasks() {
    const list = document.getElementById("taskList");
    list.innerHTML = "";

    document.getElementById("empty").style.display =
        tasks.length === 0 ? "block" : "none";

    tasks.forEach((task, index) => {
        const item = document.createElement("div");
        item.className = "task";

        const name = document.createElement("span");
        name.className = "task-name" +
            (task.completed ? " completed" : "");
        name.textContent = task.name + " | " + task.priority +
            (task.date ? " | " + task.date : "");

        const check = document.createElement("input");
        check.type = "checkbox";
        check.checked = task.completed;
        check.onchange = () => toggleTask(index);

        const remove = document.createElement("button");
        remove.textContent = "Delete";
        remove.className = "delete";
        remove.onclick = () => deleteTask(index);

        item.append(check, name, remove);
        list.appendChild(item);
    });

    const total = tasks.length;
    const done = tasks.filter(task => task.completed).length;
    const remaining = total - done;
    const percent = total === 0 ? 0 : Math.round(done / total * 100);

    document.getElementById("total").textContent = total;
    document.getElementById("done").textContent = done;
    document.getElementById("remaining").textContent = remaining;
    document.getElementById("progressBar").style.width = percent + "%";
    document.getElementById("progressText").textContent =
        percent + "% completed";
}

showTasks();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)

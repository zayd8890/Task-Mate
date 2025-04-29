# AI Task Management Agent

The **AI Task Management Agent** is a Python-based application designed to help users manage and prioritize their tasks efficiently. It uses AI/ML logic to auto-assign task priorities, handle task dependencies, and create schedules. The agent can also visualize task dependencies and handle recurring tasks.

---

## Features

1. **Task Prioritization**:
   - Auto-assigns weights to tasks based on deadlines, task type, and urgency.
   - Supports user-defined weights for custom prioritization.

2. **Task Dependencies**:
   - Handles task dependencies using topological sorting.
   - Detects and raises errors for circular dependencies.

3. **Scheduling**:
   - Creates schedules for tasks based on their priorities and deadlines.
   - Supports recurring tasks (e.g., daily standups, weekly reviews).

4. **Visualization**:
   - Visualizes task dependencies using `networkx` and `matplotlib`.

5. **Extensibility**:
   - Modular design makes it easy to add new features (e.g., calendar integration, notifications).

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required Python libraries (see `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/task-management-agent.git
   cd task-management-agent

## Usage

### Task Prioritization
```python
from ai_ml_logic.task_prioritization import auto_assign_weight

task = {"description": "Prepare for exam", "deadline": "2023-11-10", "type": "work"}
weight = auto_assign_weight(task["description"], task.get("deadline"), task.get("type"))
print(f"Priority: {weight:.2f}")
```
### Task Dependencies
```python
from ai_ml_logic.task_prioritization import resolve_dependencies

tasks = [
    {"id": 1, "description": "Task 1", "dependencies": []},
    {"id": 2, "description": "Task 2", "dependencies": [1]},
]
ordered_tasks = resolve_dependencies(tasks)
```
### Scheduling
```python
from ai_ml_logic.scheduling import create_schedule

tasks = [
    {"description": "Task 1", "deadline": "2023-11-01", "type": "work"},
    {"description": "Task 2", "deadline": "2023-11-02", "type": "work"},
]
schedule = create_schedule(tasks, "2023-10-25")
```
### Visualization
```python
from ai_ml_logic.visualization import visualize_dependencies

tasks = [
    {"id": 1, "description": "Task 1", "dependencies": []},
    {"id": 2, "description": "Task 2", "dependencies": [1]},
]
visualize_dependencies(tasks)
```
### File structure
```bash
Task Mate/
│
├── ai_agent/
│
│   ├── task_management/
│
│   │   ├── ai_ml_logic/
│
│   │   │   ├── __pycache__/
│
│   │   │   │   ├── __init__.cpython-311.pyc
│
│   │   │   │   ├── __init__.cpython-312.pyc
│
│   │   │   │   ├── scheduling.cpython-311.pyc
│
│   │   │   │   ├── task_decomposition.cpython-311.pyc
│
│   │   │   │   ├── task_prioritization.cpython-311.pyc
│
│   │   │   │   ├── task_prioritization.cpython-312.pyc
│
│   │   │   │   └── visualization.cpython-311.pyc
│
│   │   │   ├── __init__.py
│
│   │   │   ├── scheduling.py
│
│   │   │   ├── task_decomposition.py
│
│   │   │   ├── task_prioritization.py
│
│   │   │   └── visualization.py
│
│   │   ├── config/
│
│   │   │   ├── api_keys.yaml
│
│   │   │   └── settings.yaml
│
│   │   ├── htmlcov/
│
│   │   │   ├── class_index.html
│
│   │   │   ├── coverage_html_cb_497bf287.js
│
│   │   │   ├── favicon_32_cb_58284776.png
│
│   │   │   ├── function_index.html
│
│   │   │   ├── index.html
│
│   │   │   ├── keybd_closed_cb_ce680311.png
│
│   │   │   ├── status.json
│
│   │   │   ├── style_cb_718ce007.css
│
│   │   │   ├── z_c4962fce667ec12e___init___py.html
│
│   │   │   ├── z_c4962fce667ec12e_scheduling_py.html
│
│   │   │   ├── z_c4962fce667ec12e_task_decomposition_py.html
│
│   │   │   ├── z_c4962fce667ec12e_task_prioritization_py.html
│
│   │   │   └── z_c4962fce667ec12e_visualization_py.html
│
│   │   ├── scripts/
│
│   │   │   └── scripts.py
│
│   │   ├── utils/
│
│   │   │   └── __init__.py
│
│   │   └── main.py
│
│   ├── tests/
│
│   │   ├── __init__.py
│
│   │   ├── conftest.py
│
│   │   ├── pytest.ini
│
│   │   ├── test_agent.py
│
│   │   ├── test_integration.py
│
│   │   ├── test_task_manager.py
│
│   │   └── test_tools.py
│
│   ├── tools/
│
│   │   ├── calculator.py
│
│   │   ├── file_operations.py
│
│   │   ├── task_manager.py
│
│   │   ├── text_processor.py
│
│   │   └── web_search.py
│
│   ├── agent.py
│
│   ├── config.toml
│
│   ├── deepseek.py
│
│   └── main.py
│
├── backend/
│
├── frontend/
│
│   ├── icons/
│
│   │   ├── icon128.png
│
│   │   └── icon48.png
│
│   ├── background.js
│
│   ├── config.cfg
│
│   ├── manifest.json
│
│   ├── popup.css
│
│   ├── popup.html
│
│   └── popup.js
│
├── LICENSE
│
├── directory_tree.py
│
├── readme.md
│
└── requirements.txt
```
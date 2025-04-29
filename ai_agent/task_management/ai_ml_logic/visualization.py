# ai_ml_logic/visualization.py
import networkx as nx
import matplotlib.pyplot as plt

def visualize_dependencies(tasks):
    """
    Visualizes task dependencies using a directed graph.

    Args:
        tasks (list): List of tasks, where each task is a dict with "id", "description",
                      and "dependencies".

    Example:
        >>> tasks = [
        ...     {"id": 1, "description": "Task 1", "dependencies": []},
        ...     {"id": 2, "description": "Task 2", "dependencies": [1]},
        ... ]
        >>> visualize_dependencies(tasks)
        # Displays a graph with nodes (tasks) and edges (dependencies).
    """
    # Create a directed graph
    graph = nx.DiGraph()
    
    # Add nodes and edges
    for task in tasks:
        graph.add_node(task["id"], label=task["description"])
        for dependency in task["dependencies"]:
            graph.add_edge(dependency, task["id"])
    
    # Draw the graph
    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, "label")
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", arrows=True)
    plt.show()
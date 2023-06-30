import tkinter as tk
import math
from collections import defaultdict

modifiedGraph =[]
MAX_INT = float('Inf')
shortest_paths = []


def BellmanFord(edges, graph, num_vertices):

	dist = [MAX_INT] * (num_vertices + 1)
	dist[num_vertices] = 0

	for i in range(num_vertices):
		edges.append([num_vertices, i, 0])

	for i in range(num_vertices):
		for (src, des, weight) in edges:
			if((dist[src] != MAX_INT) and
					(dist[src] + weight < dist[des])):
				dist[des] = dist[src] + weight
	return dist[0:num_vertices]


# Return the vertex with its minimum distance from the source
def minDistance(dist, visited):

	(minimum, minVertex) = (MAX_INT, 0)
	for vertex in range(len(dist)):
		if minimum > dist[vertex] and visited[vertex] == False:
			(minimum, minVertex) = (dist[vertex], vertex)

	return minVertex

def Dijkstra(graph, modifiedGraph, src):

    num_vertices = len(graph)
    sptSet = defaultdict(lambda: False)

   
    dist = [MAX_INT] * num_vertices
    dist[src] = 0

    for count in range(num_vertices):
        curVertex = minDistance(dist, sptSet)
        sptSet[curVertex] = True

        for vertex in range(num_vertices):
            if (
                (sptSet[vertex] == False)
                and (
                    dist[vertex]
                    > (dist[curVertex] + modifiedGraph[curVertex][vertex])
                )
                and (graph[curVertex][vertex] != 0)
            ):
                dist[vertex] = dist[curVertex] + modifiedGraph[curVertex][vertex]

    return dist


def JohnsonAlgorithm(graph):
    global modifiedGraph
    global shortest_path
    edges = []

    # Create a list of edges 
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] != 0:
                edges.append([i, j, graph[i][j]])

    
    modifyWeights = BellmanFord(edges, graph, len(graph))
    modifiedGraph = [[0 for x in range(len(graph))] for y in range(len(graph))]

    #get rid of negative weights
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] != 0:
                modifiedGraph[i][j] = (
                    graph[i][j] + modifyWeights[i] - modifyWeights[j]
                )

    
    for src in range(len(graph)):
        shortest_path = Dijkstra(graph, modifiedGraph, src)
        shortest_paths.append(shortest_path)
    return shortest_paths




#Graphic part of the code 

def draw_graph(event,graph):
    
    canvas.delete("all")  

    num_nodes = len(graph)

    # Calculate the positions of the nodes
    node_positions = {}
    radius = min(canvas.winfo_width(), canvas.winfo_height()) / 3
    node_radius = 30  
    for i in range(num_nodes):
        angle = 2 * i * math.pi / num_nodes
        x = canvas.winfo_width() / 2 + radius * math.sin(angle)
        y = canvas.winfo_height() / 2 + radius * math.cos(angle)
        node_positions[i] = (x, y)

    # Draw the nodes
    for node, pos in node_positions.items():
        x, y = pos
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill='blue')
        canvas.create_text(x, y, text=str(node), fill='white', font=('Arial', 16), justify='center')

    # Draw the edges 
    for i in range(num_nodes):
        for j in range(num_nodes):
            weight = graph[i][j]
            if weight != float('inf') :
                x1, y1 = node_positions[i]
                x2, y2 = node_positions[j]
                canvas.create_line(x1, y1, x2, y2, width=2, arrow=tk.LAST,
                                   arrowshape=(15, 60, 15))  
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(weight))


    text = "1-add a new vertexand connecting it to \nall existing vertices with zero-weight edges.\n This ensures that there are\n no negative cycles in the graph.\n\n 2-Apply the Bellman-Ford\n algorithm on the modified graph\n\n \n3-Apply Dijkstra's algorithm \non the  modified graph\nfor each vertex as the source\n to find the shortest paths to all \nother vertices."
    text_x = canvas.winfo_width()-1100 
    text_y = 50 
    canvas.create_text(text_x, text_y, text=text, fill='black', font=('Arial', 16), anchor=tk.NE)



def add_new_node(event):
    add_new_node_button.destroy()
 
    #position of the new node
    x = event.x+1500
    y = event.y + 70  

    # Draw the new node
    node_radius = 20
    canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill='red')

    # Calculate the positions of the existing nodes
    num_nodes = len(adjacency_matrix)
    node_positions = calculate_node_positions(num_nodes)

    # Draw the curved lines to connect the new node to the existing nodes
    for i, pos in node_positions.items():
        x1, y1 = pos
        draw_curved_line(x, y, x1, y1)

    create_new_button()


def create_new_button():
    global bellman_ford_button
    bellman_ford_button = tk.Button(window, text="apply bellmanford", bg="blue", fg="white", width=20, height=3)
    bellman_ford_button.bind("<Button-1>", draw_new_graph)
    bellman_ford_button.place(x=100, y=800)



def draw_new_graph(event):
    global modifiedGraph
    bellman_ford_button.destroy()
    draw_graph(event, modifiedGraph)
    show_shourtest_path()


def show_shourtest_path():
    global text


   
    array_text = "shourtest path:\n"
    for i, path in enumerate(shortest_paths):
        
        for j, distance in enumerate(path):
            array_text += f"{i}-> {j}: {distance}\n"
        array_text += "\n"

    text = array_text
    font_size = 8
    text_x = canvas.winfo_width()-100 
    text_y = 50 
    canvas.create_text(text_x, text_y, text=text, fill='black', font=('Arial', 16), anchor=tk.NE)




#calculate the position of new node
def calculate_node_positions(num_nodes):
    node_positions = {}
    radius = min(canvas.winfo_width(), canvas.winfo_height()) / 3
    node_radius = 20

    for i in range(num_nodes):
        angle = 2 * i * math.pi / num_nodes
        x = canvas.winfo_width() / 2 + radius * math.sin(angle)
        y = canvas.winfo_height() / 2 + radius * math.cos(angle)
        node_positions[i] = (x, y)

    return node_positions


#connect new node to the existing one with edges with 0 weight 
def draw_curved_line(x1, y1, x2, y2):

    # Calculate the control points for the Bezier curve
    control_x = (x1 + x2) / 2
    control_y = (y1 + y2) / 2 - abs(x1 - x2) / 4

    # Draw the curved line using a Bezier curve
    line = canvas.create_line(x1, y1, control_x, control_y, x2, y2, smooth=True, width=2, arrow=tk.LAST, arrowshape=(12, 15, 8))
    line_coords = canvas.coords(line)
    text_x = (line_coords[0] + line_coords[2]) / 2
    text_y = (line_coords[1] + line_coords[3]) / 2
    canvas.create_text(text_x, text_y, text='0', fill='black', font=('Arial', 10))







adjacency_matrix =  [[0, -5, 2, 3],
                    [float('inf'), 0, 4, float('inf')],
                    [float('inf'), float('inf'), 0, 1],
                    [float('inf'), float('inf'), float('inf'), 0]]



JohnsonAlgorithm(adjacency_matrix)


# Create the main window
window = tk.Tk()
window.geometry("2000x1100")  
window.title("JohnsonAlgorithm")
window.resizable(False, False)


# Create the canvas
canvas = tk.Canvas(window, width=1000, height=800)
canvas.pack(fill=tk.BOTH, expand=True)


# Bind the draw_graph function to the Configure event of the canvas
canvas.bind("<Configure>", lambda event: draw_graph(event, adjacency_matrix))


#Addbutton to add a new node  to the graph, add edges from new vertex to all vertices of graph
add_new_node_button = tk.Button(window, text=" add new vertex", bg="blue", fg="white", width=20, height=3)
add_new_node_button.bind("<Button-1>", add_new_node)
add_new_node_button.place(x=window.winfo_width() +100- add_new_node_button.winfo_width(), y=800)
bellman_ford_button = tk.Button(window, text="apply bellmanford", bg="blue", fg="white", width=20, height=3)


window.mainloop()
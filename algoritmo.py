import heapq
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def dijkstra(graph, start, end):
    # Inicializar las distancias y la cola de prioridad
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruir el camino más corto
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()

    return distances[end], path

def graficar_grafo(graph, path):
    print("Generando el grafo...")
    G = nx.DiGraph()  # Cambiar a DiGraph para grafo dirigido

    # Agregar nodos y aristas al grafo
    for node, edges in graph.items():
        for neighbor, weight in edges:
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)  # Posiciones de los nodos

    # Dibujar nodos y aristas sin flechas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, arrows=False)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Resaltar el camino más corto con flechas
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, arrows=True)

    plt.title("Grafo y camino más corto")

    # Guardar el gráfico como imagen
    static_dir = "static"  # Carpeta donde se guardarán las imágenes
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)  # Crear la carpeta si no existe
    file_name = f"{static_dir}/grafo_camino_mas_corto.png"

    plt.savefig(file_name)  # Sobrescribe la imagen existente
    print(f"El gráfico ha sido guardado como '{file_name}'.")

    plt.close()  # Cierra la figura para liberar memoria

def main():
    print("Introduce las aristas del grafo (formato: nodo1 nodo2 peso, una por línea). Escribe 'fin' para terminar:")
    graph = {}

    while True:
        line = input()
        if line.lower() == 'fin':
            break
        try:
            node1, node2, weight = line.split()
            weight = int(weight)
            if node1 not in graph:
                graph[node1] = []
            if node2 not in graph:
                graph[node2] = []
            graph[node1].append((node2, weight))
            graph[node2].append((node1, weight))  # Si el grafo es dirigido, elimina esta línea.
        except ValueError:
            print("Entrada inválida. Asegúrate de usar el formato: nodo1 nodo2 peso")

    start = input("Introduce el nodo inicial: ")
    end = input("Introduce el nodo final: ")

    try:
        distance, path = dijkstra(graph, start, end)
        print(f"La distancia más corta de {start} a {end} es {distance}")
        print(f"El camino más corto es: {' -> '.join(path)}")

        # Graficar el grafo y el camino más corto
        graficar_grafo(graph, path)
    except KeyError:
        print("Uno de los nodos especificados no existe en el grafo.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()
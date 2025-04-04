from flask import Flask, render_template, request
import os
from algoritmo import dijkstra, graficar_grafo

app = Flask(__name__)

def obtener_ultima_imagen():
    # Retornar siempre el nombre fijo de la imagen
    return "grafo_camino_mas_corto.png"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener los datos del formulario
        edges = request.form.get("edges")
        start = request.form.get("start")
        end = request.form.get("end")

        # Procesar las aristas ingresadas en formato de texto
        graph = {}
        try:
            for line_number, line in enumerate(edges.split("\n"), start=1):
                line = line.strip()
                if not line:
                    continue  # Ignorar líneas vacías
                try:
                    node1, node2, weight = line.split()
                    weight = int(weight)
                except ValueError:
                    return render_template(
                        "index.html",
                        error=f"Error en la línea {line_number}: '{line}'. Asegúrate de usar el formato 'nodo1 nodo2 peso'."
                    )
                if node1 not in graph:
                    graph[node1] = []
                if node2 not in graph:
                    graph[node2] = []
                graph[node1].append((node2, weight))
                graph[node2].append((node1, weight))  # Si el grafo es dirigido, elimina esta línea.
        except Exception as e:
            return render_template("index.html", error=f"Error inesperado: {str(e)}")

        # Ejecutar el algoritmo de Dijkstra
        try:
            distance, path = dijkstra(graph, start, end)
        except KeyError:
            return render_template("index.html", error="Uno de los nodos especificados no existe en el grafo.")
        except Exception as e:
            return render_template("index.html", error=f"Error inesperado: {str(e)}")

        # Generar el gráfico
        graficar_grafo(graph, path)

        # Obtener la última imagen generada
        imagen = obtener_ultima_imagen()

        # Redirigir a la página de resultados
        return render_template("result.html", distance=distance, path=" -> ".join(path), image=imagen)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
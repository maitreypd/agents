from langchain_core.runnables.graph import MermaidDrawMethod


class GraphVisualizer:
    @staticmethod
    def draw_graph(graph):
        png_data = graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        with open("graph.png", "wb") as f:
            f.write(png_data)
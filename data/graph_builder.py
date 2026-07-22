import os
import logging
import networkx as nx
import pandas as pd
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("GraphBuilder")

class GraphBuilder:
    def __init__(self):
        # We use a directed graph because traffic flow and wind corridors are directional
        self.graph = nx.DiGraph()
        self.output_dir = os.path.join(os.path.dirname(__file__), "processed")
        os.makedirs(self.output_dir, exist_ok=True)

    def add_nodes_from_data(self, node_data: list):
        """
        Adds nodes representing intersections or sensor locations.
        Expected data format: [{'id': 'node_1', 'lat': 23.81, 'lon': 90.41, 'pm25': 150.2}]
        """
        logger.info(f"Adding {len(node_data)} nodes to the graph.")
        for node in node_data:
            node_id = node.get("id")
            if not node_id:
                continue
            
            # Add node with features
            self.graph.add_node(
                node_id, 
                lat=node.get("lat"), 
                lon=node.get("lon"), 
                pm25=node.get("pm25", 0.0)
            )

    def add_edges_from_data(self, edge_data: list):
        """
        Adds edges representing roads connecting nodes.
        Expected data format: [{'source': 'node_1', 'target': 'node_2', 'traffic_speed': 15.5, 'wind_factor': 0.8}]
        """
        logger.info(f"Adding {len(edge_data)} edges to the graph.")
        for edge in edge_data:
            source = edge.get("source")
            target = edge.get("target")
            if source and target:
                # Invert traffic speed to represent 'bottleneck/friction' weight
                # Slower speed = higher weight
                speed = edge.get("traffic_speed", 30.0)
                weight = 1.0 / speed if speed > 0 else 999.0
                
                self.graph.add_edge(
                    source, 
                    target, 
                    traffic_speed=speed,
                    wind_factor=edge.get("wind_factor", 1.0),
                    weight=weight
                )

    def export_graph_for_stgcn(self, filename: str = "stgcn_graph.json"):
        """
        Exports the graph topology (Adjacency list and Node features) into a JSON format suitable for PyTorch Geometric / STGCN.
        """
        logger.info("Exporting graph topology for STGCN.")
        
        data = {
            "nodes": [],
            "edges": []
        }
        
        for node, attr in self.graph.nodes(data=True):
            data["nodes"].append({"id": node, "features": attr})
            
        for source, target, attr in self.graph.edges(data=True):
            data["edges"].append({"source": source, "target": target, "features": attr})
            
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
        logger.info(f"Graph exported successfully to {filepath}")
        return filepath

if __name__ == "__main__":
    # Example execution
    builder = GraphBuilder()
    
    # Mock data
    nodes = [
        {"id": "intersection_1", "lat": 23.8103, "lon": 90.4125, "pm25": 140.5},
        {"id": "intersection_2", "lat": 23.8120, "lon": 90.4150, "pm25": 145.0}
    ]
    edges = [
        {"source": "intersection_1", "target": "intersection_2", "traffic_speed": 12.0, "wind_factor": 1.1}
    ]
    
    builder.add_nodes_from_data(nodes)
    builder.add_edges_from_data(edges)
    builder.export_graph_for_stgcn()

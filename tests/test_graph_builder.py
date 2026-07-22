import os
import sys
import pytest
import networkx as nx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.graph_builder import GraphBuilder

def test_graph_initialization():
    builder = GraphBuilder()
    assert isinstance(builder.graph, nx.DiGraph), "Graph must be directed (DiGraph) to model flow."
    assert len(builder.graph.nodes) == 0

def test_add_nodes():
    builder = GraphBuilder()
    nodes = [
        {"id": "node_A", "lat": 23.1, "lon": 90.1, "pm25": 50.0},
        {"id": "node_B", "lat": 23.2, "lon": 90.2, "pm25": 60.0}
    ]
    builder.add_nodes_from_data(nodes)
    
    assert len(builder.graph.nodes) == 2
    assert "node_A" in builder.graph
    assert builder.graph.nodes["node_A"]["pm25"] == 50.0

def test_topological_connectivity():
    builder = GraphBuilder()
    builder.add_nodes_from_data([{"id": "node_A"}, {"id": "node_B"}])
    
    edges = [
        {"source": "node_A", "target": "node_B", "traffic_speed": 10.0}
    ]
    builder.add_edges_from_data(edges)
    
    assert len(builder.graph.edges) == 1
    assert builder.graph.has_edge("node_A", "node_B")
    
    # Test directional topology - edge should not exist in reverse
    assert not builder.graph.has_edge("node_B", "node_A")
    
    # Test weight calculation (inverse of speed)
    weight = builder.graph.edges["node_A", "node_B"]["weight"]
    assert weight == 1.0 / 10.0

def test_graph_export():
    builder = GraphBuilder()
    builder.add_nodes_from_data([{"id": "n1"}])
    filepath = builder.export_graph_for_stgcn("test_export.json")
    
    assert os.path.exists(filepath)
    os.remove(filepath) # Cleanup

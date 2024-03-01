import streamlit as st
import json
import uuid
import networkx as x
from model import metamodel_dict
from streamlit_agraph import agraph, Node, Edge, Config
import graphviz
from graph_functions import output_nodes_and_edges, count_nodes
def print_hi(name, age):
    st.success(f'Hi, My name is {name} and i am {age} years old')  # Press Ctrl+F8 to toggle the breakpoint.

def graph_dict():
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"]
    }
    st.session_state["graph_dict"] = graph_dict

def save_node(name,age):
    node_dict = {
        "name": name,
        "age": age,
        " id": str(uuid.uuid4()),
        "type": "Node"
    }
    st.session_state["node_list"].append(node_dict)
def save_edge(node1,relation,node2):
    edge_dict = {
        "source": node1,
        "target": node2,
        "type": relation,
        " id": str(uuid.uuid4()),
    }
    st.session_state["edge_list"].append(edge_dict)
def upload_graph():
    uploaded_graph = st.file_uploader("upload an existing graph", type="json")
    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)
        uploaded_nodes = uploaded_graph_dict["nodes"]
        uploaded_edges = uploaded_graph_dict["edges"]
        st.write(uploaded_graph_dict)
    else:
        st.info("Please upload graph if available")
    update_graph_button = st.button("Update Graph",use_container_width=True, type="primary")
    if update_graph_button:
        st.session_state["node_list"] = uploaded_nodes
        st.session_state["edge_list"] = uploaded_edges
def create_node():
    name_node = st.text_input("Type in the name of the node")
    age_node = st.number_input("Type in the age of the node", value=0)
    type_node = st.selectbox("Specify the type of node", ["Node","Person"])
    Save_node_button = st.button("Save details", use_container_width=True, type="primary")
    if Save_node_button:
        save_node(name_node, age_node,type_node)
        print_hi(name_node, age_node)
def create_relations():
    node1_col, relation_col, node2_col = st.columns(3)
    node_list = st.session_state["node_list"]
    node_name_list = []
    for node in node_list:
        node_name_list.append(node["name"])
        with node1_col:
            node1_select = st.selectbox("Select the first node",options=node_name_list,key="node1_select")

        with relation_col:
            relation_list = metamodel_dict["edges"]
            relation_name = st.selectbox("Specify the relation",options=relation_list)
        with node2_col:
            node2_select = st.selectbox("Select the second node",options=node_name_list,key="node2_select")
        store_edge_button = st.button("Save relation",use_container_width=True, type="primary")
        if store_edge_button:
            save_edge(node1_select, relation_name, node2_select)
        st.write(f"{node1_select} is {relation_name}  {node2_select}")
        st.write(st.session_state["node_list"])
        st.write(st.session_state["edge_list"])

def store_graph():
    store_graph_button = st.button("Save Graph", use_container_width=True, type="primary")
    with st.expander("Show Graph JSON"):
        st.json(st.session_state["node_list"], expanded=False)
        st.json(st.session_state["edge_list"], expanded=False)
        graph_dict()
    with st.expander("Show Graph JSON", expanded=False):
        st.json(graph_dict)
def visualize_graph():
    def set_color(node_type):
        color = "Grey",
        if node_type == "Person":
            color = "Blue"
        elif node_type == "Node":
            color = "Red"
        elif node_type == "Resource":
            color = "Yellow"
        elif node_type == "Sensor":
            color = "White"
        return color
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"]
    }
    st.session_state["graph_dict"] = graph_dict
    with st.expander("Show Graph", expanded=False):
        graph = graphviz.Digraph()
        graph_dict = st.session_state["graph_dict"]
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]
        for node in node_list:
            node_name = node["name"]
            graph.node(node_name)

        for edge in edge_list:
            source = edge["source"]
            target = edge["target"]
            label = edge["type"]
            graph.edge(source, target, label=label)
    with st.expander("Agraph Visualization", expanded=False):
        nodes = []
        edges = []

        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]

        for node in node_list:
            nodes.append(Node(id=node["name"], label=node["name"]))

        # for edge in edge_list:
        #     for node in node_list:
        #         if edge["source"]==node["name"]:
        #             source=node["id"]
        #         elif edge["target"]==node["name"]:
        #             target=node["id"]
        #         edges.append(Edge(source=source, target=target, label=edge["type"]))
        #     edges.append(Edge(source=source, target=target, label=edge["type"]))
        for edge in edge_list:
            edges.append(Edge(source=edge['source'], target=edge['target'], label=edge["type"]))

        config = Config(width=500,
                        height=500,
                        directed=True,
                        physics=True,
                        hierarchical=False,
                        )
    st.graphviz_chart(graph)
def export_graph():
    graph_string = json.dumps(st.session_state["graph_dict"])
    st.download_button("Export Graph to JSON ", file_name="graph.json", mime="application/json", data=graph_string,
                       use_container_width=True, type="primary")
def analyze_graph():
    G = x.Graph()

    graph_dict = st.session_state['graph_dict']
    node_list = graph_dict['nodes']
    edge_list = graph_dict['edges']
    node_tuple_list = []
    edge_tuple_list = []

    for node in node_list:
        node_tuple = (node["name"], node)
        node_tuple_list.append(node_tuple)

    for edge in edge_list:
        edge_tuple = (edge["source"], edge["target"], edge)
        edge_tuple_list.append(edge_tuple)

    G.add_nodes_from(node_tuple_list)
    G.add_edges_from(edge_tuple_list)

    select_function = st.selectbox(label="select function", options=["output nodes and edges", "Count nodes"])

    if select_function == "Output nodes and edges":
        output_nodes_and_edges(graph=G)
    elif select_function == "Count nodes ":
        count_nodes(graph=G)
    output_nodes_and_edges(graph=G)
    count_nodes(graph=G)
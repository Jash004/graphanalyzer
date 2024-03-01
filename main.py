import random
import uuid
import json
import graphviz
import networkx as x
from streamlit_agraph import agraph, Node, Edge, Config
from graph_functions import output_nodes_and_edges, count_nodes
from streamlit_option_menu import option_menu
from tabs import upload_graph, create_node, create_relations, store_graph, visualize_graph, export_graph, analyze_graph
import streamlit as st
from model import metamodel_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    st.title("Jash")
    tab_list = ["Import a Graph" ,"Create Nodes", "Create relations between Nodes", "Store the graph","Export the graph", " Visualize the graph", "Analyze the Graph"]
    import_graph_tab, create_node_tab, create_relations_tab, store_graph_tab, export_graph_tab, visualize_graph_tab, analyze_graph_tab = st.tabs(tab_list)
    # with st.sidebar:
    selected_tab = option_menu("Main Menu", tab_list,
                               icons=['house', 'gear','arrow clockwise'], menu_icon="cast", default_index=0,orientation="horizontal")

    st.write(selected_tab)
    if selected_tab == "Import a Graph":
        upload_graph()
    if selected_tab == "Create Nodes":
        create_node()

    if selected_tab == "Create relations between Nodes":
        create_relations()
    if selected_tab == "Store the graph":
        store_graph()


    if selected_tab == " Visualize the graph":
        visualize_graph()

    if selected_tab == "Export the graph":
        export_graph()

    if selected_tab == "Analyze the Graph":
        analyze_graph()





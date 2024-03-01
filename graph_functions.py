import networkx as nx
import streamlit as st
import networkx as x

def output_nodes_and_edges(graph:nx.Graph):
    st.write(graph.nodes)
    st.write(graph.edges)


def count_nodes(graph:nx.Graph):
    count= graph.number_of_nodes()
    st.info(f"Total number of nodes are {count}")

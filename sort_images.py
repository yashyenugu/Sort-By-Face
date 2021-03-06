import pickle
import numpy as np
import networkx as nx
import os
import shutil
import argparse
import sys

from CW import draw_graph,chinese_whispers

def image_sorter(G):
    """Copies images from the source and pastes them to a directory.
    Each sub directory represents a cluster which contains images of the cluster assigned by
    the clustering algorithm

    Args:
        graph : networkx graph on which the clustering algorithm has been done on
    """
    root = "Sorted-pictures"
    if not os.path.exists(root):
        os.mkdir(root)

    for node,attribute in G.nodes.items():

        # Get the image path from the node of the graph and copy it to a subdirectory with the name of the cluster
        source = attribute["source"]
        destination = os.path.join(root,attribute["cluster"])

        if not os.path.exists(os.path.join(root,attribute["cluster"])):
            os.mkdir(os.path.join(root,attribute["cluster"]))
        try: 
            shutil.copy(source,destination)
        except FileNotFoundError:
            pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--threshold", type=float, required=False, default=0.67, help="minimum  distance required between face embeddings to form a edge")
    
    parser.add_argument(
        "-itr", "--iterations", type=int, required=False, default=30, help="number of iterations for the Chinese Whispers algorithm")

    args = vars(parser.parse_args())

    #Load the embeddings
    try:
        data = pickle.load(open("embeddings.pickle","rb"))
        
    except FileNotFoundError:
        print("No saved embeddings found. Please run the script embedder.py")
        sys.exit(1)
    
    # Draw the initial graph
    graph = draw_graph(data,args["threshold"])

    # Run the clustering algorithm on the graph
    graph = chinese_whispers(graph,args["iterations"])

    # Sort the images using the clusters
    image_sorter(graph)
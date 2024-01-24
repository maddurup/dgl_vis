import os
import json
import pandas as pd
import s3fs
import pickle
import sys
import dgl
from sampler import HeteroGraphNeighborSampler
import boto3

def load_graph_s3(bucket, prefix, key):
    # Function to load a graph from an S3 bucket
    if prefix.startswith('s3://'):
        prefix = prefix[len('s3://'+bucket+'/'):]
    path = os.path.join(prefix, key)
    s3 = boto3.resource('s3')
    N = pickle.loads(
        s3.Bucket(bucket).Object(path).get()['Body'].read()
    )
    return N

def load_graph_from_s3(bucket, prefix, key):
    fs = s3fs.S3FileSystem(anon=False)
    fs.access_key = os.environ.get('AWS_ACCESS_KEY_ID') 
    fs.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    with fs.open(os.path.join(prefix, key), 'rb') as f:
        g_meta = pickle.load(f)
    return g_meta

def get_graph_metadata(g_meta):
    # Extract graph and metadata from the loaded graph
    g = g_meta[0]
    id_to_node_all = g_meta[3]
    node_to_id_all = {k: {vx: kx for kx, vx in v.items()} for k, v in id_to_node_all.items()}
    return g, id_to_node_all, node_to_id_all

def sample_graph(g, category, nhops, fanout, seeds):
    # Sample a graph using the HeteroGraphNeighborSampler
    protosampler = HeteroGraphNeighborSampler(
        g=g,
        category=category,
        nhops=nhops,
        fanout=fanout
    )
    blocks, seeds, batch_nids, input_nodes = protosampler.sample_block(seeds)
    
    block_node_to_graph_id = {}
    graph_id_to_block_node = {}
    for k, v in input_nodes.items():
        block_node_to_graph_id[k] = {i : int(n) for i, n in enumerate(v)}
        graph_id_to_block_node[k] = {int(n) : i for i, n in enumerate(v)}
        
    return blocks, seeds, batch_nids, input_nodes, block_node_to_graph_id, graph_id_to_block_node

def get_node_id(mapping, ntype, node_id):
    return mapping[ntype][mapping[ntype][node_id]]

def get_root_node_id(block_mapping, graph_mapping, ntype, node_id):
    graph_node_id = block_mapping[ntype][node_id]
    return graph_mapping[ntype][graph_node_id]

def get_block_nodes_and_edges_list(blocks, block_mapping, graph_mapping):
    nodes_edges = []
    for block in blocks:
        for etype in block.canonical_etypes: 
            print(etype)
            src, dst = block.all_edges(etype=etype)
            if len(src)>0:
                src_node_type = etype[0]
                dst_node_type = etype[2]
                edge_type = etype[1]
                src_root_node = [get_root_node_id(block_mapping, graph_mapping, src_node_type, int(i)) for i in src]
                dst_root_node = [get_root_node_id(block_mapping, graph_mapping, dst_node_type, int(i)) for i in dst]

                nodes_edges.extend([(src_t, s, dst_t, d, e)  
                                    for s, d, e in zip(src_root_node, dst_root_node, etype)])

                # nodes_edges.append({'src_node_type' : src_node_type, 'dst_node_type' : dst_node_type, 'edge_type' : edge_type, 'src_node' : src_root_node, 'dst_node' : dst_root_node})
            

    # df = pd.DataFrame(nodes_edges, columns=['src_node_type', 'src_node', 
    #                                         'dst_node_type', 'dst_node',
    #                                         'edge_type'])
    
    return nodes_edges

def extract_nodes_edges(blocks, block_mapping, graph_mapping):

    nodes_edges = []
    for block in blocks:
        for etype in block.canonical_etypes:  

            if etype[1] == "self_relation":
                continue
            
            try:
                src_type = etype[0]
                dst_type = etype[2]
                edge_type = etype[1]

                src, dst = block.edges(etype=edge_type)
                src_nodes = [get_root_node_id(block_mapping, graph_mapping, src_type, int(i)) for i in src]  
                dst_nodes = [get_root_node_id(block_mapping, graph_mapping, dst_type, int(i)) for i in dst]

                for s, d in zip(src_nodes, dst_nodes):
                    payload = {
                        "src_node_type": src_type,
                        "dst_node_type": dst_type,
                        "edge_type": edge_type,
                        "src_node": s, 
                        "dst_node": d
                    }
                    nodes_edges.append(payload)
            except exception as e:
                print(e)
                print(src_nodes, dst_nodes)

    return nodes_edges
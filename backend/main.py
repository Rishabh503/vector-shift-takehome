from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


def is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
   
    node_ids = {n.id for n in nodes}

    
    adj = {n.id: [] for n in nodes}
    for e in edges:
        if e.source in adj:
            adj[e.source].append(e.target)

  
    state = {n: 0 for n in node_ids}

    def has_cycle(node: str) -> bool:
        state[node] = 1
        for neighbour in adj.get(node, []):
            if neighbour not in state:
                continue
            if state[neighbour] == 1:
                return True
            if state[neighbour] == 0 and has_cycle(neighbour):
                return True
        state[node] = 2
        return False

    for node_id in node_ids:
        if state[node_id] == 0:
            if has_cycle(node_id):
                return False

    return True


@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    dag = is_dag(pipeline.nodes, pipeline.edges)

    return {
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'is_dag': dag,
    }
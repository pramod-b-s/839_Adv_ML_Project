from cProfile import label
from http.client import NETWORK_AUTHENTICATION_REQUIRED
import json
import networkx as nx
import matplotlib.pyplot as plt
from string import ascii_lowercase 

class graphNode:
    proc_type = 'cpu'
    proc_ph = 'X'
    proc_name = 'name'
    proc_pid = 0
    proc_tid = 0
    proc_ts = 0
    proc_dur = 0

    def _print_node(self):
        print(' Type: ', self.proc_type, ' Ph: ', self.proc_ph, ' Name: ', self.proc_name, ' PID: ', self.proc_pid,
        ' TID: ', self.proc_tid, ' Timestamp: ', self.proc_ts, ' Duration: ', self.proc_dur)
    
    def construct_node(self, proc):
        self.proc_ph = proc['ph']
        self.proc_type = proc['cat']
        self.proc_ph = proc['name']
        self.proc_pid = proc['pid']
        self.proc_tid = proc['tid']
        self.proc_ts = proc['ts']
        self.proc_dur = proc['dur']
        

def printNodes(_nodeList):
    for node in _nodeList:
        node._print_node()

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

f = open('trace.json')
data = json.load(f)
nodeList = []
dep_graph = nx.Graph()
labelDict = {}
counter = 1
 
for proc in data['traceEvents']:
    if (('cat' in proc)): # and (proc['ts'] in range(1647025986525965, 1647025986529065))):
        # labelDict[str("Node" + str(counter))] = str(proc['name'])
        new_node = graphNode()
        new_node.construct_node(proc)
        # thr_graph[proc['tid']].append(new_node)
        nodeList.append(new_node)
        dep_graph.add_node(new_node)
        counter = counter + 1        

for node in dep_graph.nodes():
    labelDict[node] = node.proc_ph

f.close()

nodeList.sort(key = lambda proc: proc.proc_ts)
printNodes(nodeList)

## CPU jobs in same thread dependency
for nd_1, nd_2 in pairwise(nodeList):
    if ((nd_1.proc_type == nd_2.proc_type) and (nd_1.proc_tid == nd_2.proc_tid) 
        and (nd_1.proc_type == 'cpu_op') and (nd_2.proc_ts >= nd_1.proc_ts + nd_1.proc_dur)):
        dep_graph.add_edge(nd_1, nd_2)

## GPU jobs in same thread dependency
for nd_1, nd_2 in pairwise(nodeList):
    if ((nd_1.proc_type == nd_2.proc_type) and (nd_1.proc_tid == nd_2.proc_tid) 
        and (nd_1.proc_type == 'gpu_op') and (nd_2.proc_ts >= nd_1.proc_ts + nd_1.proc_dur)):
        dep_graph.add_edge(nd_1, nd_2)


# H = nx.relabel_nodes(G, mapping)
nx.draw(dep_graph, with_labels = True, labels = labelDict)
plt.show()
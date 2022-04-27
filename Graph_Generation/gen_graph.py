import json
import networkx as nx
import matplotlib.pyplot as plt


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
        self.proc_name = proc['name']
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


def display_graph(dep_graph, labelDict):
    nx.draw(dep_graph, with_labels = True, labels = labelDict)
    # print(nx.dag_longest_path_length(dep_graph))
    plt.show()


def construct_graph(traceFile):
    f = open(traceFile)
    data = json.load(f)
    nodeList = []
    dep_graph = nx.DiGraph()
    seenNodesCpu = {}
    seenNodesGpu = {}
    counter = 1

    for proc in data['traceEvents']:
        if (('cat' in proc)):
            new_node = graphNode()
            new_node.construct_node(proc)
            nodeList.append(new_node)
            dep_graph.add_node(new_node)
            counter = counter + 1        

    f.close()

    nodeList.sort(key = lambda proc: proc.proc_ts)
    # printNodes(nodeList)

    ## CPU jobs in same thread dependency
    for i in range(len(nodeList) - 2):
        for j in range(i + 1, len(nodeList) - 1):
            nd_1 = nodeList[i]
            nd_2 = nodeList[j]

            if ((nd_1.proc_type == nd_2.proc_type) and (nd_1.proc_tid == nd_2.proc_tid) 
                and (nd_1.proc_type == 'cpu_op') and ((nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur))
                and (nd_1 not in seenNodesCpu) and (nodeList.index(nd_2) > nodeList.index(nd_1))):
                if (nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur):
                    seenNodesCpu[nd_1] = True
                dep_graph.add_edge(nd_1, nd_2)


    ## GPU jobs in same thread dependency
    for i in range(len(nodeList) - 2):
        for j in range(i + 1, len(nodeList) - 1):
            nd_1 = nodeList[i]
            nd_2 = nodeList[j]

            if ((nd_1.proc_type == nd_2.proc_type) and (nd_1.proc_tid == nd_2.proc_tid) 
                and (nd_1.proc_type == 'gpu_op') and ((nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur)) 
                and (nd_1 not in seenNodesGpu) and (nodeList.index(nd_2) > nodeList.index(nd_1))):
                if (nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur):
                    seenNodesGpu[nd_1] = True
                dep_graph.add_edge(nd_1, nd_2)

    # print(len(nodeList))
    # H = nx.relabel_nodes(G, mapping)
    return dep_graph

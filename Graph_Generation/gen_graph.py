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
    sim_ref = 0
    proc_args = {}

    def _print_node(self):
        print(' Type: ', self.proc_type, ' Ph: ', self.proc_ph, ' Name: ', self.proc_name, ' PID: ', self.proc_pid,
        ' TID: ', self.proc_tid, ' Timestamp: ', self.proc_ts, ' Duration: ', self.proc_dur, 'Ref: ', self.sim_ref,
        ' Args: ', self.proc_args)

    
    def construct_node(self, proc):
        self.proc_ph = proc['ph']
        self.proc_type = proc['cat']
        self.proc_name = proc['name']
        self.proc_pid = proc['pid']
        self.proc_tid = proc['tid']
        self.proc_ts = proc['ts']
        
        if "dur" in proc:
            self.proc_dur = proc['dur']
        else:
            self.proc_dur = 0
        
        if "args" in proc:
            self.proc_args = proc['args']
        else:
            self.proc_args = {}



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
    seenNodesComm = {}
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
    for i in range(len(nodeList) - 1):
        for j in range(i + 1, len(nodeList)):
            nd_1 = nodeList[i]
            nd_2 = nodeList[j]

            if ((nd_1.proc_type == nd_2.proc_type) and (nd_1.proc_tid == nd_2.proc_tid) 
                and (nd_1.proc_type == 'cpu_op') and ((nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur))
                and (nd_1 not in seenNodesCpu) and (nodeList.index(nd_2) > nodeList.index(nd_1))
                and (("gloo" not in nd_1.proc_name) and ("gloo" not in nd_2.proc_name))):
                if (nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur):
                    seenNodesCpu[nd_1] = True

                dep_graph.add_edge(nd_1, nd_2)


    ## GPU jobs in same thread dependency
    for i in range(len(nodeList) - 1):
        for j in range(i + 1, len(nodeList)):
            nd_1 = nodeList[i]
            nd_2 = nodeList[j]

            if ((nd_1.proc_type == nd_2.proc_type) and (nd_1.proc_tid == nd_2.proc_tid) 
                and (nd_1.proc_type == 'gpu_op') and ((nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur)) 
                and (nd_1 not in seenNodesGpu) and (nodeList.index(nd_2) > nodeList.index(nd_1))
                and (("gloo" not in nd_1.proc_name) and ("gloo" not in nd_2.proc_name))):
                if (nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur):
                    seenNodesGpu[nd_1] = True

                dep_graph.add_edge(nd_1, nd_2)


    ## Correlation from CUDA APIs to GPU kernels
    for i in range(len(nodeList) - 1):        
        nd_1 = nodeList[i]

        if ((len(nd_1.proc_args) != 0) and ("correlation" in nd_1.proc_args)):
            correlation_id = nd_1.proc_args['correlation']

            for j in range(i + 1, len(nodeList)):                
                nd_2 = nodeList[j]
                if ((len(nd_2.proc_args) != 0) and ("correlation" in nd_2.proc_args) and 
                    (nd_2.proc_args['correlation'] == correlation_id)):            
                    dep_graph.add_edge(nd_1, nd_2)


    ## Correlation from CUDA APIs to GPU kernels
    for i in range(len(nodeList)):        
        nd_1 = nodeList[i]
        tmpAsyncNodeList = []

        if (nd_1.proc_name == "async_gpu"):
            tmpAsyncNodeList.append(nd_1)
        elif (nd_1.proc_name == "Kernel"):
            for j in range(len(tmpAsyncNodeList)):
                dep_graph.add_edge(tmpAsyncNodeList[j], nd_1)


    ## Dependency between communication and CPU jobs
    for i in range(len(nodeList) - 1):
        for j in range(i + 1, len(nodeList)):
            nd_1 = nodeList[i]
            nd_2 = nodeList[j]

            if (((nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur) or (nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur))
                and (nd_2 not in seenNodesComm) and (("gpu" not in nd_1.proc_name) and ("gloo" not in nd_1.proc_name) 
                and ("gloo" in nd_2.proc_name))):
                if (nd_2.proc_ts > nd_1.proc_ts + nd_1.proc_dur):
                    seenNodesComm[nd_2] = True
                
                dep_graph.add_edge(nd_1, nd_2)

                for k in range(i, len(nodeList) - 1):
                    nd_3 = nodeList[k]
                    if ((nd_3.proc_ts < nd_2.proc_ts + nd_2.proc_dur) and 
                        (nd_3.proc_ts + nd_3.proc_dur > nd_2.proc_ts + nd_2.proc_dur)):
                        dep_graph.add_edge(nd_2, nd_3)
                        break


    # print(len(nodeList))
    # H = nx.relabel_nodes(G, mapping)
    return dep_graph

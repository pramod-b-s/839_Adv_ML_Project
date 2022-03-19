import json
import networkx as nx

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


f = open('trace.json')
data = json.load(f)
nodeList = []
dep_graph = nx.Graph()
 
for proc in data['traceEvents']:
    if 'cat' in proc:
        new_node = graphNode()
        new_node.proc_ph = proc['ph']
        new_node.proc_type = proc['cat']
        new_node._print_node()
        nodeList.append(new_node)
        dep_graph.add_node(new_node)

f.close()
import json
from Graph_Generation import gen_graph


def transform_amp(orig_dep_graph):
    _F = []
    _P = {}

    nodeList = []
    for node in orig_dep_graph.nodes:
        nodeList.append(node)
        node.sim_ref = len(list(orig_dep_graph.predecessors(node)))

        if (node.sim_ref == 0):
            _F.append(node)


    while (len(_F) != 0):
        _u = _F[0]
        _t = _u.proc_tid
        _F.pop(0)
        if (_t in _P):
            _u.proc_ts = max(_P[_t], _u.proc_ts)
        else:
            _u.proc_ts = _u.proc_ts
            
        _P[_t] = _u.proc_ts + _u.proc_dur

        for _c in orig_dep_graph.successors(_u):
            _c.sim_ref = _c.sim_ref - 1
            _c.proc_ts = max(_c.proc_ts, _u.proc_ts + _u.proc_dur)

            if (_c.sim_ref == 0):
                _F.append(_c)

    
    nodeTime = []
    for node in orig_dep_graph.nodes:
        nodeTime.append(int(node.proc_ts) + int(node.proc_dur))

    return (max(nodeTime) - min(nodeTime))



        

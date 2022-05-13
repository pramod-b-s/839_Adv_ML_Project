from Graph_Generation import gen_graph
from Graph_Transformations import transform_graph
from Graph_Simulation import simulate_graph

import networkx as nx
import time as tm
import os


def main():
    trace = "trace_resnet18.json"

    while (1):
        print("0-> Specify TF\n1-> Construct DG\n2-> View DG\n3-> Add FP Txs\n4-> Simulate FP Graph")
        ch = input("5-> DAG Longest Path Dur\n6-> blank\n7-> Get SubG\n9-> Exit\n")        

        if (ch == "0"):
            trace = input("Enter trace file path\n")
            # trace = "trace2.json"
            print("Using trace file: " + trace)  

        elif (ch == "1"):            
            start = tm.time()
            dep_graph = gen_graph.construct_graph(trace)
            end = tm.time()
            print(end - start)
            print("Constructed dependency graph from file")                      

        elif (ch == "2"):            
            if (dep_graph.number_of_nodes() == 0):
                print("Graph not generated")
            else:
                labelDict = {}
                for node in dep_graph.nodes():
                    labelDict[node] = node.proc_name
                
                gen_graph.display_graph(dep_graph, labelDict)

        elif (ch == "3"):
            transform_graph.select_task_amp(trace)
            print("Applied FP transformations")            

        elif (ch == "4"):            
            new_iter_time = simulate_graph.transform_amp(dep_graph)
            print("Simulated graph with FP Txs has iteration time: ", new_iter_time[0],  new_iter_time[1])

        elif (ch == "5"):
            dag_path = nx.dag_longest_path(dep_graph)
            time = []
            for nd in dag_path:
                time.append(float(nd.proc_ts))
                time.append(float(nd.proc_ts) + float(nd.proc_dur))
                        
            print('Longest path has length ', len(dag_path))
            # print('DAG duration sum ', sum(time))
            print('DAG duration diff ', max(time) - min(time))

        elif(ch == "6"):
            nodeTime = []
            for node in dep_graph.nodes():
                nodeTime.append(int(node.proc_ts) + int(node.proc_dur))

        elif (ch == "7"):      
            filtered_nodes = [node for node in dep_graph.nodes() if ('cuda' in node.proc_name)]
            dep_graph = dep_graph.subgraph(filtered_nodes)
            # print(filtered_nodes)  
            # print(dep_graph.nodes())   

        elif (ch == "8"):
            traceFile = ['trace_resnet18.json', 'trace_GoogLeNet.json', 'trace_mobilenet.json']
            iters = [100, 10, 1]
            for f in traceFile:
                filePath = "graph_" + str(os.path.splitext(f)[0]) + ".gr"                
                print('trace ', f)
                start = tm.time()
                for i in iters:
                    dep_graph = gen_graph.construct_graph(f)
                end = tm.time()

                print('Average construct time for trace ', f, ' from ', str(i), ' runs ', float(end - start)/int(i))
                if os.path.exists(filePath):
                    os.remove(filePath)

        elif (ch == "9"):
            break



if __name__=="__main__":
    main()
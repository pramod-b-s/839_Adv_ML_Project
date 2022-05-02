from Graph_Generation import gen_graph
from Graph_Transformations import transform_graph
from Graph_Simulation import simulate_graph

def main():
    trace = "trace.json"

    while (1):
        ch = input("0-> Specify TF\n1-> Construct DG\n2-> View DG\n3-> Add FP Txs\n4-> Simulate FP Tx Graph\n5-> Quit\n")        

        if (ch == "0"):
            trace = input("Enter trace file path\n")
            # trace = "trace2.json"
            print("Using trace file: " + trace)  

        elif (ch == "1"):
            dep_graph = gen_graph.construct_graph(trace)    
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
            dep_graph = simulate_graph.transform_amp(dep_graph)
            print("Simulated graph with FP Txs")

        elif (ch == "5"):
            break


if __name__=="__main__":
    main()
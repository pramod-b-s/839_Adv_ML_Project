from Graph_Generation import gen_graph
from Graph_Transformations import transform_graph

def main():
    trace = input("Enter trace file path\n")
    dep_graph = gen_graph.construct_graph(trace)    

    while (1):
        ch = input("1-> Load dependency graph\n2-> View dependency graph\n3-> Add transformation\n4-> Check result of current transformations\n5-> Undo all transformations\n6-> Quit\n")        

        if (ch == "1"):
            print("Loading dependency graph from file")            

        elif (ch == "2"):            
            if (dep_graph.number_of_nodes() == 0):
                print("Graph not generated")
            else:
                labelDict = {}
                for node in dep_graph.nodes():
                    labelDict[node] = node.proc_name
                
                gen_graph.display_graph(dep_graph, labelDict)

        elif (ch == "3"):
            print("Applying transformation")

        elif (ch == "4"):
            print("Check effect of transformations")

        elif (ch == "5"):
            print("Undo transformations")

        elif (ch == "6"):
            break


if __name__=="__main__":
    main()
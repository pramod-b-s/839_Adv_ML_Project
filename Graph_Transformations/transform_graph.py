import json


def insert_task(traceFile):
    f = open(traceFile)
    data = json.load(f)
    inputEle = input("Enter json object to insert\n")
    data.append(inputEle)
    
    with open(traceFile, 'w') as outfile:
        json.dump(data, outfile)


def delete_task(traceFile):
    f = open(traceFile)
    data = json.load(f)
    # name = input("Enter name of task\n") 
    name = "aten::empty"
    
    for i in range(len(data['traceEvents'])):
        if (data[i]['name'] == name):
            data.pop(i)
    
    with open(traceFile, 'w') as outfile:
        json.dump(data, outfile)


def select_task_amp(traceFile):
    f = open(traceFile)
    data = json.load(f)

    for gt in data['traceEvents']:
        if (("cat" in gt) and (gt["cat"] == "gpu_op")):
            if (("sgemm" in gt['name']) or ("scudnn" in gt['name'])):
                gt['dur'] = (gt['dur'] / 3)
            else:
                gt['dur'] = (gt['dur'] / 2)

    with open(traceFile, 'w') as outfile:
        json.dump(data, outfile)


'''def select_task_gpu(traceFile):
    f = open(traceFile)
    data = json.load(f)
    if (len(tasks) == 0):
        dataF = data['traceEvents']
    else:
        dataF = tasks

    tasks = [d for d in dataF if d['cat'] == 'gpu_op']
'''

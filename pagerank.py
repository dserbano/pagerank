import matplotlib.pyplot as plt, os
import matplotlib.ticker as mticker
import time

def print_figure(figure_name):
    figure_path = os.path.join(os.path.join(os.getcwd(), "figures"))
    
    if os.path.isdir(figure_path):
        plt.savefig(os.path.join(figure_path, figure_name), quality=99)
    else:
        os.mkdir(figure_path)
        plt.savefig(os.path.join(figure_path, figure_name), quality=99)
    return

def printListResults(arr:list, title, cols, func):
    print(title)
    print("-".join(cols))
    for i in range(0, len(arr)):
        print(func(arr[i]))

def plotHistogram(plot_title:str, d:list, start:float, end:float, buckets:int):
    #print in local folder "figures"
    diff = float(abs(end - start)/buckets)
    intervals =  [{"start": start + i*diff, "end": start + (i + 1)*diff, "middle": (start + (i + 1)*diff + start + i*diff)/2}  for i in range(0, buckets)]
    values = [interval["middle"] for interval in intervals]
    count = [0 for i in range(0, len(intervals))]
    for i in range(0, len(d)):
        j = 0
        found = False
        while (j < len(intervals) and found == False):
            if d[i] >= intervals[j]["start"] and d[i] <= intervals[j]["end"]:
                count[j] = count[j] + 1 
            j = j + 1
    count = [val if val != 0 else float('nan') for val in count]
  
    plt.figure()
    plt.xlabel('PageRank Scores')
    plt.ylabel('Number of instances')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
    g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(g))
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(g))
    plt.gcf().subplots_adjust(left=0.15)
    plt.plot(values, count, color='b', marker='*', linestyle='')
    print_figure(plot_title)

    #prints the same histogram but skips first 3 buckets
    plt.figure()
    plt.xlabel('PageRank Scores')
    plt.ylabel('Number of instances')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
    g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(g))
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(g))
    plt.gcf().subplots_adjust(left=0.15)
    plt.plot(values[3:len(values)], count[3:len(count)], color='b', marker='*', linestyle='')
    print_figure(plot_title + "_skip_3")



def nMaxElements(arr:list, N:int): 
    nMax = [] 
    localArr = arr.copy()
  
    for i in range(0, N):  
        maximum = {"pos": -float('inf'), "value": -float('inf')}
        for j in range(0, len(localArr)):
            if localArr[j] > maximum["value"]:
                maximum = {"pos": j, "value": float(localArr[j])}            
        localArr.remove(maximum["value"])
        nMax.append(maximum) 
    
    del localArr
    return nMax

def nMinElements(arr:list, N:int): 
    nMin = [] 
    localArr = arr.copy()
  
    for i in range(0, N):  
        minimum = {"pos": float('inf'), "value": float('inf')}
        for j in range(0, len(localArr)):
            if localArr[j] < minimum["value"] and localArr[j] != 0:
                minimum = {"pos": j, "value": float(localArr[j])}     
        localArr.remove(minimum["value"]); 
        nMin.append(minimum) 

    del localArr
    return nMin

def MSE(a:list, b:list):
    summation = 0 
    for i in range (0, len(a)):   
        summation = summation + (a[i] - b[i])**2 
    return summation/len(a) 

def pageRank(M:list, iterations:int, threshold:int = None):
    start_exec = time.perf_counter()    
    init_d = float(1/len(M))
    d = [init_d for item in range(0, len(M))]
    MSEs = []
    count = 0
    stop = False
    while (count < iterations):
        old_d = d.copy()
        for i in range(0, len(M)):
            new_d = 0
            for j in range(0, len(M[i])):
                new_d = new_d + M[i][j]["value"] * d[M[i][j]["col"]]
            d[i] = float(new_d) 
        current_MSE = MSE(old_d, d)
        if threshold != None and len(MSEs) > 0:
            diff_MSE = abs(current_MSE - MSEs[len(MSEs)])
            if diff_MSE < threshold:
                stop = True
        MSEs.append(current_MSE)
        count = count + 1
    stop_exec = time.perf_counter()   
    print("EXEC TIME Normal PageRank ", iterations, threshold, f"{stop_exec - start_exec:0.4f} seconds") 
    return d, MSEs, count

def pageRankImproved(M:list, iterations:int, a:int, threshold:int = None):
    start_exec = time.perf_counter()    
    init_d = float(1/len(M))
    d = [init_d for item in range(0, len(M))]
    MSEs = []
    count = 0
    stop = False
    while (count < iterations and stop == False):
        old_d = d.copy()
        for i in range(0, len(M)):
            new_d = 0 
            for j in range(0, len(M[i])):
                new_d = new_d + M[i][j]["value"] * d[M[i][j]["col"]]
            d[i] = a * float(new_d) + (1 - a) * 1
        current_MSE = MSE(old_d, d)
        if threshold != None and len(MSEs) > 0:
            diff_MSE = abs(current_MSE - MSEs[len(MSEs) - 1])
            if diff_MSE < threshold:
                stop = True
        MSEs.append(current_MSE)
        count = count + 1
    stop_exec = time.perf_counter()   
    print("EXEC TIME Improved PageRank ", iterations, threshold, f"{stop_exec - start_exec:0.4f} seconds")
    return d, MSEs, count

csv_file_r = open("web-Google.txt", newline='')
csv_file_r.readline()
csv_file_r.readline()
csv_file_r.readline()
csv_file_r.readline()

#reading the data and preprocessing it at the same time
nr_nodes = 916428
population_cols = [0 for item in range(0, nr_nodes)]
M = [[] for item in range(0, nr_nodes)]

line = csv_file_r.readline()

while (line):
    line = line.strip("\n").strip("\r").split("\t")
    i = int(line[0])
    j = int(line[1])

    M[j].append({"value": 0, "col": i})
    population_cols[i] = population_cols[i] + 1

    line = csv_file_r.readline()

    
for i in range(0, len(M)):
    for j in range(0, len(M[i])):
        M[i][j]["value"] = 1/(population_cols[M[i][j]["col"]])


# Normal PageRank 10 iterations
d_1, MSE_1, actual_iterations_1 = pageRank(M, 10)
top20PageRank_1 = nMaxElements(d_1, 20)
bottom20PageRank_1 = nMinElements(d_1, 20)

printListResults(top20PageRank_1, "(a) Top 20 Normal PageRank 10 iterations", ["Id", "Value"], lambda x: str(x["pos"]) + "-" + str("%.7e"%float(x["value"])))
printListResults(bottom20PageRank_1, "(a) Bottom 20 Normal PageRank 10 iterations", ["Id", "Value"], lambda x: str(x["pos"]) + "-" + str("%.7e"%float(x["value"])))

plotHistogram("exercise_a_10", d_1, min(bottom20PageRank_1, key=lambda x: x["value"])["value"], max(top20PageRank_1, key=lambda x: x["value"])["value"], 60)

print("MSE Normal PageRank 10 iterations", MSE_1)
# Improved PageRank 10 iterations with a = 0.2
d_2, MSE_2, actual_iterations_2 = pageRankImproved(M, 10, 0.2)
top20PageRank_2 = nMaxElements(d_2, 20)
bottom20PageRank_2 = nMinElements(d_2, 20)

printListResults(top20PageRank_2, "(b) Top 20 Improved PageRank 10 iterations with a = 0.2", ["Id", "Value"], lambda x: str(x["pos"]) + "-" + str("%.7e"%float(x["value"])))
printListResults(bottom20PageRank_2, "(b) Bottom 20 Improved PageRank 10 iterations with a = 0.2", ["Id", "Value"], lambda x: str(x["pos"]) + "-" + str("%.7e"%float(x["value"])))

plotHistogram("exercise_b_10_0_2", d_2, min(bottom20PageRank_2, key=lambda x: x["value"])["value"], max(top20PageRank_2, key=lambda x: x["value"])["value"], 60)

print("MSE Improved PageRank 10 iterations with a = 0.2", MSE_2)
# Improved PageRank 10 iterations with a = 0.85
d_3, MSE_3, actual_iterations_3 = pageRankImproved(M, 10, 0.85)
top20PageRank_3 = nMaxElements(d_3, 20)
bottom20PageRank_3 = nMinElements(d_3, 20)

printListResults(top20PageRank_3, "(b) Top 20 Improved PageRank 10 iterations with a = 0.85", ["Id", "Value"], lambda x: str(x["pos"]) + "-" + str("%.7e"%float(x["value"])))
printListResults(bottom20PageRank_3, "(b) Bottom 20 Improved PageRank 10 iterations with a = 0.85", ["Id", "Value"], lambda x: str(x["pos"]) + "-" + str("%.7e"%float(x["value"])))

plotHistogram("exercise_b_10_0_85", d_3, min(bottom20PageRank_3, key=lambda x: x["value"])["value"], max(top20PageRank_3, key=lambda x: x["value"])["value"], 60)

print("MSE Improved PageRank 10 iterations with a = 0.85", MSE_3)

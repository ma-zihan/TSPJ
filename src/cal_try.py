import numpy as np
def calculate_completion_time_TSPJ(sequence, job_sequence, T, TT):
    '''
    sequnce: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    job_sequence: [0,5,3,4,1,2], only from the depot, len(job_sequence)=n
    T: T[0][i]==0 and T[i][0]==0, len(T)=n
    TT: TT[i][i]==0 and TT[i][j]==TT[j][i], len(TT)=n
    return C: from the depot to the depot, len(C)=n+1
    '''
    
    C = [0] * len(sequence)
    current_time = 0

    for i in range(1, len(sequence)-1):
        current_node = sequence[i]

        previous_node = sequence[i-1]
        travel_time = TT[previous_node][current_node]
        current_time += travel_time

        job_time = T[current_node][job_sequence[current_node]]
        C[current_node] = current_time + job_time

    travel_time_back_to_start = TT[sequence[-2]][sequence[-1]]
    # print(travel_time_back_to_start)
    current_time += travel_time_back_to_start
    C[-1] = current_time

    return C
def calculate_completion_time_TSP(sequence, TT):
    '''
    sequnce: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    TT: TT[i][i]==0 and TT[i][j]==TT[j][i], len(TT)=n
    return C: from the depot to the depot, len(C)=n+1
    '''
    
    C = [0] * len(sequence)
    current_time = 0

    for i in range(1, len(sequence)-1):
        current_node = sequence[i]

        previous_node = sequence[i-1]
        travel_time = TT[previous_node][current_node]
        current_time += travel_time

        C[current_node] = current_time

    travel_time_back_to_start = TT[sequence[-2]][sequence[-1]]
    # print(travel_time_back_to_start)
    current_time += travel_time_back_to_start
    C[-1] = current_time

    return C


def calculate_Cmax(sequence, job_sequence, T, TT):
    '''
    sequence: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    job_sequence: [0,5,3,4,1,2], only from the depot, len(job_sequence)=n
    T: T[0][i]==0 and T[i][0]==0, len(T)=n
    TT: TT[i][i]==0 and TT[i][j]==TT[j][i], len(TT)=n
    return: C, C_max, i_star, k_star
    '''
    C = calculate_completion_time_TSPJ(sequence, job_sequence, T, TT)
    C_max = max(C[:-1])  # 去掉最后返回仓库的时间，只考虑节点的最大完成时间
    i_star = C.index(C_max)
    k_star = job_sequence[i_star]
    return C, C_max, i_star, k_star



TT = np.array([
    [0, 5, 9, 12, 10, 6],
    [5, 0, 7, 9, 12, 10],
    [9, 7, 0, 5, 10, 12],
    [12, 9, 5, 0, 6, 10],
    [10, 12, 10, 6, 0, 7],
    [6, 10, 12, 10, 7, 0]
])


T = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 20, 22, 32, 25, 33],
    [0, 21, 20, 34, 23, 32],
    [0, 20, 22, 30, 22, 34],
    [0, 22, 24, 31, 22, 32],
    [0, 21, 20, 32, 24, 34]
])


seq = [0, 3, 4, 5, 2, 1, 0]
seq_j = [0,3,5,4,1,2]

C, C_max, i_star, k_star = calculate_Cmax(seq, seq_j, T, TT)
print(calculate_completion_time_TSP(seq, TT)) # [0, 76, 69, 34, 40, 45, 49]
print(C) # [0, 76, 69, 34, 40, 45, 49]
print(C_max) # 76
print(i_star) # 1
print(k_star) # 3
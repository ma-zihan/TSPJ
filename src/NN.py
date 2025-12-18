'''
Nearest Neighbor Heuristic for TSPJ and TSP
'''
from src.cal_time import calculate_completion_time_TSPJ, calculate_completion_time_TSP

def tspj_nn(TT, T):
    best_sequence = [] # length = n+1
    best_job_sequence = [] # length = n
    C_max = float('inf')

    for S in range(1, len(TT)):  
        node_pool = list(range(1, len(TT)))  
        sequence = [0, S]
        node_pool.remove(S)

        while node_pool:
            last_node = sequence[-1]
            next_node = min(node_pool, key=lambda x: TT[last_node][x])
            sequence.append(next_node)
            node_pool.remove(next_node)
        
        sequence.append(0)  
        # print(sequence)

        job_sequence = [0] * len(TT) # length = n
        job_pool = list(range(1, len(job_sequence)))  
        for i in range(len(job_sequence) - 1, 0, -1):  
            current_node = sequence[i]
            next_job = min(job_pool, key=lambda x: T[current_node][x])
            job_sequence[current_node] = next_job
            job_pool.remove(next_job)

        # print(job_sequence)
        C_new_sequence = calculate_completion_time_TSPJ(sequence, job_sequence, T, TT)
        # print(C_new_sequence)

        if max(C_new_sequence) < C_max:
            C_max = max(C_new_sequence)
            best_sequence = sequence[:]
            best_job_sequence = job_sequence[:]

    return best_sequence, best_job_sequence, C_max

def tspj_nn_far(TT, T):
    best_sequence = [] # length = n+1
    best_job_sequence = [] # length = n
    C_max = float('inf')

    for S in range(1, len(TT)):  
        node_pool = list(range(1, len(TT))) 

        far_node = max(node_pool, key=lambda x: TT[0][x]) 
        node_pool.remove(far_node)

        sequence = [0]
        if S != far_node:
            sequence.append(S)
            node_pool.remove(S)

        while node_pool:
            last_node = sequence[-1]
            next_node = min(node_pool, key=lambda x: TT[last_node][x])
            sequence.append(next_node)
            node_pool.remove(next_node)
        
        sequence.append(far_node)
        sequence.append(0)  
        print(sequence)

        job_sequence = [0] * len(TT) # length = n
        job_pool = list(range(1, len(job_sequence)))  
        for i in range(len(job_sequence) - 1, 0, -1):  
            current_node = sequence[i]
            next_job = min(job_pool, key=lambda x: T[current_node][x])
            job_sequence[current_node] = next_job
            job_pool.remove(next_job)

        # print(job_sequence)
        C_new_sequence = calculate_completion_time_TSPJ(sequence, job_sequence, T, TT)
        # print(C_new_sequence)

        if max(C_new_sequence) < C_max:
            C_max = max(C_new_sequence)
            best_sequence = sequence[:]
            best_job_sequence = job_sequence[:]

    return best_sequence, best_job_sequence, C_max

def tsp_nn(TT):
    best_sequence = [] # length = n+1
    C_max = float('inf')

    for S in range(1, len(TT)):  
        node_pool = list(range(1, len(TT)))  
        sequence = [0, S]
        node_pool.remove(S)

        while node_pool:
            last_node = sequence[-1]
            next_node = min(node_pool, key=lambda x: TT[last_node][x])
            sequence.append(next_node)
            node_pool.remove(next_node)
        
        sequence.append(0)  
        # print(sequence)

        C_new_sequence = calculate_completion_time_TSP(sequence, TT)
        # print(C_new_sequence)

        if max(C_new_sequence) < C_max:
            C_max = max(C_new_sequence)
            best_sequence = sequence[:]

    return best_sequence, C_max


# TT = np.array([
#     [0, 5, 9, 12, 10, 6],
#     [5, 0, 7, 9, 12, 10],
#     [9, 7, 0, 5, 10, 12],
#     [12, 9, 5, 0, 6, 10],
#     [10, 12, 10, 6, 0, 7],
#     [6, 10, 12, 10, 7, 0]
# ])

# T = np.array([
#     [0, 0, 0, 0, 0, 0],
#     [0, 20, 22, 32, 25, 33],
#     [0, 21, 20, 34, 23, 32],
#     [0, 20, 22, 30, 22, 34],
#     [0, 22, 24, 31, 22, 32],
#     [0, 21, 20, 32, 24, 34]
# ])

# best_sequence, best_job_sequence, C_max = tspj_nn(TT, T)
# print("best_sequence:", best_sequence)
# print("best_job_sequence:", best_job_sequence)
# print("C_max:", C_max)

# best_sequence, best_job_sequence, C_max = tspj_nn_far(TT, T)
# print("best_sequence:", best_sequence)
# print("best_job_sequence:", best_job_sequence)
# print("C_max:", C_max)


# best_sequence, C_max = tsp_nn(TT)
# print("best_sequence:", best_sequence)
# print("C_max:", C_max)

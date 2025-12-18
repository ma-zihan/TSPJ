'''
2-opt algorithm for TSP and TSPJ
'''
# from cal_time import calculate_completion_time_TSPJ, calculate_completion_time_TSP
from src.cal_time import calculate_completion_time_TSPJ, calculate_completion_time_TSP

def swap_nodes(seq, i, j):
    new_seq = seq[:]
    new_seq[i:j+1] = new_seq[i:j+1][::-1]
    return new_seq

def tspj_two_opt(sequence, job_sequence, TT, T):
    '''
    sequnce: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    job_sequence: [0,5,3,4,1,2], only from the depot, len(job_sequence)=n
    T: T[0][i]==0 and T[i][0]==0, len(T)=n
    TT: TT[i][i]==0 and TT[i][j]==TT[j][i], len(TT)=n
    '''

    best_sequence = sequence[:]
    best_job_sequence = job_sequence[:]
    C_sequence = calculate_completion_time_TSPJ(best_sequence, best_job_sequence, T, TT)

    improvement = True
    while improvement:
        improvement = False
        for i in range(1, len(TT)-1):
            for j in range(i + 1, len(TT)):
                new_sequence = swap_nodes(best_sequence, i, j)
                # print(new_sequence)
                C_new_sequence = calculate_completion_time_TSPJ(new_sequence, best_job_sequence, T, TT)
  
                if max(C_new_sequence) < max(C_sequence):
                    C_sequence = C_new_sequence[:]
                    best_sequence = new_sequence[:]
                    # print(best_sequence)

                    new_job_sequence = [0] * len(TT) # length = n
                    job_pool = list(range(1, len(new_job_sequence)))  
                    for k in range(len(new_job_sequence) - 1, 0, -1):  
                        current_node = new_sequence[k]
                        next_job = min(job_pool, key=lambda x: T[current_node][x])
                        new_job_sequence[current_node] = next_job
                        job_pool.remove(next_job)

                    best_job_sequence = new_job_sequence[:]
                    improvement = True
                    break
            if improvement:
                break
    final_C_sequence = calculate_completion_time_TSPJ(best_sequence, best_job_sequence, T, TT)
    C_max = max(final_C_sequence)
    return best_sequence, best_job_sequence, C_max

def tsp_two_opt(sequence, TT):
    '''
    sequnce: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    TT: TT[i][i]==0 and TT[i][j]==TT[j][i], len(TT)=n
    '''

    best_sequence = sequence[:]
    C_sequence = calculate_completion_time_TSP(best_sequence, TT)

    improvement = True
    while improvement:
        improvement = False
        for i in range(1, len(TT)-1):
            for j in range(i + 1, len(TT)):
                new_sequence = swap_nodes(best_sequence, i, j)
                # print(new_sequence)
                C_new_sequence = calculate_completion_time_TSP(new_sequence, TT)
  
                if max(C_new_sequence) < max(C_sequence):
                    C_sequence = C_new_sequence[:]
                    best_sequence = new_sequence[:]
                    # print(best_sequence)

                    improvement = True
                    break
            if improvement:
                break
    final_C_sequence = calculate_completion_time_TSP(best_sequence, TT)
    C_max = max(final_C_sequence)
    return best_sequence, C_max

# TT = np.array([
#     [0, 5, 9, 12, 10, 6],
#     [5, 0, 7, 9, 12, 10],
#     [9, 7, 0, 5, 10, 12],
#     [12, 9, 5, 0, 6, 10],
#     [10, 12, 10, 6, 0, 7],
#     [6, 10, 12, 10, 7, 0]
# ])

# # # T = np.array([
# # #     [0, 0, 0, 0, 0, 0],
# # #     [0, 20, 22, 32, 25, 33],
# # #     [0, 21, 20, 34, 23, 32],
# # #     [0, 20, 22, 30, 22, 34],
# # #     [0, 22, 24, 31, 22, 32],
# # #     [0, 21, 20, 32, 24, 34]
# # # ])


# seq = [0,5,3,4,1,2,0]
# # # seq_j = [0,2,4,3,5,1]
# # # best_sequence, best_job_sequence, C_sequence = tspj_two_opt(seq, seq_j, TT, T)
# # # print(best_sequence)
# # # print(best_job_sequence)
# # # print(C_sequence)
# best_sequence, C_sequence = tsp_two_opt(seq, TT)
# print(best_sequence)
# print(C_sequence)
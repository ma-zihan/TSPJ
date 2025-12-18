'''
Local Search Improvement heuristic for TSPJ
Including 3 steps: Initiation, Forward Swaps and Backward Swaps
'''
import numpy as np
# from src.cal_time import calculate_completion_time_TSPJ, calculate_completion_time_TSP
from cal_time import calculate_completion_time_TSPJ, calculate_completion_time_TSP

def calculate_Cmax(sequence, job_sequence, T, TT):
    '''
    sequence: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    job_sequence: [0,5,3,4,1,2], only from the depot, len(job_sequence)=n
    T: T[0][i]==0 and T[i][0]==0, len(T)=n
    TT: TT[i][i]==0 and TT[i][j]==TT[j][i], len(TT)=n
    return: C, C_max, i_star, k_star
    '''
    C = calculate_completion_time_TSPJ(sequence, job_sequence, T, TT)
    C_max = max(C[:-1])  
    i_star = C.index(C_max)
    k_star = job_sequence[i_star]
    return C, C_max, i_star, k_star






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


# seq = [0, 1, 2, 3, 4, 5, 0]
# seq_j = [0,5,3,4,1,2]

# print(calculate_Cmax(seq, seq_j, T, TT))
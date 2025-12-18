import numpy as np

def calculate_completion_time_TSPJ(sequence, job_sequence, T, TT):
    '''
    sequence: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    job_sequence: [0,5,3,4,1,2], only from the depot, len(job_sequence)=n
    T: T[0][i]==0 and T[i][0]==0, len(T)=n
    TT: TT[i][i]==0 and TT[i][j]==TT[j][i], len(TT)=n
    return C: from the depot to the depot, len(C)=n+1
    '''
    C = [0] * len(sequence)
    current_time = 0

    for i in range(1, len(sequence) - 1):
        current_node = sequence[i]
        previous_node = sequence[i - 1]
        travel_time = TT[previous_node][current_node]
        current_time += travel_time

        job_time = T[current_node][job_sequence[current_node]]
        C[current_node] = current_time + job_time

    travel_time_back_to_start = TT[sequence[-2]][sequence[-1]]
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
    seq = [0, 3, 4, 5, 2, 1, 0]
    seq_j = [0,3,5,4,1,2]

    C, C_max, i_star, k_star = calculate_Cmax(seq, seq_j, T, TT)
    print(C) # [0, 76, 69, 34, 40, 45, 49]
    print(C_max) # 76
    print(i_star) # 1
    print(k_star) # 3
    '''
    C = calculate_completion_time_TSPJ(sequence, job_sequence, T, TT)
    C_max = max(C[:-1])  # 去掉最后返回仓库的时间，只考虑节点的最大完成时间
    i_star = C.index(C_max)
    k_star = job_sequence[i_star]
    return C, C_max, i_star, k_star

def swap_nodes(seq, i, j):
    new_seq = seq[:]
    new_seq[i:j+1] = new_seq[i:j+1][::-1]
    return new_seq

def LSI_algorithm(sequence, job_sequence, T, TT):
    def swap_jobs(job_sequence, i_star, k_new, k_star):
        job_sequence_temp = job_sequence[:]
        idx_new = job_sequence_temp.index(k_new)
        job_sequence_temp[i_star], job_sequence_temp[idx_new] = job_sequence_temp[idx_new], job_sequence_temp[i_star]
        return job_sequence_temp
    
    def assign_remaining_jobs(sequence, job_sequence, i_star, remaining_jobs, T):
        for idx in range(len(sequence) - 2, i_star, -1):
            if sequence[idx] != sequence[i_star]:
                min_job = min(remaining_jobs, key=lambda k: T[sequence[idx]][k])
                job_sequence[sequence[idx]] = min_job
                remaining_jobs.remove(min_job)
        return job_sequence

    improved = True
    while improved:
        improved = False
        C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
        # 初始化在 i_star 之后节点的任务列表
        unassigned_jobs = [job_sequence[sequence[i]] for i in range(i_star + 1, len(sequence) - 1)]
        print(unassigned_jobs)

        # Step I: Forward Swaps
        while True:
            # Step I.1
            valid_jobs = [(T[i_star][k], k) for k in range(1, len(job_sequence)) if job_sequence.index(k) > job_sequence.index(k_star)]
            print('valid_jobs:',valid_jobs)
            if valid_jobs is None:
                break
            min_t_ik, k_min = min(valid_jobs, key=lambda x: x[0])
            # print('min_t_ik:',min_t_ik)
            # min_t_ik = min([T[i_star][k] for k in range(1, len(job_sequence)) if job_sequence.index(k) > job_sequence.index(k_star)])
            # print('min_t_ik1:',min_t_ik)
            # min_t_ik = min([T[i_star][k] for k in unassigned_jobs])
            # print('min_t_ik2:',min_t_ik)
            if T[i_star][k_star] <= min_t_ik:
                break

            # Step I.2
            while T[i_star][k_star] > min_t_ik:
                k_new = k_min
                print('k_new1', k_new)
                # k_new = min([(T[i_star][k], k) for k in unassigned_jobs], key=lambda x: x[0])[1]
                # print('k_new2', k_new)
                job_sequence_temp = swap_jobs(job_sequence, i_star, k_new, k_star)
                _, new_C_max, _, _ = calculate_Cmax(sequence, job_sequence_temp, T, TT)

                valid_swap = True
                for i in range(1, len(sequence) - 1): # i 是1 2 3 4 5 6
                    if i != sequence.index(i_star):
                        TS_i = calculate_completion_time_TSP(sequence, TT)[i] 
                        # print(TS_i)
                        for k in range(1, len(job_sequence)):
                            if job_sequence_temp[sequence.index(i)] == k:
                                if TS_i + T[sequence.index(i)][k] >= C_max:
                                    valid_swap = False
                                    break

                # TS_i = calculate_completion_time_TSP(sequence, TT)[sequence.index(i)]                
                if new_C_max < C_max and valid_swap:
                    job_sequence = job_sequence_temp
                    C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
                    # 更新在 i_star 之后节点的任务列表
                    unassigned_jobs = [job_sequence[sequence[i]] for i in range(i_star + 1, len(sequence) - 1)]
                    improved = True
                else:
                    break

            if improved:
                break
    #         # Step I.3
    #         for k in range(1, len(job_sequence)):
    #             if sequence.index(k) > sequence.index(k_star):
    #                 sequence_temp = sequence[:]
    #                 idx_k = sequence.index(k)
    #                 sequence_temp[i_star], sequence_temp[idx_k] = sequence_temp[idx_k], sequence_temp[i_star]
    #                 _, new_C_max, _, _ = calculate_Cmax(sequence_temp, job_sequence, T, TT)
    #                 if new_C_max < C_max:
    #                     sequence = sequence_temp
    #                     C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
    #                     improved = True
    #                     break

    #         if improved:
    #             break

    #     # Step II: Backward Swaps
    #     while True:
    #         improvement = False

    #         # Step II.1: Predecessor Node Swaps
    #         for v in range(i_star - 1, 0, -1):
    #             u = v - 1
    #             w = i_star + 1
    #             if u >= 0 and w < len(sequence):
    #                 delta_i1 = TT[u][i_star] + TT[v][w] - TT[u][v] - TT[i_star][w]
    #                 if delta_i1 + C[i_star] < C_max and delta_i1 + C[i_star] + TT[i_star][0] < C_max:
    #                     sequence_temp = swap_nodes(sequence, v, i_star)
    #                     _, new_C_max, _, _ = calculate_Cmax(sequence_temp, job_sequence, T, TT)
    #                     if new_C_max < C_max:
    #                         sequence = sequence_temp
    #                         C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
    #                         improvement = True
    #                         break

    #         if improvement:
    #             continue

    #         # Step II.2: Multi-node Swaps
    #         for p in range(1, i_star):
    #             for r in range(p + 1, i_star):
    #                 if r >= 0 and r < len(sequence):
    #                     delta_ip = TT[u][i_star] + TT[v][w] - TT[u][v] - TT[i_star][w]
    #                     if delta_ip + C[i_star] < C_max and delta_ip + C[i_star] + TT[i_star][0] < C_max:
    #                         sequence_temp = sequence[:]
    #                         for i in range(v, i_star):
    #                             sequence_temp = swap_nodes(sequence_temp, i, i_star)
    #                         _, new_C_max, _, _ = calculate_Cmax(sequence_temp, job_sequence, T, TT)
    #                         if new_C_max < C_max:
    #                             sequence = sequence_temp
    #                             C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
    #                             improvement = True
    #                             break

    #         if not improvement:
    #             break

    return sequence, job_sequence, C_max

# 示例输入数据
sequence = [0, 1, 2, 3, 4, 5, 0]
job_sequence = [0, 3, 5, 4, 1, 2]
T = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 20, 22, 32, 25, 33],
    [0, 21, 20, 34, 23, 32],
    [0, 23, 36, 40, 39, 41],
    [0, 29, 30, 32, 31, 32],
    [0, 22, 13, 32, 14, 34]
])
TT = np.array([
    [0, 5, 9, 12, 10, 6],
    [5, 0, 7, 9, 12, 10],
    [9, 7, 0, 5, 10, 12],
    [12, 9, 5, 0, 6, 10],
    [10, 12, 10, 6, 0, 7],
    [6, 10, 12, 10, 7, 0]
])

# 调用 LSI 算法
best_sequence, best_job_sequence, C_max = LSI_algorithm(sequence, job_sequence, T, TT)
print("Best Sequence:", best_sequence)
print("Best Job Sequence:", best_job_sequence)
print("Completion Times:", C_max)

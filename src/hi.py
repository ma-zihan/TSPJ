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
    C_max = max(C[:-1])  
    i_star = C.index(C_max)
    k_star = job_sequence[i_star]
    return C, C_max, i_star, k_star

def swap_jobs(job_seq, i_star, k):
    new_seq = job_seq[:]
    index_k = job_seq.index(k)
    new_seq[index_k], new_seq[i_star] = job_seq[i_star], job_seq[index_k]
    return new_seq

def swap_resign_jobs(job_seq, i_star, k_min, seq, T):
    # unsigned_jobs = job_seq[i_star:]
    i_star_job = job_seq[i_star]
    unsigned_nodes = seq[seq.index(i_star)+1:-1]
    unsigned_jobs = [job_seq[i] for i in unsigned_nodes]
    unsigned_jobs.append(i_star_job)
    temp_job_seq = job_seq [:]
    temp_job_seq[i_star] = k_min
    # print('k_min',k_min)
    # print('unsigned_job:', unsigned_jobs)
    unsigned_jobs.remove(k_min)

    for node in reversed(unsigned_nodes):
        min_value = float('inf')
        min_job = None
        for job in unsigned_jobs:
            if T[node][job] < min_value:
                min_value = T[node][job]
                min_job = job
        temp_job_seq[node] = min_job
        # print(min_value)
        unsigned_jobs.remove(min_job)
    return temp_job_seq, unsigned_jobs, unsigned_nodes

def swap_nodes(seq, i_star, i_index):
    new_seq = seq[:]
    i_star_index = seq.index(i_star)
    new_seq[i_star_index], new_seq[i_index] = i_index, i_star
    return new_seq

def delta(i_index, i_star_index, TT):
    a = TT[i_index][i_star_index]
    c = TT[i_index+1][i_star_index+1]
    d = TT[i_index][i_index+1]
    f = TT[i_star_index][i_star_index+1]
    return a+c-d-f
    
def LSI_algorithm(sequence, job_sequence, T, TT):

    C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
    # print(i_star,k_star)
    improved = True
    while improved:
        improved = False
        
        # Step I: Forward Swaps
        while True:
            # Step I.1
           
            unsigned_nodes = sequence[sequence.index(i_star)+1:-1]
            unsigned_jobs = [job_sequence[i] for i in unsigned_nodes]
            valid_jobs = [(T[i_star][k], k) for k in unsigned_jobs]
            # print(i_star,k_star,sequence[sequence.index(i_star):],T[i_star][k_star])
            # print(valid_jobs)
            if not valid_jobs:
                #print('hi')
                break
            # print('valid_jobs:',valid_jobs)
            min_t_ik, k_min = min(valid_jobs, key=lambda x: x[0])
            if T[i_star][k_star] <= min_t_ik:
                # print('hi')
                break

            temp_job_seq, _, _ = swap_resign_jobs(job_sequence, i_star, k_min, sequence, T)
            # _, new_C_max, _, _ = calculate_Cmax(sequence, temp_job_seq, T, TT)

            # print(T[i_star][k_star] > min_t_ik)
            # Step I.2
            while T[i_star][k_star] > min_t_ik:
                # print('la')
                valid_swap = True
                for i in range(1, len(sequence) - 1): 
                    if i == i_star: continue
                    else:
                        TS_i = calculate_completion_time_TSP(sequence, TT)[i] 
                        T_i = T[i][temp_job_seq[i]]
                        # print(T_i)
                        # print('C_max', C_max)
                        if TS_i + T_i >= C_max:
                            # print(TS_i + T_i >= C_max)
                            valid_swap = False
                            break
                # print(valid_swap)            
                if valid_swap:
                    # print('la')
                    job_sequence = temp_job_seq
                    C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
                    # print(C_max)
                    # k_star = k_min
                    improved = True
                    break
                else:
                    improved = False
                    # break
                    for job in unsigned_jobs: # unsigned_jobs = [job_sequence[i] for i in unsigned_nodes]
                        valid_swap2 = True
                        if T[i_star][job] >= T[i_star][k_star]:
                            valid_swap2 = False

                        TS_ii = calculate_completion_time_TSP(sequence, TT)[job_sequence.index(job)]
                        TS_ii_star = calculate_completion_time_TSP(sequence, TT)[i_star]
                        t_ii_k_star = T[job_sequence.index(job)][k_star]
                        t_i_star_k_star = T[i_star][k_star]

                        if TS_ii + t_ii_k_star >= TS_ii_star + t_i_star_k_star:
                            valid_swap2 = False

                        # print(valid_swap2)
                        if valid_swap2:
                            # job_sequence = new_job_seq
                            job_sequence = swap_jobs(job_sequence, i_star, job)
                            C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT)
                            # print(C_max)
                            improved = True
                            break
                        # else: improved = False

                    break
#             if not improved:
#                 break
#             print(sequence)
# # #       Step II:
# #         while True:
#             # print(i_star)

            i_star_index = sequence.index(i_star)

            f_nodes = sequence[1:sequence.index(i_star)]
            f_jobs = [job_sequence[i] for i in f_nodes]

            f_nodes_re = f_nodes[::-1]
            f_jobs_re = [job_sequence[i] for i in f_nodes_re]

            if not f_nodes:
                #print('hi')
                break
            if i_star_index < 3 or sequence.index(i_star) == len(sequence) - 2:
                break

            s_index = i_star_index - 1
            delta_s = delta(s_index, i_star_index, TT)

            for s in range(i_star_index - 2, 0, -1):
                mid_nodes = f_nodes[sequence.index(fea):]


            nodes_index = []
            i_star_index = sequence.index(i_star)
            for node in f_nodes:
                node_index = sequence.index(node)
                nodes_index.append(node_index)
            # print(nodes_index)
            deltas = []
            for index in nodes_index:
                delta_i = delta(index, i_star_index, TT)
                deltas.append(delta_i)
            # print(deltas)
            u_f_nodes = sequence[sequence.index(i_star)+1:-1]
            # print(u_f_nodes)
            # C_is = C[i_star:-1]

            # print(sequence)
            # print(i_star)

            for i in range(len(nodes_index)):
                
                valid_swap3 = True
                # 28
                for u_f_node in u_f_nodes:
                    if deltas[i] + C[u_f_node]>= C_max:
                        valid_swap3 = False
                        break
                
                # 29
                vi_nodes = sequence[ (i+1) : sequence.index(i_star)]
                for vi_node in vi_nodes:
                    if not vi_nodes:
                        if calculate_completion_time_TSP(vi_node, TT) + T[vi_node][job_sequence[vi_node]] >= C_max:
                            valid_swap3 = False
                            break

                # 30
                if deltas[i] + calculate_completion_time_TSP(sequence, TT)[-1] >= C_max:
                    valid_swap3 = False

                # print(valid_swap3)
                if valid_swap3:
                    sequence = swap_nodes(sequence, i_star, i+1)
                    C, C_max, i_star, k_star = calculate_Cmax(sequence, job_sequence, T, TT) 
                    improved = True
                    break

            if not improved:
                break    

    return sequence, job_sequence, C_max

# sequence = [0, 1, 2, 3, 4, 5, 0]
# job_sequence = [0, 3, 5, 4, 1, 2]
# T = np.array([
#     [0, 0, 0, 0, 0, 0],
#     [0, 20, 22, 32, 25, 33],
#     [0, 21, 20, 34, 23, 32],
#     [0, 23, 36, 40, 39, 41],
#     [0, 29, 30, 32, 31, 32],
#     [0, 22, 13, 32, 14, 34]
# ])
# TT = np.array([
#     [0, 5, 9, 12, 10, 6],
#     [5, 0, 7, 9, 12, 10],
#     [9, 7, 0, 5, 10, 12],
#     [12, 9, 5, 0, 6, 10],
#     [10, 12, 10, 6, 0, 7],
#     [6, 10, 12, 10, 7, 0]
# ])

# best_sequence, best_job_sequence, C_max = LSI_algorithm(sequence, job_sequence, T, TT)
# print("Best Sequence:", best_sequence)
# print("Best Job Sequence:", best_job_sequence)
# print("Completion Times:", C_max)




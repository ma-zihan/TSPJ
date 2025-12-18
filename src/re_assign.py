import numpy as np
'''
reverse_assignments algorithm
'''
def reverse_assignments(sequence, T):
    T = T.to_numpy()
    '''
    sequnce: [0,1,2,3,4,5,0], from the depot to the depot, len(sequence)=n+1
    T: T[0][i]==0 and T[i][0]==0, len(T)=n
    return job_sequence: [0,5,3,4,1,2], only from the depot, len(job_sequence)=n
    '''
    T = T.astype(float)
    job_sequence = [0] * len(T) # length = n

    sequence_temp = sequence[1:-1]

    T[0, :] = np.inf
    T[:, 0] = np.inf

    while sequence_temp:
        current_node = sequence_temp[-1]
        job_times = T[current_node, :]

        min_job = np.argmin(job_times)
        job_sequence[current_node] = min_job

        T[:, min_job] = np.inf

        sequence_temp = sequence_temp[:-1]

    return job_sequence


# T = np.array([
#     [0, 0, 0, 0, 0, 0],
#     [0, 20, 22, 32, 25, 33],
#     [0, 21, 20, 34, 23, 32],
#     [0, 20, 22, 30, 22, 34],
#     [0, 22, 24, 31, 22, 32],
#     [0, 21, 20, 32, 24, 34]
# ])


# seq = [0, 1, 2, 3, 4, 5, 0]

# print(reverse_assignments(seq, T)) # [0, 5, 3, 4, 1, 2]
def swap_nodes(seq, i_star, i):
    new_seq = seq[:]
    i_star_index = seq.index(i_star)
    i_index = seq.index(i)
    new_seq[i_star_index], new_seq[i_index] = i, i_star
    return new_seq

seq = [0,2,4,6,3,1,5]
print(swap_nodes(seq,3,2))
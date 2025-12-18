import pandas as pd
import os
from src.NN import tspj_nn, tsp_nn, tspj_nn_far
from src.two_opt import tspj_two_opt,tsp_two_opt
from src.re_assign import reverse_assignments
from src.hi import *
import time

def read_and_check_csv(tt_path, jt_path):
    results = {'tt_valid': False, 'jt_valid': False, 'tt': None, 'jt': None}

    try:
        jt = pd.read_csv(jt_path, header=None, index_col=False, sep='\s+')
        # jt = pd.read_csv(jt_path, header=None, index_col=False)
        if jt.shape[0] == jt.shape[1] and (jt.iloc[0, :] == 0).all() and (jt.iloc[:, 0] == 0).all():
            results['jt_valid'] = True
            results['jt'] = jt
    except Exception as e:
        print(f"Error reading or validating {jt_path}: {e}")

    try:
        tt = pd.read_csv(tt_path, header=None, index_col=False, sep='\s+')
        # tt = pd.read_csv(tt_path, header=None, index_col=False)
        if tt.shape[0] == tt.shape[1] and all(tt.iloc[i, i] == 0 for i in range(tt.shape[0])):
            results['tt_valid'] = True
            results['tt'] = tt
    except Exception as e:
        print(f"Error reading or validating {tt_path}: {e}")

    return results

def main():
    directory = ['data/Test', 'data/TSPLIB-J', 'data/Small_problems']
    directory = directory[1]
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            jt_path = os.path.join(folder_path, 'JT.csv')
            tt_path = os.path.join(folder_path, 'TT.csv')
            
            results = read_and_check_csv(tt_path, jt_path)
            
            
            if results['tt_valid'] and results['jt_valid']:
                # tspj_nn(results['tt'], results['jt'])
                # print(f"Both files in {folder} are valid and now processing...")
                print(folder_path)
                f3(results['tt'], results['jt'])
                # f2(results['tt'], results['jt'])
                # f3(results['tt'], results['jt'])
                # f4(results['tt'], results['jt'])
            else:
               print(f"Validation failed for files in {folder}.")
                
def f1(tt, jt):
    start_time = time.time()
    best_sequence, best_job_sequence, C_max = tspj_nn(tt, jt)
    best_sequence, best_job_sequence, C_max = tspj_two_opt(best_sequence, best_job_sequence, tt, jt)
    # C = calculate_completion_time_TSPJ(best_sequence, best_job_sequence, jt, tt)
    # print(best_sequence.index(C.index(max(C))), len(best_sequence), len(best_job_sequence), len(tt),len(jt))
    # sequence, job_sequence, C_max = LSI_algorithm(best_sequence,best_job_sequence, jt, tt)
    end_time = time.time()  
    execution_time = end_time - start_time  

    print(f"C_max: {C_max}")
    print(f"Execution time: {execution_time} seconds")
    #print(f"C_max: {C_max}")

def f2(tt, jt):
    start_time = time.time()
    best_sequence, C_max = tsp_nn(tt)
    best_sequence, C_max = tsp_two_opt(best_sequence, tt)
    best_job_sequence = reverse_assignments(best_sequence, jt)
    # C = calculate_completion_time_TSPJ(best_sequence, best_job_sequence, jt, tt)
    # C_max = max(C)
    sequence, job_sequence, C_max = LSI_algorithm(best_sequence,best_job_sequence, jt, tt)
    end_time = time.time()  
    execution_time = end_time - start_time 
    print(f"C_max: {C_max}")
    print(f"Execution time: {execution_time} seconds")


def f3(tt, jt):
    start_time = time.time()
    best_sequence, best_job_sequence, C_max = tspj_nn(tt, jt)
    best_sequence, best_job_sequence, C_max = LSI_algorithm(best_sequence,best_job_sequence, jt, tt)
    best_sequence, best_job_sequence, C_max = tspj_two_opt(best_sequence, best_job_sequence, tt, jt)
    # C = calculate_completion_time_TSPJ(best_sequence, best_job_sequence, jt, tt)
    # print(best_sequence.index(C.index(max(C))), len(best_sequence), len(best_job_sequence), len(tt),len(jt))
    # sequence, job_sequence, C_max = LSI_algorithm(best_sequence,best_job_sequence, jt, tt)
    end_time = time.time()  
    execution_time = end_time - start_time  

    print(f"C_max: {C_max}")
    print(f"Execution time: {execution_time} seconds")



def f4(tt, jt):
    start_time = time.time()
    best_sequence, best_job_sequence, C_max = tspj_nn_far(tt, jt)
    best_sequence, best_job_sequence, C_max = LSI_algorithm(best_sequence,best_job_sequence, jt, tt)
    best_sequence, best_job_sequence, C_max = tspj_two_opt(best_sequence, best_job_sequence, tt, jt)
    # C = calculate_completion_time_TSPJ(best_sequence, best_job_sequence, jt, tt)
    # print(best_sequence.index(C.index(max(C))), len(best_sequence), len(best_job_sequence), len(tt),len(jt))
    # sequence, job_sequence, C_max = LSI_algorithm(best_sequence,best_job_sequence, jt, tt)
    end_time = time.time()  
    execution_time = end_time - start_time  

    print(f"C_max: {C_max}")
    print(f"Execution time: {execution_time} seconds")

if __name__ == "__main__":
    main()

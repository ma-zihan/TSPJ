# Traveling Salesman Problem with Job-times (TSPJ)

KAIST IE801 Special Topics in Industrial Engineering II

This repository provides a Python implementation of the Traveling Salesman Problem with Job Times (TSPJ). The Implementation follows the model and heuristics proposed by Mosayebi et al. (2021), aiming to minimize the maximum job completion time ($C_{max}$).

## Problem Overview

In TSPJ: A traveler starts from a depot, visits each node exactly once, assigns one job to each node, and returns to the depot
- Once a job is assigned, it executes autonomously
- Job processing times depend on the assigned node
- The objective is to minimize the maximum completion time of all jobs, including the return time to the depot

## Implemented Heuristics

-   **TSPJ-NN**: Nearest Neighbor heuristic adapted for TSPJ
-   **TSPJ-2-OPT**: 2-opt improvement based on $C_{max}$
-   **Reverse Assignments**: Backward job assignment strategy
-   **Local Search Improvement (LSI)**: Core improvement heuristic involving job and node swaps

## Heuristic Procedures

Four heuristic procedures are implemented:

1.  **Procedure 1**: TSPJ-NN → TSPJ-2-OPT
2.  **Procedure 2**: NN → 2-OPT → Reverse Assignments → LSI
3.  **Procedure 3**: TSPJ-NN → LSI → TSPJ-2-OPT
4.  **Procedure 4**: Modified TSPJ-NN (greatest-distance start) → LSI →TSPJ-2-OPT

## Project Structure

``` text
data/
├── Small_problems/
└── TSPLIB-J/

src/
├── cal_time.py     # Compute maximum completion time (Cmax)
├── NN.py           # TSPJ-NN heuristic
├── two_opt.py      # TSPJ-2-OPT heuristic
├── re_assign.py    # Reverse Assignments
├── LSI.py          # Local Search Improvement
└── main.py         # Load data and run procedures
```

## Datasets

-   **TSPLIB-J**: TSPJ instances derived from TSPLIB
-   **Small Problems**: Randomly generated small-scale instances

Each instance includes: - Travel time matrix (CSV) - Job processing time matrix (CSV)

## Usage

``` bash
python src/main.py
```

The procedure to run can be selected and configured inside `main.py`.

## Experimental Notes

Experiments were conducted on TSPLIB-J instances to evaluate solution quality and computational performance. Results were compared with the GAMS solutions reported in the original paper.

However, the performance gap for **Procedure 2** is notably larger than that reported in the paper. I suspect this discrepancy is due to errors in my implementation of Procedure 2. 

## Citation

Original Paper

``` bibtex
@article{Mosayebi2021TSPJ,
  title   = {The Traveling Salesman Problem with Job-times (TSPJ)},
  author  = {Mosayebi, Mohsen and Sodhi, Manbir and Wettergren, Thomas A.},
  journal = {Computers \& Operations Research},
  volume  = {129},
  pages   = {105226},
  year    = {2021},
  doi     = {10.1016/j.cor.2021.105226}
}
```

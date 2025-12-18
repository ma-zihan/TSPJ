import os
import pandas as pd
import numpy as np

# 定义基本目录
base_dir = "/Users/zihanma/Library/Mobile Documents/com~apple~CloudDocs/Project/data/Small_problems"

# 获取所有子文件夹
sub_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

# 遍历每个子文件夹
for sub_dir in sub_dirs:
    tt_path = os.path.join(base_dir, sub_dir, "TT.csv")
    jt_path = os.path.join(base_dir, sub_dir, "JT.csv")
    
    # 处理TT.csv文件
    if os.path.exists(tt_path):
        tt_df = pd.read_csv(tt_path, header=None)
        np.fill_diagonal(tt_df.values, 0)
        tt_df.to_csv(tt_path, header=False, index=False)
    
    # 处理JT.csv文件
    if os.path.exists(jt_path):
        jt_df = pd.read_csv(jt_path, header=None)
        jt_df.iloc[:, 0] = 0
        jt_df.to_csv(jt_path, header=False, index=False)

print("操作完成")

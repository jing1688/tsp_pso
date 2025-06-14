import pandas as pd
import numpy as np
from utils import tour_length          # ← 跟主程式同一支長度函式
# def load_distance(csv_path):
#     data = pd.read_csv(csv_path, header=None).values
#     return data[:,0], data[:,1]

# def build_D(csv_path):
#     xs, ys = load_distance(csv_path)
#     m = len(xs)
#     D = np.zeros((m, m))
#     for i in range(m):
#         for j in range(m):
#             D[i,j] = np.hypot(xs[i]-xs[j], ys[i]-ys[j])
#     return D



# D = build_D("C:/Users/eric3/OneDrive/桌面/tsp_pso/data/xy48.csv")
# localsearch.py

def _or_once(route, k, D):
    n   = len(route)
    # 一開始也把 route 轉成整數 numpy array
    route = np.array(route, dtype=int)
    base  = tour_length(route, D)
    best_gain = 0.0
    best      = None

    for i in range(n - k + 1):
        seg  = route[i : i+k]
        rest = np.concatenate((route[:i], route[i+k:]))
        for j in range(len(rest) + 1):
            cand = np.concatenate((rest[:j], seg, rest[j:]))
            # 確保 cand 是整數
            cand = cand.astype(int)
            gain = base - tour_length(cand, D)
            if gain > best_gain:
                best_gain, best = gain, cand.copy()

    if best is not None:
        return best.tolist(), best_gain
    else:
        # 返回的 route 也最好是 list
        return route.tolist(), 0.0

def local_search_full(route, D):
    # 不要傳 numpy.float64 進來，保證都是純整數 list
    cur = list(map(int, route))
    while True:
        for k in (1, 2, 3):
            nxt, gain = _or_once(cur, k, D)
            if gain > 0:
                cur = nxt   # 已經是 list[int]
                break
        else:
            return cur
# print("localsearch.py",local_search_full( [15, 21, 2, 33, 40, 28, 1, 41, 25, 3, 34, 44, 9, 23, 4, 47, 38, 31, 20, 46, 12, 24, 13, 22, 10, 11, 39, 14, 45, 32, 19, 29, 42, 16, 26, 18, 36, 5, 27, 35, 6, 17, 43, 30, 37, 8, 7],D))
def depot_insert_best(route, D):
    """在 route 中嘗試把『任一城市』放到頭或尾，回傳最短路徑。
       route 只含 1…N-1；D 是距離矩陣；O(n²)。
    """
    best_route = route                  # 目前最佳
    best_len   = tour_length(route, D)  # 目前成本
    n = len(route)

    for idx in range(n):
        city = route[idx]

        # 拿掉 city 之後的剩餘路徑
        rem = route[:idx] + route[idx+1:]

        # (1) city 插到最前面
        r1   = [city] + rem
        len1 = tour_length(r1, D)
        if len1 < best_len:
            best_route, best_len = r1, len1

        # (2) city 插到最後面
        r2   = rem + [city]
        len2 = tour_length(r2, D)
        if len2 < best_len:
            best_route, best_len = r2, len2

    return best_route

# 347. Top K Frequent Elements
# https://leetcode.com/problems/top-k-frequent-elements/
# 難度：Medium
#
# 給一個整數陣列 nums 和整數 k，回傳出現頻率前 k 高的元素。
# 答案順序不限。
#
# Example:
#   Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
#   Output: [1, 2]   (1 出現 3 次、2 出現 2 次，前 2 高)
#
#   Input:  nums = [1], k = 1
#   Output: [1]
#
# 進階要求：能不能做到比 O(n log n) 更好？（也就是「不要用排序」）


from typing import List


# 辨識：「頻率 / 出現幾次」→ hash 計數；「前 k 高」→ 取 top k
#
# 解法一：計數 + 排序取前 k
#   時間：O(n log n)  ← 排序
#   空間：O(n)
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    count = {}
    for num in nums:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1
    
    res = sorted(count.keys(), key=lambda x: count[x], reverse=True)
    return res[:k]

# 解法二：Bucket Sort（最佳）
#   洞察：出現次數最多 = len(nums)，範圍有上限 → 拿「次數」當 index 建桶
#   時間：O(n)  ← 不排序，建桶 + 掃桶都是線性
#   空間：O(n)
def top_k_frequent_bucket(nums: List[int], k: int) -> List[int]:
    count = {}
    for num in nums:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1
    answer = [[] for _ in range(len(nums) + 1)]
    for key in count:
        answer[count[key]].append(key)

    res = []
    for i in range(len(answer) - 1, 0, -1):   # 從最後一桶往前掃到 index 1
        for num in answer[i]:                  # 這桶裡的每個數字
            res.append(num)
            if len(res) == k:                  # 湊滿 k 個就回傳
                return res

# 測試
if __name__ == "__main__":
    print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))   # [1, 2]
    print(top_k_frequent([1], 1))                   # [1]
    print(top_k_frequent([1, 2], 2))                # [1, 2]

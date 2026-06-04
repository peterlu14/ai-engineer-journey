# 167. Two Sum II - Input Array Is Sorted
# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
# 難度：Medium
#
# 給一個「已經由小到大排序」的陣列 numbers，和一個目標值 target。
# 找出兩個數字相加 = target，回傳它們的「位置」（注意：1-indexed，從 1 開始算）。
#
# 假設一定有唯一解，且不能用同一個元素兩次。
#
# Example:
#   Input:  numbers = [2, 7, 11, 15], target = 9
#   Output: [1, 2]   （numbers[0] + numbers[1] = 2 + 7 = 9，位置是 1 和 2）
#
#   Input:  numbers = [2, 3, 4], target = 6
#   Output: [1, 3]   （2 + 4 = 6）
#
# 辨識：「已排序的陣列」+「找兩數配對」→ Two Pointers（左右夾，靠 sum 大小決定移哪邊）
#
# 提示：陣列已排序是關鍵！
#   sum 太大 → 右指標左移（換小一點的數）
#   sum 太小 → 左指標右移（換大一點的數）
#   sum 剛好 → 找到了


from typing import List


def two_sum(numbers: List[int], target: int) -> List[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        sum = numbers[left] + numbers[right]
        if sum > target:
            right -= 1
        elif sum < target:
            left += 1
        else:
            return [left + 1, right + 1]


# 測試
if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))   # [1, 2]
    print(two_sum([2, 3, 4], 6))         # [1, 3]
    print(two_sum([-1, 0], -1))          # [1, 2]

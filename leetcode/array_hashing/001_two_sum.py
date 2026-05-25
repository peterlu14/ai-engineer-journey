# 001. Two Sum
# https://leetcode.com/problems/two-sum/
# 難度：Easy
#
# 給一個整數陣列 nums 和目標值 target
# 找出兩個數字的 index，使它們相加等於 target
# 每個 input 只有一個答案，不能用同一個元素兩次
#
# Example:
#   Input:  nums = [2, 7, 11, 15], target = 9
#   Output: [0, 1]  (nums[0] + nums[1] = 2 + 7 = 9)

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    pass


# 測試
if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
    print(two_sum([3, 2, 4], 6))         # [1, 2]
    print(two_sum([3, 3], 6))            # [0, 1]

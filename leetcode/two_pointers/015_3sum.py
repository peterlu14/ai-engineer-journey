# 15. 3Sum
# https://leetcode.com/problems/3sum/
# 難度：Medium
#
# 給一個整數陣列 nums，找出所有「不重複」的三元組 [a, b, c]，
# 使得 a + b + c = 0。
#
# Example:
#   Input:  nums = [-1, 0, 1, 2, -1, -4]
#   Output: [[-1, -1, 2], [-1, 0, 1]]
#
#   Input:  nums = [0, 1, 1]
#   Output: []
#
#   Input:  nums = [0, 0, 0]
#   Output: [[0, 0, 0]]
#

from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    result = []
    sorted_nums = sorted(nums)
    for i, _ in enumerate(sorted_nums):
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue
        pinned_num = sorted_nums[i]
        left, right = i + 1, len(nums) - 1
        while left < right:
            current = [pinned_num, sorted_nums[left], sorted_nums[right]]
            current_sum = sum(current)
            if current_sum == 0:
                result.append(current)
                left += 1
                right -= 1
                while left < right and sorted_nums[left] == sorted_nums[left - 1]:
                    left += 1
                while left < right and sorted_nums[right] == sorted_nums[right + 1]:
                    right -= 1
            elif current_sum > 0:
                right -= 1
            else:
                left +=1
    return result

# 測試
if __name__ == "__main__":
    print(three_sum([-1, 0, 1, 2, -1, -4]))   # [[-1, -1, 2], [-1, 0, 1]]
    print(three_sum([0, 1, 1]))                # []
    print(three_sum([0, 0, 0]))                # [[0, 0, 0]]
    print(three_sum([-2, 0, 0, 2, 2]))         # [[-2, 0, 2]]

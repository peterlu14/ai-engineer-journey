# 11. Container With Most Water
# https://leetcode.com/problems/container-with-most-water/
# 難度：Medium
#
# 給一個陣列 height，每個值代表一根直立柱子的高度（x 軸位置就是 index）。
# 任選兩根柱子當容器的左右壁，能裝多少水 = 寬 × 高。
#   寬  = 兩根柱子的距離（right index - left index）
#   高  = 兩根柱子「較矮」的那根（水會從矮的那邊溢出）
# 求能裝的最大水量。
#
# Example:
#   Input:  height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
#   Output: 49
#   （選 index 1(高8) 和 index 8(高7)：寬 = 8-1 = 7，高 = min(8,7) = 7 → 7×7 = 49）
#
#   Input:  height = [1, 1]
#   Output: 1   （寬 1 × 高 1）
#
# 辨識：「左右兩端 + 求最大/最小」→ Two Pointers（左右往中間夾）
#
# 核心洞察（這題的關鍵）：
#   面積 = 寬 × min(左高, 右高)
#   從最寬（左右兩端）開始，每次移動「較矮」的那根——
#   因為瓶頸是矮的那根，移高的只會讓面積更小，移矮的才有機會變大。


from typing import List


def max_area(height: List[int]) -> int:
    max_water = 0
    left, right = 0, len(height) - 1

    while left < right:
        left_height = height[left]
        right_height = height[right]
        max_water = max(max_water, min(left_height, right_height) * (right - left))

        if left_height <= right_height:
            left += 1
        else:
            right -= 1

    return max_water

# 測試
if __name__ == "__main__":
    print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # 49
    print(max_area([1, 1]))                          # 1
    print(max_area([4, 3, 2, 1, 4]))                 # 16
    print(max_area([1, 2, 1]))                       # 2

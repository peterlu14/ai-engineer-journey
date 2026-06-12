# 125. Valid Palindrome
# https://leetcode.com/problems/valid-palindrome/
# 難度：Easy
#
# 給一個字串 s，判斷它是不是回文（palindrome）。
# 規則：只看「英數字元」，忽略大小寫、空格、標點。
#
# 回文 = 正著讀跟反著讀一樣，例如 "level"、"A man a plan a canal Panama"
#
# Example:
#   Input:  "A man, a plan, a canal: Panama"
#   Output: True   （清理後是 "amanaplanacanalpanama"，左右對稱）
#
#   Input:  "race a car"
#   Output: False  （"raceacar" 不對稱）
#
#   Input:  " "
#   Output: True   （清理後是空字串，視為回文）
#
# 辨識：「對稱 / 頭尾比對 / 正反一樣」→ Two Pointers（左右各一個指標往中間夾）


def is_palindrome(s: str) -> bool:
    new_str = ""
    for ch in s:
        if ch.isalnum():
            new_str += ch.lower()

    left = 0
    right = len(new_str) - 1
    while left < right:
        if new_str[left] == new_str[right]:
            left += 1
            right -= 1
        else:
            return False
    return True


# 測試
if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))   # True
    print(is_palindrome("race a car"))                        # False
    print(is_palindrome(" "))                                 # True
    print(is_palindrome("0P"))                                # False（'0' vs 'P'）

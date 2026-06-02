# 242. Valid Anagram
# https://leetcode.com/problems/valid-anagram/
# 難度：Easy
#
# 給兩個字串 s 和 t，判斷 t 是不是 s 的 anagram（重組字）。
# anagram = 用完全相同的字母、相同的數量，重新排列。
#
# Example:
#   Input:  s = "anagram", t = "nagaram"
#   Output: True
#
#   Input:  s = "rat", t = "car"
#   Output: False   (字母不一樣)
#
# 進階思考：如果字串包含 unicode 字元，你的解法還成立嗎？


def is_anagram(s: str, t: str) -> bool:
    d = {}
    if len(s) != len(t):
        return False

    for ch in s:
        if ch in d:
            d[ch] += 1
        else:
            d[ch] = 1

    for ch in t:
        if ch in d:
            d[ch] -= 1
        else:
            return False

    return True



# 測試
if __name__ == "__main__":
    print(is_anagram("anagram", "nagaram"))   # True
    print(is_anagram("rat", "car"))           # False
    print(is_anagram("a", "ab"))              # False（長度不同）
    print(is_anagram("", ""))                 # True

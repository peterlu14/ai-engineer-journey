# 3. Longest Substring Without Repeating Characters
# https://leetcode.com/problems/longest-substring-without-repeating-characters/
# 難度：Medium
#
# 給一個字串 s，找出「不含重複字元」的最長子字串的長度。
# （子字串 = 連續的一段；不是子序列）
#
# Example:
#   Input:  s = "abcabcbb"
#   Output: 3      （"abc"，長度 3）
#
#   Input:  s = "bbbbb"
#   Output: 1      （"b"）
#
#   Input:  s = "pwwkew"
#   Output: 3      （"wke"；注意 "pwke" 不是子字串，因為不連續）
#
#   Input:  s = ""
#   Output: 0
#
# 辨識：「連續子字串」+「最長」+「符合條件(不重複)」→ Sliding Window
#
# 心法（先想清楚再寫）：
#   - 維護一個窗口 [left, right]，裡面保證「字元都不重複」
#   - right 一步步往右擴，把新字元納進來
#   - 如果新字元造成重複 → left 往右縮，直到窗口又合法
#   - 每一步都更新答案 = max(答案, 窗口長度)
#
# 你要自己想的關鍵問題：
#   1. 用什麼資料結構記「窗口裡有哪些字元」？(查重要快)
#   2. 遇到重複時，left 該怎麼移？一次移一格？還是能直接跳？
#   3. 窗口長度怎麼算？(用 left/right 算，不要真的去切字串)


def length_of_longest_substring(s: str) -> int:
    left = 0
    max_num = 0
    repeat_char = set()

    for right in range(len(s)):
        while s[right] in repeat_char:
            repeat_char.remove(s[left])
            left += 1
        repeat_char.add(s[right])
        max_num = max(max_num, len(repeat_char))
    return max_num


# 複雜度心法（面試會追問）：
#   雖然是 for 包 while，但 left 單調遞增、永不回頭 → 總移動 O(n)，
#   right 也走 O(n)，兩指標加起來 O(2n) = O(n)，不是 O(n²)。
#   再用 set 讓「查重 in」從 O(n) 降到 O(1)，整體才真正 O(n)。
#   （list 版會退化成 O(n²)，因為每步的 in 是 O(n)。）
#   這種「雙指標單向不回頭」攤平巢狀迴圈成本的分析，叫攤還分析(amortized analysis)。


    

        



# 測試
if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))  # 3
    print(length_of_longest_substring("bbbbb"))     # 1
    print(length_of_longest_substring("pwwkew"))    # 3
    print(length_of_longest_substring(""))          # 0
    print(length_of_longest_substring("dvdf"))      # 3  ("vdf")

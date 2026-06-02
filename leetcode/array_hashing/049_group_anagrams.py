# 49. Group Anagrams
# https://leetcode.com/problems/group-anagrams/
# 難度：Medium
#
# 給一個字串陣列，把互為 anagram（重組字）的字串分到同一組。
# 回傳的組別順序、組內順序都不重要。
#
# Example:
#   Input:  ["eat", "tea", "tan", "ate", "nat", "bat"]
#   Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
#
#   "eat" "tea" "ate" 都是同樣的字母重組 → 一組
#   "tan" "nat" 一組
#   "bat" 自己一組
#
# 核心問題：怎麼讓「互為 anagram 的字串」產生同一個 key，
#           這樣就能用 dict 把它們收集到同一個 list？


from typing import List


# 複雜度（n = 字串數量，k = 最長字串長度）
#   時間：O(n · k log k)  ← n 個字串，每個都要 sorted（排序為 k log k）
#   空間：O(n · k)        ← dict 存下所有字串
#   進階：用「字母計數 tuple」當 key 可省掉排序，降到 O(n · k)
def group_anagrams(strs: List[str]) -> List[List[str]]:
    d = {}
    for s in strs:
        key = "".join(sorted(s))
        if key in d:
            d[key].append(s)
        else:
            d[key] = [s]
    return list(d.values())

# 測試
if __name__ == "__main__":
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [["eat","tea","ate"], ["tan","nat"], ["bat"]]（順序不限）

    print(group_anagrams([""]))      # [[""]]
    print(group_anagrams(["a"]))     # [["a"]]

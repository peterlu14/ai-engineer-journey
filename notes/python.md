# Python 重點筆記

做 Day 10 agent + LeetCode 時打通的觀念，整理在這。

---

## `*args` / `**kwargs` — 攤平 vs 收集

**同一個符號，寫在「定義」和「呼叫」意義相反。**

| 符號 | 對象 | 呼叫時（攤平/拆開） | 定義時（收集/打包） |
|------|------|----------------------|----------------------|
| `*`  | list / tuple（位置參數） | `f(*[1,2])` → `f(1,2)` | `def f(*args)` → args 是 tuple |
| `**` | dict（keyword 參數） | `f(**{"a":1})` → `f(a=1)` | `def f(**kwargs)` → kwargs 是 dict |

```python
# 呼叫時攤平：把 dict 拆成 keyword 參數
args = {"city": "台北"}
get_weather(**args)          # → get_weather(city="台北")

# 定義時收集：把傳進來的打包起來
def f(*args, **kwargs):
    print(args)              # (1, 2)
    print(kwargs)            # {"a": 3}
f(1, 2, a=3)

# 轉發參數（同時用到兩者）
def wrapper(*args):          # 收集
    return add(*args)        # 攤平
```

口訣：**def 裡的 `*` 把散的「收」起來；呼叫的 `*` 把整包「拆」開來。**

`args` / `kwargs` 只是慣例命名，決定行為的是「幾顆星 + 在哪裡用」。

---

## Dispatch Table（用 dict 存函式）

Python 函式是「值」，可以存進 dict、傳遞。用來取代一堆 if/else：

```python
TOOL_FUNCS = {
    "get_weather": get_weather,   # value 是函式本身（沒加括號 = 沒呼叫）
    "calculate": calculate,
}

result = TOOL_FUNCS[name](**args)   # 取出函式 + 攤平參數 → 一行通吃所有工具
```

加新工具只要往 dict 加一筆，loop 完全不用改。

---

## lambda（匿名函式）+ 為什麼 sorted 的 key 要傳函式

`lambda x: count[x]` 就是一個沒名字的小函式：

```python
key=lambda x: count[x]
# 等於
def f(x): return count[x]
key=f
```

**為什麼 `key` 要傳「函式」不是「值」？**
sorted 要排很多元素，每個都要算出排序依據。它需要的是一條「規則」：給我任何元素 x，告訴我怎麼算依據。所以傳函式（規則），sorted 對每個元素各呼叫一次。

```python
sorted(count.keys(),            # 要排的：每個 key（x 是逐一取出的單個元素）
       key=lambda x: count[x],  # 依據：用該 key 的次數
       reverse=True)            # 由大到小
```

> 傳值 = 一個答案（不夠，每個元素答案不同）
> 傳函式 = 算答案的規則（sorted 對每個元素套用）

JS 的 callback（`arr.sort((a,b)=>...)`、`map(fn)`）是同一回事。

---

## dict 操作 + falsy 陷阱

```python
d = {}
d["a"] = d.get("a", 0) + 1   # 不存在當 0，存在用現值（計數慣用法）
"a" in d                      # 檢查 key 在不在 → 精確
```

⚠️ **陷阱**：用 `if d.get(c):` 判斷 key 存不存在會出錯，因為值為 `0` 時是 falsy，會被當成「不存在」。
→ 要判斷 key 存在性，用 `if c in d:`，不要用 `if d.get(c):`。

---

## List Comprehension + `[[]]*n` 陷阱

```python
buckets = [[] for _ in range(n)]   # n 個「各自獨立」的空 list ✅
```

⚠️ **陷阱**：`[[]] * n` 會建出 n 個「指向同一個 list」的參考，改一個全部變：
```python
b = [[]] * 3
b[0].append(1)
print(b)            # [[1], [1], [1]] ← 三個都變了！
```
建獨立的空 list 一定用 `[[] for _ in range(n)]`。

（`_` = 「我不在乎這個迴圈變數」的慣例命名）

---

## range 的三參數 + 倒序

```python
range(起點, 終點, 步長)     # 終點「不包含」
range(6, 0, -1)            # 6,5,4,3,2,1（到 0 停，不含 0）
```

## index 換算：`+1` vs `-1`
- 建 n+1 個位置：`range(len(nums) + 1)`（次數最大到 n，index 0~n 要 n+1 個）
- 取最後一個 index：`len(arr) - 1`（長度 n，最後 index 是 n-1）

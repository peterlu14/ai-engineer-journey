# 程式語言比較

## Python vs TypeScript vs Rust

| | Python | TypeScript | Rust |
|--|--------|-----------|------|
| 速度 | 慢 | 中 | 快（接近 C） |
| 記憶體 | GC | GC | 所有權，無 GC |
| 學習曲線 | 低 | 中 | 高 |
| 適合 | AI / 腳本 / 快速開發 | 前端 / 全端 | 系統 / 效能敏感 |
| 型別 | 動態（可加 hint）| 靜態 | 靜態（很嚴格）|

## Rust 核心優勢

Python / JS 都有 GC（垃圾回收），會自動幫你清記憶體，但 GC 會暫停程式、佔資源。

Rust 用「所有權系統」在編譯時就確保記憶體安全，執行時零成本。結果：速度接近 C/C++，但不會有 C 的記憶體漏洞。

**AI 領域的 Rust：** PyTorch 底層、Hugging Face `tokenizers`、部分推理引擎都是 Rust 寫的。

## Python 加速方案

Python 慢是因為直譯器，但可以用以下方式提速：

| 工具 | 原理 | 適合 |
|------|------|------|
| **NumPy / PyTorch** | 熱路徑用 C/CUDA 寫，Python 只是介面 | 數值運算 / AI |
| **Numba** | JIT 編譯，加 `@jit` decorator 快 100 倍 | 複雜數值迴圈 |
| **Cython** | 把 Python 編譯成 C extension | 需要精細控制 |
| **CuPy** | NumPy 的 GPU 版本 | NVIDIA GPU 加速 |
| **JAX** | Google 出的，`@jit` 自動編譯成 XLA | GPU/TPU 訓練 |

```python
from numba import jit

@jit(nopython=True)
def heavy_loop(arr):
    total = 0.0
    for i in range(len(arr)):
        total += arr[i] ** 2
    return total
# 第一次呼叫編譯，之後快 100 倍
```

CPython（Python 預設直譯器）是用 C 寫的，所以直譯器本身很快，但你寫的 Python 程式碼還是跑在直譯器上。AI 訓練快是因為 PyTorch 的 CUDA kernel，不是 Python 本身快。

---

## Rust 基礎語法

### 變數
```rust
let x = 5;       // 預設不可變（像 TS 的 const）
let mut y = 5;   // 加 mut 才能改（像 TS 的 let）
y = 10;          // OK
```

### 型別對照

**數字**
| Rust | 說明 |
|------|------|
| `i32` | 整數，LeetCode 最常用 |
| `i64` | 大整數 |
| `usize` | 陣列 index 專用 |
| `f64` | 浮點數（Python `float`）|

**其他**
| Rust | 等於 |
|------|------|
| `bool` | bool |
| `&str` | 字串常數（不可變）|
| `String` | 字串物件（可變）|
| `Vec<i32>` | `list[int]` |
| `HashMap<K, V>` | `dict` |
| `Option<T>` | 可能是 None |

### 函式
```rust
fn add(a: i32, b: i32) -> i32 {
    a + b  // 最後一行不加分號 = return
}
```

### Vec
```rust
let mut nums = vec![1, 2, 3];
nums.push(4);

for n in &nums {
    println!("{}", n);
}
```

### HashMap
```rust
use std::collections::HashMap;

let mut map = HashMap::new();
map.insert("key", 1);

if let Some(&val) = map.get("key") {
    println!("{}", val);
}
```

### Option（Rust 沒有 null）
```rust
let x: Option<i32> = Some(5);
let y: Option<i32> = None;

if let Some(val) = x {
    println!("{}", val);  // 5
}
```
HashMap 的 `.get()` 回傳 `Option`，取值前要先判斷。

### match
```rust
match x {
    1 => println!("one"),
    2 | 3 => println!("two or three"),
    _ => println!("other"),  // default
}
```

---

## Rust 所有權（Ownership）與借用（Borrowing）

### 核心概念
每個值只有一個「擁有者」，編譯器在編譯時確保記憶體安全，不需要 GC。

### Move vs Borrow vs Clone

| 操作 | 語法 | 原本的變數 | 類比 |
|------|------|-----------|------|
| Move（移交所有權）| `let b = a` | 失效，不能用 | 無對應概念 |
| Borrow（借用）| `let b = &a` | 還能用 | call by reference |
| Clone（複製）| `let b = a.clone()` | 還能用 | deep copy |

```rust
// Move：所有權轉移，原本失效
let a = String::from("hello");
let b = a;
println!("{}", a);  // 編譯錯誤！a 已失效

// Borrow：借用，兩個都能用
let a = String::from("hello");
let b = &a;
println!("{}", a);  // OK
println!("{}", b);  // OK

// Clone：完整複製
let a = String::from("hello");
let b = a.clone();
println!("{}", a);  // OK
println!("{}", b);  // OK
```

### 例外：基本型別會複製不會 Move
`i32`, `f64`, `bool` 這類小型別直接複製，不會 move：
```rust
let x: i32 = 5;
let y = x;         // 複製，不是 move
println!("{}", x); // OK，x 還在
```

### 為什麼 HashMap API 要傳 `&key`
```rust
map.contains_key(&diff)  // 只借給它看，diff 還是你的
map.get(&diff)           // 同上
```
函式只需要「看」值，不需要拿走所有權，所以 API 設計成接受 `&`。
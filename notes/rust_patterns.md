# Rust 常見 Pattern

## Option

Rust 沒有 null，用 `Option` 代替：

```rust
Some(值)  // 有值
None      // 沒值
```

`HashMap.get()` 就回傳 Option：
```rust
map.get(&key)  // → Some(&value) 或 None
```

---

## if let

「定義變數 + if 判斷」合一，比對成功才進去：

```rust
if let Some(&j) = map.get(&diff) {
    // Some 才進來，j 就是裡面的值
    // None 直接跳過
}
```

拆開來理解等於：
```rust
let result = map.get(&diff);
if result != None {
    let j = *result.unwrap();
    // ...
}
```

`j` 是佔位符，名字隨便取，只是說「如果匹配成功，把裡面的值叫做 j」。

---

## if let 比對規則

比對的是**形狀（pattern）**，不是值：

```rust
Some(&j) = Some(5)  // 形狀符合，j = 5，進去
Some(&j) = None     // 形狀不符，跳過
```

---

## match（多條件）

```rust
match map.get(&key) {
    Some("hello") => println!("是 hello"),
    Some("world") => println!("是 world"),
    Some(other)   => println!("是 {}", other),
    None          => println!("沒有值"),
}
```

---

## Some 只是 Option 的 variant

`Some` 不是特殊語法，是 `Option` 這個 enum 的一種狀態：

```rust
enum Option<T> {
    Some(T),  // 有值
    None,     // 沒值
}
```

不同型別有不同的 variant，不一定用 `Some`：
```rust
if let Some(x) = option_value { }   // Option
if let Color::Red = color { }       // 自定義 enum
if let 5 = number { }               // 整數
```

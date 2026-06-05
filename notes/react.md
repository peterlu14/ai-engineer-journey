# React

## useState
管理元件內部狀態，state 改變會觸發重新渲染。
```ts
const [value, setValue] = useState<string>('')
```
- 不能直接修改 state（如 `.push()`），要用 setter 函式
- 更新 array 用展開運算子：`setValue(prev => [...prev, newItem])`

## State 更新與 re-render 的核心機制 ⭐

### 1. render = 整個函式從頭重跑一次
- 每次 render 都把元件函式完整執行一遍，產生**那一次專屬的區域變數**（像一張凍結的快照）。
- `const [messages] = useState()` 的 `messages`，在這次 render 裡是 **const，永遠不變**。
- 所以 `setMessages` 之後**下一行**讀 `messages`，還是舊值：
```ts
console.log(messages)   // []
setMessages([1, 2])     // 通知 React：存新值 + 排重畫（不改現在的 messages）
console.log(messages)   // 還是 [] ！新值要等下次 render 才出現
```

### 2. closure 陷阱：迴圈裡一定要用 `prev =>`
- `messages`（closure 變數）= render 當下的快照，整個 loop 不會變。
- `prev`（React 傳進來的參數）= React 倉庫裡的**最新值**，會拿到上一圈的結果。
- 凡是「**基於前一個 state 算下一個**」（累加 / append / 計數）→ 一定用 `setX(prev => ...)`：
```ts
// streaming 逐字累加，必須用 prev，否則每個 chunk 互相蓋掉只剩最後一個
setMessages(prev => {
  const last = prev[prev.length - 1]
  return [...prev.slice(0, -1), { ...last, content: last.content + chunk }]
})
```

### 3. const 鎖「綁定」，不鎖「內容」
- **reassign（重新賦值）**：改變數指向誰 → `arr = [...]` → const **擋**。
- **mutate（變動內容）**：不動指向，改它指向的物件內部 → `arr.push()`、`arr[0]=x`、`obj.name=y` → const **不擋**（JS 允許）。
- 原始型別（number/string）沒有「內部」可改 → 只能 reassign → const 後就**完全凍結**。

### 4. immutable（不可變寫法）
- 物件/陣列天生 **mutable**，但 React 要求我們**當成 immutable 對待**：不改舊的，要變化就 `[...]` / `{...}` **做一個新的**。
- 這是**自律**，不是語言強制。

### 5. 為什麼一定要 setter，不能自己 mutate
`setMessages` 做**兩件事**：① 把新值存進倉庫 ② 排一次 re-render。
- 自己 mutate 舊陣列 → 這兩件事一件都不會發生。
- 而且 React 排重畫後會用 **`Object.is` 比新舊 reference**：
  - reference 不同（新陣列）→ 真的變了 → 重畫 ✅
  - reference 相同（mutate 後傳同一個）→ 視為沒變 → **略過不重畫** ❌
- 所以「mutate 不會更新畫面」的真相 = reference 沒換，被 Object.is 篩掉。

### 6. 倉庫：state 存在哪
- 存在 **React 內部**，活在函式**外面**、**跨 render 持續存在**。
- **每個元件實例各自一份**（不是 global）。
- `useState` 每次 render **靠「呼叫順序」**去倉庫領對應的值。
- → 這就是 **Rules of Hooks** 的原因：hook 不能放在 if / for / 條件裡，否則呼叫順序改變，React 會配錯櫃子。

### 7. re-render 的範圍：自己 + 往下，不往上 / 不往旁
- 某元件 state 變 → 只重跑**它自己 + 它的子元件子樹**。
- 父元件、兄弟元件**不會**跟著重跑。

### 完整因果鏈
> `setMessages(新陣列)` → 存進**該元件**倉庫 + 排重畫 → `Object.is` 確認 reference 真的變 → 重跑 **該元件 + 子元件** → `useState()` 領到新值 → 畫面更新

## useEffect
監聽某個值改變後自動執行，類似 Vue 的 `watch`。
```ts
useEffect(() => {
  // 在 messages 改變時執行
}, [messages])
```

## useRef
取得 DOM 元素的參考，類似 `getElementById`，但是 React 的宣告式寫法。
```ts
const ref = useRef<HTMLDivElement>(null)
// 元件 render 前 ref.current 是 null
ref.current?.scrollIntoView()  // ?. 避免 null 報錯
```

## 單向資料流
React 沒有 Vue 的 `v-model`，需要明確綁定 value 和 onChange：
```tsx
<input value={input} onChange={(e) => setInput(e.target.value)} />
```

## JSX 括號規則
- `{}` → 放 JavaScript 表達式
- `()` → 包住多行 JSX（換行時必須用，否則 return 後自動補分號）

## TypeScript union type
限定變數只能是特定值：
```ts
role: 'user' | 'assistant'
```
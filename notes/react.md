# React

## useState
管理元件內部狀態，state 改變會觸發重新渲染。
```ts
const [value, setValue] = useState<string>('')
```
- 不能直接修改 state（如 `.push()`），要用 setter 函式
- 更新 array 用展開運算子：`setValue(prev => [...prev, newItem])`

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
import { useRef, useState, useEffect } from "react"

export default function ChatPanel() {
  const [input, setInput] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [messages, setMessages] = useState<Array<{role: 'user'| 'assistant', content: string, sources?: string[]}>>([])

  const handleSubmit = async function() {
    //  對話為空，跳過
    if (!input.trim()) return
    setLoading(true)
    setMessages(prev => [...prev, {role: 'user', content: input}])
    try {
      const req = await fetch('http://localhost:8010/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ question: input })
      })
      const data = await req.json()
      setMessages(prev => [...prev, {role: 'assistant', content: data.answer, sources: data.sources}])
    } catch(error) {
      setMessages(prev => [...prev, { role: 'assistant', content: '發生錯誤，請稍後再試' }])
    } finally {
      setInput('')
      setLoading(false)
    }
  }

  const bottomRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    bottomRef.current?.scrollIntoView()
  }, [messages])

  return (
    <div className="flex-1 h-screen flex flex-col bg-gray-950 text-white">
      {/* 訊息列表 */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <p className="text-gray-500 text-center text-sm">開始提問吧</p>
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] px-4 py-2 rounded-lg ${msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-800'}`}>
              {msg.content}
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2 text-xs text-gray-400">
                  <p>參考來源：</p>
                  {msg.sources.map((s,i) => (
                    <p key={i}>{s}</p>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* 輸入區 */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="輸入問題..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
            className="flex-1 bg-gray-800 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            送出
          </button>
        </div>
      </div>
    </div>
  )
}

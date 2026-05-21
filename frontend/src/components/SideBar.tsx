export default function SideBar() {
  return (
    <div className="w-64 h-screen bg-gray-900 text-white flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <button className="w-full py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded text-sm">
          + 新對話
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-2">
        <p className="text-gray-400 text-sm px-2 py-1">對話紀錄</p>
      </div>
    </div>
  )
}

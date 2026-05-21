import SideBar from "./components/SideBar";
import ChatPanel from "./components/ChatPanel";

export default function App () {
  return (
    <div className="flex">
      <SideBar></SideBar>
      <ChatPanel></ChatPanel>
    </div>
  )
}
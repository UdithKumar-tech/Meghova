import Sidebar from "./Sidebar"; import TopHeader from "./TopHeader";
export default function AppShell({children}){return <div className="app-shell"><TopHeader/><div className="app-body"><Sidebar/><main className="main-content">{children}</main></div></div>}

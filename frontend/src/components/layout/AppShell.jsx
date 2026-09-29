import Sidebar from "./Sidebar";
import TopHeader from "./TopHeader";

function AppShell({ children }) {

  return (

    <div className="app-shell">

      <TopHeader />

      <div className="app-body">

        <Sidebar />

        <main className="main-content">

          {children}

        </main>

      </div>

    </div>

  );
}

export default AppShell;
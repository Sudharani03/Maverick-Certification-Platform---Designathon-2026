import { Outlet } from 'react-router-dom'
import TopBar from '../utils/TopBar.jsx'
import Sidebar from '../utils/Sidebar.jsx'

const Layout = () => {
  return (
    <div className="min-h-screen bg-[#F5F7FA]">
      <TopBar />
      {/* Push content below the fixed header (60px) with extra breathing room */}
      <div className="flex pt-[60px]">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 pt-5 min-h-[calc(100vh-60px)]">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default Layout

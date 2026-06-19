import { useNavigate } from 'react-router-dom'
import { RiLogoutBoxRLine } from 'react-icons/ri'

const TopBar = () => {
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')

  const handleLogout = () => {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <div
      className="fixed top-0 left-0 right-0 z-40 h-[60px] flex items-center justify-between px-7"
      style={{
        background: 'linear-gradient(270deg, #04134A 0%, #0A1E5C 50%, #04134A 100%)',
        boxShadow: '0 2px 12px rgba(4, 13, 67, 0.4)',
      }}
    >
      {/* Logo & App Name */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-white/10 border border-white/10 flex items-center justify-center hover:bg-white/15 transition-all duration-300 cursor-pointer">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M4 12L10 6L16 12L10 18Z" fill="white"/>
            <path d="M10 12L16 6L22 12L16 18Z" fill="#60A5FA"/>
          </svg>
        </div>
        <span className="text-white font-semibold text-[15px] tracking-tight">Maverick Certification Hub</span>
      </div>

      {/* User Profile */}
      <div className="flex items-center gap-4">
        {user.name && (
          <div className="flex items-center gap-3 bg-white/8 hover:bg-white/12 border border-white/10 rounded-full px-4 py-1.5 transition-all duration-300 cursor-default">
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-xs font-bold shadow-md">
              {user.initials}
            </div>
            <div className="flex flex-col">
              <span className="text-white text-xs font-medium leading-tight">{user.name}</span>
              <span className="text-blue-300/70 text-[10px] leading-tight">{user.role}</span>
            </div>
          </div>
        )}
        <button
          onClick={handleLogout}
          className="w-8 h-8 rounded-lg bg-white/5 hover:bg-red-500/20 border border-white/10 hover:border-red-400/30 flex items-center justify-center text-white/60 hover:text-red-300 transition-all duration-300"
          title="Logout"
        >
          <RiLogoutBoxRLine className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}

export default TopBar

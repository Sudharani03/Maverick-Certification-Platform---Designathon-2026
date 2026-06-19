import { useLocation, useNavigate } from 'react-router-dom'
import { Tooltip } from 'antd'
import {
  RiFileTextLine,
  RiTeamLine,
  RiShieldCheckLine,
  RiBarChartBoxLine,
  RiCoupon3Line,
  RiDashboardLine,
  RiHistoryLine,
  RiHome4Line,
} from 'react-icons/ri'

const menuItems = [
  { key: '/drives', label: 'All Drives', icon: RiHome4Line },
  { key: '/drive-details', label: 'Drive Details', icon: RiFileTextLine },
  { key: '/registrations', label: 'Registrations', icon: RiTeamLine },
  { key: '/eligibility', label: 'Eligibility', icon: RiShieldCheckLine },
  { key: '/assessment-results', label: 'Assessment Results', icon: RiBarChartBoxLine },
  { key: '/voucher-management', label: 'Voucher Management', icon: RiCoupon3Line, adminOnly: true },
  { key: '/reports', label: 'Reports & Analytics', icon: RiDashboardLine },
  { key: '/audit-log', label: 'Audit Log', icon: RiHistoryLine, adminOnly: true },
]

const Sidebar = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')
  const isAdmin = user.role === 'Admin'

  const visibleItems = menuItems.filter(item => !item.adminOnly || isAdmin)

  return (
    <div className="w-[240px] flex-shrink-0">
      <div className="bg-white rounded-xl border border-[#E3EBFE] shadow-[0_4px_15px_rgba(21,75,199,0.06)] m-3 p-3 min-h-[calc(100vh-90px)] sticky top-[72px]">
        <div className="mb-3 px-3 pt-1">
          <p className="text-[10px] uppercase tracking-wider text-gray-400 font-semibold">Navigation</p>
        </div>
        <nav className="flex flex-col gap-1.5">
          {visibleItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.key
            return (
              <button
                key={item.key}
                onClick={() => navigate(item.key)}
                className={`group flex items-center gap-3 h-[42px] px-4 rounded-lg text-[13px] font-medium transition-all duration-300 w-full text-left relative overflow-hidden ${
                  isActive
                    ? 'text-white shadow-[0_4px_12px_rgba(21,75,199,0.3)]'
                    : 'text-gray-600 hover:text-[#154BC7] hover:bg-blue-50/60'
                }`}
                style={isActive ? {
                  background: 'linear-gradient(135deg, #154BC7 0%, #1E6FD9 100%)',
                } : {}}
              >
                {/* Shine effect on hover */}
                {!isActive && (
                  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                    style={{ background: 'linear-gradient(90deg, transparent 0%, rgba(21,75,199,0.04) 50%, transparent 100%)' }} />
                )}
                <Icon className={`w-[18px] h-[18px] flex-shrink-0 transition-transform duration-300 ${isActive ? '' : 'group-hover:scale-110'}`} />
                <span className="truncate">{item.label}</span>
                {/* Active indicator dot */}
                {isActive && (
                  <div className="absolute right-3 w-1.5 h-1.5 rounded-full bg-white/80 shadow-[0_0_6px_rgba(255,255,255,0.8)]" />
                )}
              </button>
            )
          })}
        </nav>

        {/* Footer info */}
        <div className="mt-6 px-3 pt-4 border-t border-gray-100">
          <p className="text-[10px] text-gray-400">Logged in as</p>
          <p className="text-xs font-medium text-gray-700">{user.name}</p>
          <p className="text-[10px] text-blue-500">{user.role}</p>
        </div>
      </div>
    </div>
  )
}

export default Sidebar

import { useNavigate } from 'react-router-dom'
import { message } from 'antd'
import { RiShieldCheckLine, RiUserLine } from 'react-icons/ri'
import { loginUser } from '../config/api/apiConfig.js'
import bgImage from '../assets/Background.png'

const Login = () => {
  const navigate = useNavigate()

  const handleLogin = async (role) => {
    try {
      const res = await loginUser(role)
      if (res.data) {
        localStorage.setItem('auth_user', JSON.stringify(res.data))
        navigate('/drives')
      }
    } catch (err) {
      message.error('Login failed. Is the backend running?')
    }
  }

  return (
    <div
      className="min-h-screen flex items-center justify-end pr-[8%]"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }}
    >
      {/* Highlighted login card — right center, stands out on mixed bg */}
      <div
        className="w-full max-w-[420px] rounded-2xl p-10 border border-white/30 shadow-2xl backdrop-blur-xl"
        style={{
          background: 'linear-gradient(145deg, rgba(20, 30, 70, 0.88) 0%, rgba(10, 18, 50, 0.92) 100%)',
          boxShadow: '0 12px 48px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255,255,255,0.08), inset 0 1px 0 rgba(255,255,255,0.12)',
        }}
      >
        <div className="text-center mb-10">
          <div className="flex justify-center mb-5">
            <div className="w-16 h-16 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center shadow-lg">
              <svg width="36" height="36" viewBox="0 0 32 32" fill="none">
                <path d="M6 16L13 9L20 16L13 23Z" fill="white"/>
                <path d="M13 16L20 9L27 16L20 23Z" fill="#60A5FA"/>
              </svg>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-white mb-2 tracking-tight">Maverick Certification Hub</h1>
          <p className="text-blue-200/80 text-sm">MAP Certification Drive Automation Platform</p>
        </div>

        <div className="space-y-4">
          <button
            onClick={() => handleLogin('Admin')}
            className="w-full py-3.5 px-6 rounded-xl text-white font-semibold text-sm flex items-center justify-center gap-3 transition-all duration-300 hover:scale-[1.03] hover:shadow-[0_0_20px_rgba(21,75,199,0.5)] active:scale-[0.98]"
            style={{ background: 'linear-gradient(135deg, #154BC7 0%, #1E6FD9 50%, #2B85E8 100%)' }}
          >
            <RiShieldCheckLine className="w-5 h-5" />
            Login as Admin
          </button>
          <button
            onClick={() => handleLogin('User')}
            className="w-full py-3.5 px-6 rounded-xl text-white font-semibold text-sm flex items-center justify-center gap-3 transition-all duration-300 hover:scale-[1.03] hover:shadow-[0_0_20px_rgba(255,255,255,0.15)] active:scale-[0.98] bg-white/10 border border-white/25 hover:bg-white/20"
          >
            <RiUserLine className="w-5 h-5" />
            Login as User
          </button>
        </div>

        <p className="text-center text-blue-300/50 text-xs mt-10">
          © 2026 Hexaware Technologies. All rights reserved.
        </p>
      </div>
    </div>
  )
}

export default Login

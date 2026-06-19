import { useState, useEffect } from 'react'
import { message, Spin } from 'antd'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'
import { getDriveSummary, getFunnelData, getPassFailTrends, getVoucherUtilization } from '../config/api/apiConfig.js'
import useDrive from '../utils/useDrive.js'

const COLORS = { blue: '#154BC7', green: '#59BE9C', orange: '#F59E0B', red: '#EF4444', purple: '#7C3AED', lightBlue: '#93C5FD' }

const Reports = () => {
  const [summary, setSummary] = useState(null)
  const [funnel, setFunnel] = useState([])
  const [passFail, setPassFail] = useState([])
  const [utilization, setUtilization] = useState(null)
  const [loading, setLoading] = useState(true)
  const drive = useDrive()

  useEffect(() => { if (drive?.drive_id) fetchData() }, [drive])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [sumRes, funRes, pfRes, utilRes] = await Promise.all([
        getDriveSummary(drive.drive_id),
        getFunnelData(drive.drive_id),
        getPassFailTrends(drive.drive_id),
        getVoucherUtilization(drive.drive_id),
      ])
      setSummary(sumRes.data)
      setFunnel(funRes.data || [])
      setPassFail(pfRes.data || [])
      setUtilization(utilRes.data)
    } catch (err) { message.error('Failed to load reports') }
    finally { setLoading(false) }
  }

  if (loading) return <div className="flex justify-center py-20"><Spin /></div>

  const metricCards = [
    { label: 'Total Registered', value: summary?.total_registered || 0, bg: '#E3EBFE', color: '#154BC7' },
    { label: 'Eligible', value: summary?.eligible || 0, bg: '#D1FAE5', color: '#059669' },
    { label: 'Passed', value: summary?.passed || 0, bg: '#FEF6EB', color: '#D97706' },
    { label: 'Vouchers Issued', value: summary?.vouchers_allocated || 0, bg: '#EDE9FE', color: '#7C3AED' },
    { label: 'Redeemed', value: summary?.vouchers_redeemed || 0, bg: '#D1FAE5', color: '#059669' },
    { label: 'Utilization', value: `${utilization?.utilization_percentage || 0}%`, bg: '#E3EBFE', color: '#154BC7' },
  ]

  const pieData = utilization ? [
    { name: 'Available', value: utilization.available, color: COLORS.lightBlue },
    { name: 'Allocated', value: utilization.allocated, color: COLORS.orange },
    { name: 'Redeemed', value: utilization.redeemed, color: COLORS.green },
    { name: 'Expired', value: utilization.expired, color: COLORS.red },
  ].filter(d => d.value > 0) : []

  return (
    <div>
      <h2 className="text-lg font-bold text-gray-900 mb-4">Reports & Analytics</h2>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        {metricCards.map((card, i) => (
          <div key={i} className="metric-card rounded-xl p-4 border cursor-default" style={{ background: card.bg, borderColor: card.bg }}>
            <p className="text-[11px] text-gray-600 mb-1">{card.label}</p>
            <p className="text-xl font-bold" style={{ color: card.color }}>{card.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Funnel Chart */}
        <div className="hover-glow bg-white rounded-xl border border-gray-100 p-5">
          <h3 className="text-sm font-semibold text-gray-800 mb-4">Certification Journey Funnel</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={funnel} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" tick={{ fontSize: 11 }} />
              <YAxis type="category" dataKey="step" tick={{ fontSize: 10 }} width={80} />
              <Tooltip contentStyle={{ fontSize: 11 }} />
              <Bar dataKey="count" fill={COLORS.blue} radius={[0, 4, 4, 0]} barSize={18} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pass/Fail by Track */}
        <div className="hover-glow bg-white rounded-xl border border-gray-100 p-5">
          <h3 className="text-sm font-semibold text-gray-800 mb-4">Pass/Fail by Track</h3>
          {passFail.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={passFail} margin={{ left: -10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="track" tick={{ fontSize: 9 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ fontSize: 11 }} />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Bar dataKey="passed" fill={COLORS.green} name="Passed" radius={[4, 4, 0, 0]} barSize={20} />
                <Bar dataKey="failed" fill={COLORS.red} name="Failed" radius={[4, 4, 0, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="text-xs text-gray-400 text-center py-10">No data yet</p>}
        </div>

        {/* Voucher Utilization Pie */}
        <div className="hover-glow bg-white rounded-xl border border-gray-100 p-5">
          <h3 className="text-sm font-semibold text-gray-800 mb-4">Voucher Distribution</h3>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" outerRadius={70} dataKey="value" label={({ name, value }) => `${name}: ${value}`}
                  labelLine={false} style={{ fontSize: 10 }}>
                  {pieData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                </Pie>
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="text-xs text-gray-400 text-center py-10">No voucher data</p>}
        </div>

        {/* Summary Stats */}
        <div className="hover-glow bg-white rounded-xl border border-gray-100 p-5">
          <h3 className="text-sm font-semibold text-gray-800 mb-4">Quick Stats</h3>
          <div className="space-y-2">
            {[
              { label: 'Total Assessed', value: summary?.assessed || 0 },
              { label: 'Failed', value: summary?.failed || 0 },
              { label: 'Pending Approval', value: summary?.pending_approval || 0 },
              { label: 'Vouchers in Pool', value: summary?.vouchers_total || 0 },
              { label: 'Vouchers Available', value: summary?.vouchers_available || 0 },
              { label: 'Avg Days to Redeem', value: utilization?.avg_days_to_redeem || '-' },
            ].map((item, i) => (
              <div key={i} className="flex justify-between items-center py-1 border-b border-gray-50">
                <span className="text-xs text-gray-600">{item.label}</span>
                <span className="text-sm font-semibold text-gray-900">{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Reports

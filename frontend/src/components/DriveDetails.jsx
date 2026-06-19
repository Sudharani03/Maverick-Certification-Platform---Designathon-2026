import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Tag, Button, message, Spin } from 'antd'
import { RiArrowLeftLine, RiEditLine } from 'react-icons/ri'
import { getDriveDetails, getDriveSummary } from '../config/api/apiConfig.js'

const DriveDetails = () => {
  const navigate = useNavigate()
  const [drive, setDrive] = useState(null)
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const stored = JSON.parse(localStorage.getItem('selected_drive') || '{}')

  useEffect(() => {
    if (stored.drive_id) fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [driveRes, summaryRes] = await Promise.all([
        getDriveDetails(stored.drive_id),
        getDriveSummary(stored.drive_id),
      ])
      setDrive(driveRes.data)
      setSummary(summaryRes.data)
    } catch (err) {
      message.error('Failed to load drive details')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="flex justify-center py-20"><Spin /></div>
  if (!drive) return <p className="text-center text-gray-400 py-10">No drive selected</p>

  const metricCards = [
    { label: 'Registered', value: summary?.total_registered || 0, bg: '#E3EBFE', color: '#154BC7' },
    { label: 'Eligible', value: summary?.eligible || 0, bg: '#D1FAE5', color: '#059669' },
    { label: 'Passed', value: summary?.passed || 0, bg: '#FEF6EB', color: '#D97706' },
    { label: 'Vouchers Issued', value: summary?.vouchers_allocated || 0, bg: '#EDE9FE', color: '#7C3AED' },
  ]

  return (
    <div>
      <button onClick={() => navigate('/drives')} className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-800 mb-3">
        <RiArrowLeftLine /> Back to Drives
      </button>

      <div className="bg-white rounded-lg border border-gray-200 p-5 mb-4">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h1 className="text-lg font-bold text-gray-900">{drive.name}</h1>
              <Tag color={drive.status === 'active' ? 'blue' : 'default'}>{drive.status}</Tag>
            </div>
            <p className="text-xs text-gray-500">Sponsor: {drive.sponsor} | Budget: ₹{drive.budget?.toLocaleString()} | Target: {drive.target_count}</p>
            <p className="text-xs text-gray-500 mt-0.5">Period: {drive.start_date} to {drive.end_date} | Pass Threshold: {drive.pass_threshold}%</p>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-5">
          {metricCards.map((card, i) => (
            <div key={i} className="metric-card rounded-xl p-4 border cursor-default" style={{ background: card.bg, borderColor: card.bg }}>
              <p className="text-xs text-gray-600 mb-1">{card.label}</p>
              <p className="text-2xl font-bold" style={{ color: card.color }}>{card.value}</p>
            </div>
          ))}
        </div>
      </div>

      {drive.policy_notes && (
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h3 className="text-sm font-semibold text-gray-800 mb-1">Policy Notes</h3>
          <p className="text-xs text-gray-600">{drive.policy_notes}</p>
        </div>
      )}
    </div>
  )
}

export default DriveDetails

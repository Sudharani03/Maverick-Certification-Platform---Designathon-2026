import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Input, Tag, Modal, Button, message, Spin } from 'antd'
import { RiSearchLine, RiAddLine, RiDeleteBinLine, RiCalendarLine } from 'react-icons/ri'
import { getAllDrives, deleteDrive } from '../config/api/apiConfig.js'

const DrivesDashboard = () => {
  const navigate = useNavigate()
  const [drives, setDrives] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [deleteModalOpen, setDeleteModalOpen] = useState(false)
  const [driveToDelete, setDriveToDelete] = useState(null)
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')
  const isAdmin = user.role === 'Admin'

  useEffect(() => { fetchDrives() }, [])

  const fetchDrives = async () => {
    try {
      setLoading(true)
      const res = await getAllDrives()
      const drivesList = res.data || []
      setDrives(drivesList)
      // Auto-select first drive if none selected
      if (drivesList.length > 0 && !localStorage.getItem('selected_drive')) {
        localStorage.setItem('selected_drive', JSON.stringify(drivesList[0]))
      }
    } catch (err) {
      message.error('Failed to fetch drives')
    } finally {
      setLoading(false)
    }
  }

  const handleDriveClick = (drive) => {
    localStorage.setItem('selected_drive', JSON.stringify(drive))
    navigate('/drive-details')
  }

  const handleDelete = async () => {
    try {
      await deleteDrive(driveToDelete.drive_id)
      message.success('Drive deleted successfully')
      setDeleteModalOpen(false)
      setDriveToDelete(null)
      fetchDrives()
    } catch (err) {
      message.error('Failed to delete drive')
    }
  }

  const filteredDrives = drives.filter(d =>
    d.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const getStatusColor = (status) => {
    const colors = { active: 'blue', closed: 'default', draft: 'orange' }
    return colors[status] || 'default'
  }

  return (
    <div className="fade-in-up">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Certification Drives</h1>
          <p className="text-xs text-gray-500 mt-0.5">Manage MAP certification drives</p>
        </div>
        {isAdmin && (
          <Button type="primary" icon={<RiAddLine />} onClick={() => navigate('/create-drive')}
            style={{ background: '#154BC7', borderRadius: '8px', height: '38px', fontWeight: 600, fontSize: '13px' }}>
            Create Drive
          </Button>
        )}
      </div>

      <div className="mb-5">
        <Input prefix={<RiSearchLine className="text-gray-400" />}
          placeholder="Search drives..." value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="max-w-sm" size="large"
          style={{ borderRadius: '8px' }} />
      </div>

      {loading ? (
        <div className="flex justify-center py-20"><Spin size="large" /></div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredDrives.map((drive) => (
            <div key={drive.drive_id}
              className="card-shine hover-glow bg-white rounded-xl border border-gray-100 p-5 cursor-pointer group"
              onClick={() => handleDriveClick(drive)}>
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-[15px] font-semibold text-gray-900 group-hover:text-[#154BC7] transition-colors duration-300 line-clamp-2">
                  {drive.name}
                </h3>
                {isAdmin && (
                  <button onClick={(e) => { e.stopPropagation(); setDriveToDelete(drive); setDeleteModalOpen(true) }}
                    className="p-1.5 rounded-lg hover:bg-red-50 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all duration-300">
                    <RiDeleteBinLine className="w-4 h-4" />
                  </button>
                )}
              </div>
              <Tag color={getStatusColor(drive.status)} className="text-xs mb-3">
                {drive.status.charAt(0).toUpperCase() + drive.status.slice(1)}
              </Tag>
              <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
                <RiCalendarLine className="w-3.5 h-3.5" />
                <span>{drive.start_date} — {drive.end_date}</span>
              </div>
              <div className="text-xs text-gray-500 flex justify-between">
                <span>Budget: ₹{drive.budget?.toLocaleString()}</span>
                <span>Target: {drive.target_count}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && filteredDrives.length === 0 && (
        <div className="text-center py-16">
          <p className="text-gray-400 text-sm">No drives found</p>
        </div>
      )}

      <Modal title="Delete Drive" open={deleteModalOpen}
        onOk={handleDelete} onCancel={() => { setDeleteModalOpen(false); setDriveToDelete(null) }}
        okText="Delete" okButtonProps={{ danger: true }} centered maskClosable={false}>
        <p className="text-sm text-gray-600">
          Delete <strong>{driveToDelete?.name}</strong>? This cannot be undone.
        </p>
      </Modal>
    </div>
  )
}

export default DrivesDashboard

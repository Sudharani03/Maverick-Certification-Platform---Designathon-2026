import { useState, useEffect } from 'react'
import { Table, Tag, Button, Input, Modal, message, Upload, Spin } from 'antd'
import { RiSearchLine, RiAddLine, RiUploadCloud2Line } from 'react-icons/ri'
import { getRegistrations, registerCandidate, bulkImportRegistrations } from '../config/api/apiConfig.js'

const Registrations = () => {
  const [registrations, setRegistrations] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [form, setForm] = useState({ emp_id: '', name: '', email: '', bu: '', location: '', manager_email: '', exam_track: '', slot: '', prior_attempts: 0 })
  const drive = JSON.parse(localStorage.getItem('selected_drive') || '{}')
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')
  const isAdmin = user.role === 'Admin'

  useEffect(() => { if (drive.drive_id) fetchData() }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const res = await getRegistrations(drive.drive_id)
      setRegistrations(res.data || [])
    } catch (err) { message.error('Failed to fetch registrations') }
    finally { setLoading(false) }
  }

  const handleRegister = async () => {
    if (!form.emp_id || !form.name || !form.email) { message.error('Fill required fields'); return }
    try {
      await registerCandidate({ ...form, drive_id: drive.drive_id })
      message.success('Candidate registered')
      setModalOpen(false)
      setForm({ emp_id: '', name: '', email: '', bu: '', location: '', manager_email: '', exam_track: '', slot: '', prior_attempts: 0 })
      fetchData()
    } catch (err) { message.error(err.response?.data?.message || 'Registration failed') }
  }

  const handleBulkImport = async (file) => {
    try {
      const res = await bulkImportRegistrations(drive.drive_id, file)
      message.success(res.message)
      fetchData()
    } catch (err) { message.error('Bulk import failed') }
    return false
  }

  const statusColor = (s) => ({ registered: 'blue', eligible: 'green', ineligible: 'red', passed: 'green', failed: 'red' }[s] || 'default')

  const filtered = registrations.filter(r =>
    r.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    r.emp_id.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const columns = [
    { title: 'Emp ID', dataIndex: 'emp_id', key: 'emp_id', width: 90 },
    { title: 'Name', dataIndex: 'name', key: 'name', width: 140 },
    { title: 'Email', dataIndex: 'email', key: 'email', width: 180, ellipsis: true },
    { title: 'Track', dataIndex: 'exam_track', key: 'exam_track', width: 130 },
    { title: 'Slot', dataIndex: 'slot', key: 'slot', width: 100 },
    { title: 'Status', dataIndex: 'status', key: 'status', width: 100, render: (s) => <Tag color={statusColor(s)}>{s}</Tag> },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900">Registrations</h2>
        <div className="flex gap-2">
          {isAdmin && (
            <>
              <Upload beforeUpload={handleBulkImport} accept=".csv" showUploadList={false}>
                <Button icon={<RiUploadCloud2Line />} size="small">Import CSV</Button>
              </Upload>
              <Button type="primary" icon={<RiAddLine />} size="small" onClick={() => setModalOpen(true)}
                style={{ background: '#154BC7' }}>Register</Button>
            </>
          )}
        </div>
      </div>

      <div className="mb-3">
        <Input prefix={<RiSearchLine className="text-gray-400" />} placeholder="Search by name or emp ID..."
          value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="max-w-xs" size="small" />
      </div>

      <div className="bg-white rounded-lg border border-gray-200">
        <Table columns={columns} dataSource={filtered} rowKey="reg_id" size="small"
          loading={loading} pagination={{ pageSize: 10 }} scroll={{ x: 700 }} />
      </div>

      <Modal title="Register Candidate" open={modalOpen} onOk={handleRegister}
        onCancel={() => setModalOpen(false)} okText="Register" centered
        okButtonProps={{ style: { background: '#154BC7' } }}>
        <div className="space-y-3 mt-4">
          <Input placeholder="Employee ID *" value={form.emp_id} onChange={(e) => setForm({...form, emp_id: e.target.value})} />
          <Input placeholder="Full Name *" value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} />
          <Input placeholder="Email *" value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} />
          <div className="grid grid-cols-2 gap-2">
            <Input placeholder="Business Unit" value={form.bu} onChange={(e) => setForm({...form, bu: e.target.value})} />
            <Input placeholder="Location" value={form.location} onChange={(e) => setForm({...form, location: e.target.value})} />
          </div>
          <Input placeholder="Manager Email" value={form.manager_email} onChange={(e) => setForm({...form, manager_email: e.target.value})} />
          <div className="grid grid-cols-2 gap-2">
            <Input placeholder="Exam Track" value={form.exam_track} onChange={(e) => setForm({...form, exam_track: e.target.value})} />
            <Input placeholder="Slot (YYYY-MM-DD)" value={form.slot} onChange={(e) => setForm({...form, slot: e.target.value})} />
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default Registrations

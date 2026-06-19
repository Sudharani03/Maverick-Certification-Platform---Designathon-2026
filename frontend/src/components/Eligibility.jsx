import { useState, useEffect } from 'react'
import { Table, Tag, Button, Modal, Input, message } from 'antd'
import { RiCheckLine, RiCloseLine, RiPlayLine } from 'react-icons/ri'
import { getEligibility, getRegistrations, bulkEvaluate, approveCandidate, rejectCandidate } from '../config/api/apiConfig.js'
import useDrive from '../utils/useDrive.js'

const Eligibility = () => {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [rejectModal, setRejectModal] = useState({ open: false, eligId: null })
  const [reason, setReason] = useState('')
  const drive = useDrive()
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')
  const isAdmin = user.role === 'Admin'

  useEffect(() => { if (drive?.drive_id) fetchData() }, [drive])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [eligRes, regRes] = await Promise.all([
        getEligibility(drive.drive_id),
        getRegistrations(drive.drive_id),
      ])
      const regs = regRes.data || []
      const regMap = {}
      regs.forEach(r => { regMap[r.reg_id] = r })

      // Enrich eligibility records with candidate name
      const enriched = (eligRes.data || []).map(e => ({
        ...e,
        candidate_name: regMap[e.reg_id]?.name || e.reg_id,
        emp_id: regMap[e.reg_id]?.emp_id || '-',
      }))
      setRecords(enriched)
    } catch (err) { message.error('Failed to fetch eligibility data') }
    finally { setLoading(false) }
  }

  const handleBulkEvaluate = async () => {
    try {
      const res = await bulkEvaluate(drive.drive_id)
      message.success(res.message)
      fetchData()
    } catch (err) { message.error('Bulk evaluation failed') }
  }

  const handleApprove = async (eligId) => {
    try {
      await approveCandidate(eligId)
      message.success('Candidate approved')
      fetchData()
    } catch (err) { message.error('Approval failed') }
  }

  const handleReject = async () => {
    try {
      await rejectCandidate(rejectModal.eligId, reason)
      message.success('Candidate rejected')
      setRejectModal({ open: false, eligId: null })
      setReason('')
      fetchData()
    } catch (err) { message.error('Rejection failed') }
  }

  const decisionColor = (d) => ({ eligible: 'green', ineligible: 'red', pending_approval: 'orange' }[d] || 'default')

  const columns = [
    { title: 'Emp ID', dataIndex: 'emp_id', key: 'emp_id', width: 90 },
    { title: 'Candidate', dataIndex: 'candidate_name', key: 'name', width: 150 },
    { title: 'Decision', dataIndex: 'decision', key: 'decision', width: 110,
      render: (d) => <Tag color={decisionColor(d)}>{d}</Tag> },
    { title: 'Tenure', key: 'tenure', width: 80,
      render: (_, r) => <Tag color={r.criteria?.tenure_check ? 'green' : 'red'}>{r.criteria?.tenure_check ? '✓ Pass' : '✗ Fail'}</Tag> },
    { title: 'Training', key: 'training', width: 80,
      render: (_, r) => <Tag color={r.criteria?.training_complete ? 'green' : 'red'}>{r.criteria?.training_complete ? '✓ Done' : '✗ No'}</Tag> },
    { title: 'Attempts', key: 'attempts', width: 90,
      render: (_, r) => <Tag color={r.criteria?.prior_attempts_check ? 'green' : 'red'}>{r.criteria?.prior_attempts_check ? '✓ OK' : '✗ Exceeded'}</Tag> },
    { title: 'Budget', key: 'budget', width: 80,
      render: (_, r) => <Tag color={r.criteria?.budget_check ? 'green' : 'red'}>{r.criteria?.budget_check ? '✓ OK' : '✗ Full'}</Tag> },
    { title: 'Notes', dataIndex: 'notes', key: 'notes', ellipsis: true },
    ...(isAdmin ? [{
      title: 'Actions', key: 'actions', width: 130,
      render: (_, r) => r.decision === 'pending_approval' ? (
        <div className="flex gap-1">
          <Button size="small" type="primary" icon={<RiCheckLine />} onClick={() => handleApprove(r.elig_id)} style={{ background: '#059669', fontSize: 11 }}>Approve</Button>
          <Button size="small" danger icon={<RiCloseLine />} onClick={() => setRejectModal({ open: true, eligId: r.elig_id })} style={{ fontSize: 11 }}>Reject</Button>
        </div>
      ) : null
    }] : []),
  ]

  return (
    <div className="fade-in-up">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-bold text-gray-900">Eligibility Evaluation</h2>
          <p className="text-xs text-gray-500">Drive: {drive?.name || '—'} | {records.length} records</p>
        </div>
        {isAdmin && (
          <Button type="primary" icon={<RiPlayLine />} onClick={handleBulkEvaluate} size="small"
            style={{ background: '#154BC7' }}>Evaluate All</Button>
        )}
      </div>

      <div className="bg-white rounded-xl border border-gray-100 hover-glow">
        <Table columns={columns} dataSource={records} rowKey="elig_id" size="small"
          loading={loading} pagination={{ pageSize: 12 }} scroll={{ x: 900 }} />
      </div>

      <Modal title="Reject Candidate" open={rejectModal.open}
        onOk={handleReject} onCancel={() => { setRejectModal({ open: false, eligId: null }); setReason('') }}
        okText="Reject" okButtonProps={{ danger: true }} centered>
        <Input.TextArea rows={3} placeholder="Reason for rejection..." value={reason} onChange={(e) => setReason(e.target.value)} />
      </Modal>
    </div>
  )
}

export default Eligibility

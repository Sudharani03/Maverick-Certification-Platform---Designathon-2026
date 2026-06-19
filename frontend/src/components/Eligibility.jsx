import { useState, useEffect } from 'react'
import { Table, Tag, Button, Modal, Input, message, Spin } from 'antd'
import { RiCheckLine, RiCloseLine, RiPlayLine } from 'react-icons/ri'
import { getEligibility, bulkEvaluate, approveCandidate, rejectCandidate } from '../config/api/apiConfig.js'

const Eligibility = () => {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [rejectModal, setRejectModal] = useState({ open: false, eligId: null })
  const [reason, setReason] = useState('')
  const drive = JSON.parse(localStorage.getItem('selected_drive') || '{}')
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')
  const isAdmin = user.role === 'Admin'

  useEffect(() => { if (drive.drive_id) fetchData() }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const res = await getEligibility(drive.drive_id)
      setRecords(res.data || [])
    } catch (err) { message.error('Failed to fetch eligibility') }
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
    { title: 'Reg ID', dataIndex: 'reg_id', key: 'reg_id', width: 110, ellipsis: true },
    { title: 'Decision', dataIndex: 'decision', key: 'decision', width: 120,
      render: (d) => <Tag color={decisionColor(d)}>{d}</Tag> },
    { title: 'Tenure Check', key: 'tenure', width: 100,
      render: (_, r) => <Tag color={r.criteria?.tenure_check ? 'green' : 'red'}>{r.criteria?.tenure_check ? 'Pass' : 'Fail'}</Tag> },
    { title: 'Training', key: 'training', width: 90,
      render: (_, r) => <Tag color={r.criteria?.training_complete ? 'green' : 'red'}>{r.criteria?.training_complete ? 'Done' : 'No'}</Tag> },
    { title: 'Attempts', key: 'attempts', width: 90,
      render: (_, r) => <Tag color={r.criteria?.prior_attempts_check ? 'green' : 'red'}>{r.criteria?.prior_attempts_check ? 'OK' : 'Exceeded'}</Tag> },
    { title: 'Notes', dataIndex: 'notes', key: 'notes', ellipsis: true },
    ...(isAdmin ? [{
      title: 'Actions', key: 'actions', width: 120,
      render: (_, r) => r.decision === 'pending_approval' ? (
        <div className="flex gap-1">
          <Button size="small" type="primary" icon={<RiCheckLine />} onClick={() => handleApprove(r.elig_id)} style={{ background: '#059669', fontSize: 11 }}>OK</Button>
          <Button size="small" danger icon={<RiCloseLine />} onClick={() => setRejectModal({ open: true, eligId: r.elig_id })} style={{ fontSize: 11 }}>No</Button>
        </div>
      ) : null
    }] : []),
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900">Eligibility</h2>
        {isAdmin && (
          <Button type="primary" icon={<RiPlayLine />} onClick={handleBulkEvaluate} size="small"
            style={{ background: '#154BC7' }}>Evaluate All</Button>
        )}
      </div>

      <div className="bg-white rounded-lg border border-gray-200">
        <Table columns={columns} dataSource={records} rowKey="elig_id" size="small"
          loading={loading} pagination={{ pageSize: 10 }} scroll={{ x: 700 }} />
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

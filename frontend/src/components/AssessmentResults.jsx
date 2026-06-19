import { useState, useEffect } from 'react'
import { Table, Tag, Button, Input, Modal, InputNumber, Upload, message } from 'antd'
import { RiSearchLine, RiAddLine, RiUploadCloud2Line } from 'react-icons/ri'
import { getResults, getRegistrations, importResult, bulkImportResults } from '../config/api/apiConfig.js'
import useDrive from '../utils/useDrive.js'

const AssessmentResults = () => {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [form, setForm] = useState({ reg_id: '', score: 0, exam_date: '' })
  const drive = useDrive()
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')
  const isAdmin = user.role === 'Admin'

  useEffect(() => { if (drive?.drive_id) fetchData() }, [drive])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [resRes, regRes] = await Promise.all([
        getResults(drive.drive_id),
        getRegistrations(drive.drive_id),
      ])
      const regs = regRes.data || []
      const regMap = {}
      regs.forEach(r => { regMap[r.reg_id] = r })

      const enriched = (resRes.data || []).map(r => ({
        ...r,
        candidate_name: regMap[r.reg_id]?.name || r.reg_id,
        emp_id: regMap[r.reg_id]?.emp_id || '-',
      }))
      setResults(enriched)
    } catch (err) { message.error('Failed to fetch results') }
    finally { setLoading(false) }
  }

  const handleImport = async () => {
    if (!form.reg_id || !form.exam_date) { message.error('Fill required fields'); return }
    try {
      await importResult(form)
      message.success('Result imported')
      setModalOpen(false)
      setForm({ reg_id: '', score: 0, exam_date: '' })
      fetchData()
    } catch (err) { message.error(err.response?.data?.message || 'Import failed') }
  }

  const handleBulkImport = async (file) => {
    try {
      const res = await bulkImportResults(drive.drive_id, file)
      message.success(res.message)
      fetchData()
    } catch (err) { message.error('Bulk import failed') }
    return false
  }

  const filtered = results.filter(r =>
    (r.candidate_name || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (r.emp_id || '').toLowerCase().includes(searchQuery.toLowerCase())
  )

  const columns = [
    { title: 'Emp ID', dataIndex: 'emp_id', key: 'emp_id', width: 90 },
    { title: 'Candidate', dataIndex: 'candidate_name', key: 'name', width: 150 },
    { title: 'Score', dataIndex: 'score', key: 'score', width: 70, render: (s) => <span className="font-semibold">{s}%</span> },
    { title: 'Threshold', dataIndex: 'pass_threshold', key: 'threshold', width: 80, render: (t) => `${t}%` },
    { title: 'Outcome', dataIndex: 'outcome', key: 'outcome', width: 90,
      render: (o) => <Tag color={o === 'passed' ? 'green' : 'red'}>{o === 'passed' ? '✓ Passed' : '✗ Failed'}</Tag> },
    { title: 'Exam Date', dataIndex: 'exam_date', key: 'date', width: 100 },
    { title: 'Evidence', dataIndex: 'evidence_filename', key: 'evidence', width: 130, ellipsis: true,
      render: (f) => f ? <span className="text-blue-600 text-xs">{f}</span> : <span className="text-gray-400">—</span> },
  ]

  return (
    <div className="fade-in-up">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-bold text-gray-900">Assessment Results</h2>
          <p className="text-xs text-gray-500">Drive: {drive?.name || '—'} | {results.length} results</p>
        </div>
        {isAdmin && (
          <div className="flex gap-2">
            <Upload beforeUpload={handleBulkImport} accept=".csv" showUploadList={false}>
              <Button icon={<RiUploadCloud2Line />} size="small">Import CSV</Button>
            </Upload>
            <Button type="primary" icon={<RiAddLine />} size="small" onClick={() => setModalOpen(true)}
              style={{ background: '#154BC7' }}>Add Result</Button>
          </div>
        )}
      </div>

      <div className="mb-3">
        <Input prefix={<RiSearchLine className="text-gray-400" />} placeholder="Search by name or emp ID..."
          value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="max-w-xs" size="small" />
      </div>

      <div className="bg-white rounded-xl border border-gray-100 hover-glow">
        <Table columns={columns} dataSource={filtered} rowKey="result_id" size="small"
          loading={loading} pagination={{ pageSize: 10 }} scroll={{ x: 700 }} />
      </div>

      <Modal title="Add Result" open={modalOpen} onOk={handleImport} onCancel={() => setModalOpen(false)}
        okText="Import" centered okButtonProps={{ style: { background: '#154BC7' } }}>
        <div className="space-y-3 mt-4">
          <Input placeholder="Registration ID *" value={form.reg_id} onChange={(e) => setForm({...form, reg_id: e.target.value})} />
          <InputNumber className="w-full" placeholder="Score (%)" value={form.score}
            onChange={(v) => setForm({...form, score: v || 0})} min={0} max={100} />
          <Input type="date" value={form.exam_date} onChange={(e) => setForm({...form, exam_date: e.target.value})} />
        </div>
      </Modal>
    </div>
  )
}

export default AssessmentResults

import { useState, useEffect } from 'react'
import { Table, Tag, Button, Input, Modal, InputNumber, Upload, message } from 'antd'
import { RiSearchLine, RiAddLine, RiUploadCloud2Line } from 'react-icons/ri'
import { getResults, importResult, bulkImportResults } from '../config/api/apiConfig.js'
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
      const res = await getResults(drive.drive_id)
      setResults(res.data || [])
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

  const outcomeColor = (o) => o === 'passed' ? 'green' : 'red'

  const columns = [
    { title: 'Reg ID', dataIndex: 'reg_id', key: 'reg_id', width: 110, ellipsis: true },
    { title: 'Score', dataIndex: 'score', key: 'score', width: 70 },
    { title: 'Threshold', dataIndex: 'pass_threshold', key: 'pass_threshold', width: 80 },
    { title: 'Outcome', dataIndex: 'outcome', key: 'outcome', width: 90, render: (o) => <Tag color={outcomeColor(o)}>{o}</Tag> },
    { title: 'Exam Date', dataIndex: 'exam_date', key: 'exam_date', width: 100 },
    { title: 'Evidence', dataIndex: 'evidence_filename', key: 'evidence', width: 120, ellipsis: true,
      render: (f) => f ? <a className="text-blue-600 text-xs">{f}</a> : '-' },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900">Assessment Results</h2>
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

      <div className="bg-white rounded-lg border border-gray-200">
        <Table columns={columns} dataSource={results} rowKey="result_id" size="small"
          loading={loading} pagination={{ pageSize: 10 }} scroll={{ x: 600 }} />
      </div>

      <Modal title="Add Result" open={modalOpen} onOk={handleImport} onCancel={() => setModalOpen(false)}
        okText="Import" centered okButtonProps={{ style: { background: '#154BC7' } }}>
        <div className="space-y-3 mt-4">
          <Input placeholder="Registration ID *" value={form.reg_id} onChange={(e) => setForm({...form, reg_id: e.target.value})} />
          <InputNumber className="w-full" placeholder="Score" value={form.score}
            onChange={(v) => setForm({...form, score: v || 0})} min={0} max={100} />
          <Input type="date" value={form.exam_date} onChange={(e) => setForm({...form, exam_date: e.target.value})} />
        </div>
      </Modal>
    </div>
  )
}

export default AssessmentResults

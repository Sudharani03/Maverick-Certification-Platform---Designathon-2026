import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Input, Button, InputNumber, message } from 'antd'
import { RiArrowLeftLine } from 'react-icons/ri'
import { createDrive } from '../config/api/apiConfig.js'

const CreateDrive = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({
    name: '', sponsor: '', budget: 0, start_date: '', end_date: '',
    target_count: 50, policy_notes: '', pass_threshold: 70,
  })

  const handleSubmit = async () => {
    if (!form.name || !form.sponsor || !form.start_date || !form.end_date) {
      message.error('Please fill all required fields')
      return
    }
    try {
      setLoading(true)
      await createDrive(form)
      message.success('Drive created successfully')
      navigate('/drives')
    } catch (err) {
      message.error(err.response?.data?.message || 'Failed to create drive')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fade-in-up max-w-2xl">
      <button onClick={() => navigate('/drives')}
        className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-800 mb-4 transition-colors">
        <RiArrowLeftLine /> Back to Drives
      </button>

      <div className="bg-white rounded-xl border border-gray-100 p-7 hover-glow">
        <h1 className="text-lg font-bold text-gray-900 mb-1">Create New Drive</h1>
        <p className="text-xs text-gray-500 mb-6">Set up a new MAP certification drive</p>

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Drive Name *</label>
            <Input value={form.name} onChange={(e) => setForm({...form, name: e.target.value})}
              placeholder="e.g., AWS Solutions Architect - July 2026" size="large" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Sponsor *</label>
              <Input value={form.sponsor} onChange={(e) => setForm({...form, sponsor: e.target.value})}
                placeholder="L&D Team" size="large" />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Budget (₹)</label>
              <InputNumber className="w-full" value={form.budget} size="large"
                onChange={(v) => setForm({...form, budget: v || 0})} min={0} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Start Date *</label>
              <Input type="date" value={form.start_date} size="large"
                onChange={(e) => setForm({...form, start_date: e.target.value})} />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">End Date *</label>
              <Input type="date" value={form.end_date} size="large"
                onChange={(e) => setForm({...form, end_date: e.target.value})} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Target Candidates</label>
              <InputNumber className="w-full" value={form.target_count} size="large"
                onChange={(v) => setForm({...form, target_count: v || 0})} min={1} />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Pass Threshold (%)</label>
              <InputNumber className="w-full" value={form.pass_threshold} size="large"
                onChange={(v) => setForm({...form, pass_threshold: v || 70})} min={0} max={100} />
            </div>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Policy Notes</label>
            <Input.TextArea rows={3} value={form.policy_notes}
              onChange={(e) => setForm({...form, policy_notes: e.target.value})}
              placeholder="Max 2 attempts per year..." />
          </div>
          <Button type="primary" block loading={loading} onClick={handleSubmit}
            style={{ background: '#154BC7', height: '44px', fontWeight: 600, borderRadius: '8px', fontSize: '14px' }}>
            Create Drive
          </Button>
        </div>
      </div>
    </div>
  )
}

export default CreateDrive

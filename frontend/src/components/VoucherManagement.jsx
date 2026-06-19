import { useState, useEffect } from 'react'
import { Table, Tag, Button, Input, Modal, InputNumber, Tabs, message } from 'antd'
import { RiAddLine, RiRefreshLine, RiDeleteBinLine } from 'react-icons/ri'
import { getVouchers, addVoucherPool, autoAllocate, revokeVoucher, markRedeemed } from '../config/api/apiConfig.js'
import useDrive from '../utils/useDrive.js'

const VoucherManagement = () => {
  const [vouchers, setVouchers] = useState([])
  const [loading, setLoading] = useState(true)
  const [addModal, setAddModal] = useState(false)
  const [form, setForm] = useState({ vendor: '', value: 300, expiry_date: '', codes: '' })
  const drive = useDrive()

  useEffect(() => { if (drive?.drive_id) fetchData() }, [drive])

  const fetchData = async () => {
    try {
      setLoading(true)
      const res = await getVouchers(drive.drive_id)
      setVouchers(res.data || [])
    } catch (err) { message.error('Failed to fetch vouchers') }
    finally { setLoading(false) }
  }

  const handleAddPool = async () => {
    if (!form.vendor || !form.expiry_date || !form.codes.trim()) { message.error('Fill all fields'); return }
    const codes = form.codes.split('\n').map(c => c.trim()).filter(Boolean)
    try {
      await addVoucherPool({ drive_id: drive.drive_id, vendor: form.vendor, value: form.value, expiry_date: form.expiry_date, codes })
      message.success(`Added ${codes.length} vouchers`)
      setAddModal(false)
      setForm({ vendor: '', value: 300, expiry_date: '', codes: '' })
      fetchData()
    } catch (err) { message.error('Failed to add vouchers') }
  }

  const handleAutoAllocate = async () => {
    try {
      const res = await autoAllocate(drive.drive_id)
      message.success(res.message)
      fetchData()
    } catch (err) { message.error('Auto-allocate failed') }
  }

  const handleRevoke = async (voucherId) => {
    try {
      await revokeVoucher(voucherId)
      message.success('Voucher revoked')
      fetchData()
    } catch (err) { message.error('Revoke failed') }
  }

  const handleRedeem = async (voucherId) => {
    try {
      await markRedeemed(voucherId)
      message.success('Marked as redeemed')
      fetchData()
    } catch (err) { message.error('Failed') }
  }

  const statusColor = (s) => ({ available: 'blue', allocated: 'orange', redeemed: 'green', revoked: 'red', expired: 'default' }[s] || 'default')

  const poolVouchers = vouchers.filter(v => v.status === 'available')
  const allocatedVouchers = vouchers.filter(v => ['allocated', 'redeemed', 'revoked'].includes(v.status))

  const poolColumns = [
    { title: 'ID', dataIndex: 'voucher_id', key: 'id', width: 100, ellipsis: true },
    { title: 'Vendor', dataIndex: 'vendor', key: 'vendor', width: 80 },
    { title: 'Code', dataIndex: 'masked_code', key: 'code', width: 130 },
    { title: 'Value', dataIndex: 'value', key: 'value', width: 70, render: (v) => `₹${v}` },
    { title: 'Expiry', dataIndex: 'expiry_date', key: 'expiry', width: 100 },
    { title: 'Status', dataIndex: 'status', key: 'status', width: 90, render: (s) => <Tag color={statusColor(s)}>{s}</Tag> },
  ]

  const allocColumns = [
    { title: 'Code', dataIndex: 'masked_code', key: 'code', width: 130 },
    { title: 'Assigned To', dataIndex: 'assigned_to', key: 'assigned', width: 110, ellipsis: true },
    { title: 'Allocated', dataIndex: 'allocated_date', key: 'alloc', width: 100, render: (d) => d?.slice(0, 10) },
    { title: 'Status', dataIndex: 'status', key: 'status', width: 90, render: (s) => <Tag color={statusColor(s)}>{s}</Tag> },
    { title: 'Actions', key: 'actions', width: 150, render: (_, r) => (
      <div className="flex gap-1">
        {r.status === 'allocated' && (
          <>
            <Button size="small" onClick={() => handleRedeem(r.voucher_id)} style={{ fontSize: 10 }}>Redeem</Button>
            <Button size="small" danger onClick={() => handleRevoke(r.voucher_id)} style={{ fontSize: 10 }}>Revoke</Button>
          </>
        )}
      </div>
    )},
  ]

  const metrics = {
    total: vouchers.length,
    available: vouchers.filter(v => v.status === 'available').length,
    allocated: vouchers.filter(v => v.status === 'allocated').length,
    redeemed: vouchers.filter(v => v.status === 'redeemed').length,
  }

  const tabItems = [
    { key: 'pool', label: `Pool (${metrics.available})`, children: (
      <Table columns={poolColumns} dataSource={poolVouchers} rowKey="voucher_id" size="small" pagination={{ pageSize: 8 }} />
    )},
    { key: 'allocated', label: `Allocations (${metrics.allocated + metrics.redeemed})`, children: (
      <Table columns={allocColumns} dataSource={allocatedVouchers} rowKey="voucher_id" size="small" pagination={{ pageSize: 8 }} />
    )},
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900">Voucher Management</h2>
        <div className="flex gap-2">
          <Button icon={<RiRefreshLine />} size="small" onClick={handleAutoAllocate}
            style={{ background: '#059669', color: 'white', borderColor: '#059669' }}>Auto-Allocate</Button>
          <Button type="primary" icon={<RiAddLine />} size="small" onClick={() => setAddModal(true)}
            style={{ background: '#154BC7' }}>Add Vouchers</Button>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        {[{ l: 'Total', v: metrics.total, c: '#154BC7' }, { l: 'Available', v: metrics.available, c: '#0284C7' },
          { l: 'Allocated', v: metrics.allocated, c: '#D97706' }, { l: 'Redeemed', v: metrics.redeemed, c: '#059669' }]
          .map((m, i) => (
            <div key={i} className="bg-white rounded-lg border border-gray-200 p-3 text-center">
              <p className="text-xs text-gray-500">{m.l}</p>
              <p className="text-xl font-bold" style={{ color: m.c }}>{m.v}</p>
            </div>
        ))}
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-3">
        <Tabs items={tabItems} size="small" />
      </div>

      <Modal title="Add Vouchers to Pool" open={addModal} onOk={handleAddPool}
        onCancel={() => setAddModal(false)} okText="Add" centered okButtonProps={{ style: { background: '#154BC7' } }}>
        <div className="space-y-3 mt-4">
          <Input placeholder="Vendor (e.g., AWS)" value={form.vendor} onChange={(e) => setForm({...form, vendor: e.target.value})} />
          <InputNumber className="w-full" placeholder="Value" value={form.value} onChange={(v) => setForm({...form, value: v || 0})} />
          <Input type="date" placeholder="Expiry Date" value={form.expiry_date} onChange={(e) => setForm({...form, expiry_date: e.target.value})} />
          <Input.TextArea rows={5} placeholder="Voucher codes (one per line)" value={form.codes} onChange={(e) => setForm({...form, codes: e.target.value})} />
        </div>
      </Modal>
    </div>
  )
}

export default VoucherManagement

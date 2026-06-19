import { useState, useEffect } from 'react'
import { Table, Tag, Select, message } from 'antd'
import { getAuditLogs } from '../config/api/apiConfig.js'

const AuditLog = () => {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ entity: null, action: null })

  useEffect(() => { fetchData() }, [filters])

  const fetchData = async () => {
    try {
      setLoading(true)
      const params = {}
      if (filters.entity) params.entity = filters.entity
      if (filters.action) params.action = filters.action
      const res = await getAuditLogs(params)
      setLogs(res.data || [])
    } catch (err) { message.error('Failed to fetch audit logs') }
    finally { setLoading(false) }
  }

  const actionColor = (a) => ({
    created: 'blue', updated: 'orange', deleted: 'red', allocated: 'green',
    revoked: 'red', approved: 'green', rejected: 'red', evaluated: 'purple',
    status_updated: 'orange', pool_added: 'blue', redeemed: 'green', bulk_imported: 'cyan',
  }[a] || 'default')

  const columns = [
    { title: 'Timestamp', dataIndex: 'timestamp', key: 'ts', width: 150, render: (t) => t?.slice(0, 19).replace('T', ' ') },
    { title: 'Entity', dataIndex: 'entity', key: 'entity', width: 100, render: (e) => <Tag>{e}</Tag> },
    { title: 'Action', dataIndex: 'action', key: 'action', width: 110, render: (a) => <Tag color={actionColor(a)}>{a}</Tag> },
    { title: 'Actor', dataIndex: 'actor', key: 'actor', width: 90 },
    { title: 'Entity ID', dataIndex: 'entity_id', key: 'eid', width: 110, ellipsis: true },
  ]

  return (
    <div>
      <h2 className="text-lg font-bold text-gray-900 mb-4">Audit Log</h2>

      <div className="flex gap-3 mb-4">
        <Select placeholder="Filter Entity" allowClear style={{ width: 140 }} size="small"
          onChange={(v) => setFilters({...filters, entity: v})}
          options={['Drive', 'Registration', 'Eligibility', 'Result', 'Voucher'].map(e => ({ label: e, value: e }))} />
        <Select placeholder="Filter Action" allowClear style={{ width: 140 }} size="small"
          onChange={(v) => setFilters({...filters, action: v})}
          options={['created', 'updated', 'deleted', 'allocated', 'revoked', 'approved', 'rejected', 'evaluated'].map(a => ({ label: a, value: a }))} />
      </div>

      <div className="bg-white rounded-lg border border-gray-200">
        <Table columns={columns} dataSource={logs} rowKey="log_id" size="small"
          loading={loading} pagination={{ pageSize: 15 }}
          expandable={{
            expandedRowRender: (record) => (
              <div className="grid grid-cols-2 gap-4 p-2">
                <div>
                  <p className="text-xs font-semibold text-gray-500 mb-1">Before</p>
                  <pre className="text-[10px] bg-gray-50 p-2 rounded overflow-auto max-h-32">
                    {record.before ? JSON.stringify(record.before, null, 2) : 'null'}
                  </pre>
                </div>
                <div>
                  <p className="text-xs font-semibold text-gray-500 mb-1">After</p>
                  <pre className="text-[10px] bg-gray-50 p-2 rounded overflow-auto max-h-32">
                    {record.after ? JSON.stringify(record.after, null, 2) : 'null'}
                  </pre>
                </div>
              </div>
            ),
          }}
        />
      </div>
    </div>
  )
}

export default AuditLog

import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Layout from './layout/Layout.jsx'
import DrivesDashboard from './pages/DrivesDashboard.jsx'
import CreateDrive from './pages/CreateDrive.jsx'
import DriveDetails from './components/DriveDetails.jsx'
import Registrations from './components/Registrations.jsx'
import Eligibility from './components/Eligibility.jsx'
import AssessmentResults from './components/AssessmentResults.jsx'
import VoucherManagement from './components/VoucherManagement.jsx'
import Reports from './components/Reports.jsx'
import AuditLog from './components/AuditLog.jsx'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      {/* All pages after login use the Layout (TopBar + Sidebar) */}
      <Route element={<Layout />}>
        <Route path="/drives" element={<DrivesDashboard />} />
        <Route path="/create-drive" element={<CreateDrive />} />
        <Route path="/drive-details" element={<DriveDetails />} />
        <Route path="/registrations" element={<Registrations />} />
        <Route path="/eligibility" element={<Eligibility />} />
        <Route path="/assessment-results" element={<AssessmentResults />} />
        <Route path="/voucher-management" element={<VoucherManagement />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/audit-log" element={<AuditLog />} />
      </Route>
    </Routes>
  )
}

export default App

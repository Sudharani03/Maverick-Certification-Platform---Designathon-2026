import axios from 'axios'
import ApiUrls from './ApiUrls.jsx'

const BASE_URL = 'http://localhost:8016/api'

const API = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

const getUserId = () => {
  const user = JSON.parse(localStorage.getItem('auth_user') || '{}')
  return user.user_id || ''
}

// Auth
export const loginUser = async (role) => {
  const res = await API.post(ApiUrls.LOGIN, { role })
  return res.data
}

// Drives
export const getAllDrives = async () => {
  const res = await API.post(ApiUrls.GET_ALL_DRIVES)
  return res.data
}

export const createDrive = async (data) => {
  const res = await API.post(ApiUrls.CREATE_DRIVE, { ...data, user_id: getUserId() })
  return res.data
}

export const getDriveDetails = async (drive_id) => {
  const res = await API.post(ApiUrls.GET_DRIVE_DETAILS, { drive_id })
  return res.data
}

export const updateDrive = async (drive_id, updates) => {
  const res = await API.post(ApiUrls.UPDATE_DRIVE, { drive_id, user_id: getUserId(), ...updates })
  return res.data
}

export const closeDrive = async (drive_id) => {
  const res = await API.post(ApiUrls.CLOSE_DRIVE, { drive_id, user_id: getUserId() })
  return res.data
}

export const deleteDrive = async (drive_id) => {
  const res = await API.post(ApiUrls.DELETE_DRIVE, { drive_id, user_id: getUserId() })
  return res.data
}

// Registrations
export const registerCandidate = async (data) => {
  const res = await API.post(ApiUrls.REGISTER_CANDIDATE, { ...data, user_id: getUserId() })
  return res.data
}

export const getRegistrations = async (drive_id) => {
  const res = await API.post(ApiUrls.GET_REGISTRATIONS, { drive_id })
  return res.data
}

export const bulkImportRegistrations = async (drive_id, file) => {
  const formData = new FormData()
  formData.append('drive_id', drive_id)
  formData.append('user_id', getUserId())
  formData.append('file', file)
  const res = await API.post(ApiUrls.BULK_IMPORT_REGISTRATIONS, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

// Eligibility
export const evaluateEligibility = async (reg_id) => {
  const res = await API.post(ApiUrls.EVALUATE_ELIGIBILITY, { reg_id, user_id: getUserId() })
  return res.data
}

export const bulkEvaluate = async (drive_id) => {
  const res = await API.post(ApiUrls.BULK_EVALUATE, { drive_id, user_id: getUserId() })
  return res.data
}

export const approveCandidate = async (elig_id) => {
  const res = await API.post(ApiUrls.APPROVE_CANDIDATE, { elig_id, user_id: getUserId() })
  return res.data
}

export const rejectCandidate = async (elig_id, reason) => {
  const res = await API.post(ApiUrls.REJECT_CANDIDATE, { elig_id, user_id: getUserId(), reason })
  return res.data
}

export const getEligibility = async (drive_id) => {
  const res = await API.post(ApiUrls.GET_ELIGIBILITY, { drive_id })
  return res.data
}

// Results
export const importResult = async (data) => {
  const res = await API.post(ApiUrls.IMPORT_RESULT, { ...data, user_id: getUserId() })
  return res.data
}

export const bulkImportResults = async (drive_id, file) => {
  const formData = new FormData()
  formData.append('drive_id', drive_id)
  formData.append('user_id', getUserId())
  formData.append('file', file)
  const res = await API.post(ApiUrls.BULK_IMPORT_RESULTS, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

export const getResults = async (drive_id) => {
  const res = await API.post(ApiUrls.GET_RESULTS, { drive_id })
  return res.data
}

// Vouchers
export const addVoucherPool = async (data) => {
  const res = await API.post(ApiUrls.ADD_VOUCHER_POOL, { ...data, user_id: getUserId() })
  return res.data
}

export const allocateVoucher = async (reg_id) => {
  const res = await API.post(ApiUrls.ALLOCATE_VOUCHER, { reg_id, user_id: getUserId() })
  return res.data
}

export const autoAllocate = async (drive_id) => {
  const res = await API.post(ApiUrls.AUTO_ALLOCATE, { drive_id, user_id: getUserId() })
  return res.data
}

export const getVouchers = async (drive_id) => {
  const res = await API.post(ApiUrls.GET_VOUCHERS, { drive_id })
  return res.data
}

export const revokeVoucher = async (voucher_id) => {
  const res = await API.post(ApiUrls.REVOKE_VOUCHER, { voucher_id, user_id: getUserId() })
  return res.data
}

export const reissueVoucher = async (reg_id) => {
  const res = await API.post(ApiUrls.REISSUE_VOUCHER, { reg_id, user_id: getUserId() })
  return res.data
}

export const markRedeemed = async (voucher_id) => {
  const res = await API.post(ApiUrls.MARK_REDEEMED, { voucher_id, user_id: getUserId() })
  return res.data
}

export const getExpiringVouchers = async (days = 30) => {
  const res = await API.post(ApiUrls.GET_EXPIRING, { days })
  return res.data
}

// Reports
export const getDriveSummary = async (drive_id) => {
  const res = await API.post(ApiUrls.DRIVE_SUMMARY, { drive_id })
  return res.data
}

export const getFunnelData = async (drive_id) => {
  const res = await API.post(ApiUrls.FUNNEL_DATA, { drive_id })
  return res.data
}

export const getPassFailTrends = async (drive_id) => {
  const res = await API.post(ApiUrls.PASS_FAIL_TRENDS, { drive_id })
  return res.data
}

export const getVoucherUtilization = async (drive_id) => {
  const res = await API.post(ApiUrls.VOUCHER_UTILIZATION, { drive_id })
  return res.data
}

export const getOverallStats = async () => {
  const res = await API.post(ApiUrls.OVERALL_STATS)
  return res.data
}

// Audit
export const getAuditLogs = async (filters = {}) => {
  const res = await API.post(ApiUrls.GET_AUDIT_LOGS, filters)
  return res.data
}

// Communications
export const getCommunications = async (reg_id) => {
  const res = await API.post(ApiUrls.GET_COMMUNICATIONS, { reg_id })
  return res.data
}

export default API

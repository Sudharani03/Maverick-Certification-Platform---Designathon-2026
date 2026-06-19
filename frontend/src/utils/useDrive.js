import { useState, useEffect } from 'react'
import { getAllDrives } from '../config/api/apiConfig.js'

/**
 * Hook to get the currently selected drive.
 * If none is selected in localStorage, auto-fetches all drives 
 * and selects the first one. Always returns a drive object or null.
 */
const useDrive = () => {
  const [drive, setDrive] = useState(null)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    // Try reading from localStorage first
    const stored = localStorage.getItem('selected_drive')
    if (stored) {
      try {
        const parsed = JSON.parse(stored)
        if (parsed && parsed.drive_id) {
          setDrive(parsed)
          setLoaded(true)
          return
        }
      } catch (e) {
        // corrupted localStorage, ignore
      }
    }

    // No drive in localStorage — fetch from API and auto-select first
    getAllDrives()
      .then(res => {
        const drives = res.data || []
        if (drives.length > 0) {
          localStorage.setItem('selected_drive', JSON.stringify(drives[0]))
          setDrive(drives[0])
        }
      })
      .catch(() => {})
      .finally(() => setLoaded(true))
  }, [])

  return drive
}

export default useDrive

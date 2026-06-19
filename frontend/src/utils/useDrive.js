import { useState, useEffect } from 'react'
import { getAllDrives } from '../config/api/apiConfig.js'

/**
 * Hook to get the currently selected drive.
 * If none is selected, auto-selects the first available drive.
 */
const useDrive = () => {
  const [drive, setDrive] = useState(() => {
    const stored = localStorage.getItem('selected_drive')
    return stored ? JSON.parse(stored) : null
  })

  useEffect(() => {
    if (!drive) {
      getAllDrives().then(res => {
        const drives = res.data || []
        if (drives.length > 0) {
          localStorage.setItem('selected_drive', JSON.stringify(drives[0]))
          setDrive(drives[0])
        }
      }).catch(() => {})
    }
  }, [])

  return drive
}

export default useDrive

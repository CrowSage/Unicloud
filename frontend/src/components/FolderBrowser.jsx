import { useEffect, useState } from "react"
import { useAuth } from "../context/AuthContext"

export default function FolderBrowser({ selectedAccount, serviceName }) {

  // Loading Context
  const { apiRequest } = useAuth()

  // States
  const [files, setFiles] = useState([])


  // UseEffect
  useEffect(() => {
    fetchFiles()

  }, [selectedAccount])

  // Functions
  async function fetchFiles(path = "root") {
    const response = await apiRequest(`services/${serviceName}/files/?account_id=${selectedAccount}&path=${path}`)
    if (response.ok) {
      const data = await response.json()
      setFiles(data)
    }
  }



  // MOSTLY HTML RETURN...

  return (
    <div className="filesContainer">
      {files.map((file) => (
        <span className="file" key={file.id} onClick={() => { fetchFiles(file?.path_display || file.id) }}>

          <span>{file.name}</span>
          <span>{file?.mimeType}</span>

        </span>
      ))}
    </div>
  )
}

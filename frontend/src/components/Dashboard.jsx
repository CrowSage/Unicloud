import AccountsList from "./AccountsList"
import FolderBrowser from "./FolderBrowser"

import { useAuth } from "../context/AuthContext"
import { useState } from "react"


export default function Dashboard() {

  // States
  const [selectedAccount, setSelectedAccount] = useState("")
  const [serviceName, setServiceName] = useState("")

  // Functions
  function onSelect(account_id, serviceName) {
    setSelectedAccount(account_id)
    setServiceName(serviceName)
  }



  return (
    <>
      <AccountsList selectedAccount={selectedAccount} onSelect={onSelect} />
      {selectedAccount && <FolderBrowser selectedAccount={selectedAccount} serviceName={serviceName} />}
    </>
  )

}

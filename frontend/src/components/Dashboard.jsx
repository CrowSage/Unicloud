import AccountsList from "./AccountsList"
import { useAuth } from "../context/AuthContext"
import { useState } from "react"


export default function Dashboard() {

  // States
  const [selectedAccount, setSelectedAccount] = useState("")


  // Functions
  function onSelect(account_id) {
    setSelectedAccount(account_id)
  }



  return (
    <AccountsList selectedAccount={selectedAccount} onSelect={onSelect} />
  )

}

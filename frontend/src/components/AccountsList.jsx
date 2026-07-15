import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext"

export default function AccountsList({ onSelect, selectedAccount }) {

  // Loading Context
  const { user, apiRequest } = useAuth()

  // States
  const [userAccounts, setUserAccounts] = useState([])

  // UseEffects
  useEffect(() => {

    async function fetchAccounts() {

      const response = await apiRequest("services/list/", { method: "GET" })
      const data = await response.json()
      setUserAccounts(data.services)

    }

    fetchAccounts()
  }, [])


  return (
    <ul className="accountList">{userAccounts.map((acc) => (

      <li className={selectedAccount == acc.account_id ? "selected accountItem" : "accountItem"} key={acc.account_id} onClick={() => { onSelect(acc.account_id) }}>
        <span>{acc.name}</span><br />
        <span>{acc.account_id}</span>
        <hr />
      </li>
    ))}</ul>
  );
}

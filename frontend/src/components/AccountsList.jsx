import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext"
import { API_URL } from "../config";

export default function AccountsList() {

  // Loading Context
  const { user } = useAuth()

  // States
  const [userAccounts, setUserAccounts] = useState([])

  // UseEffects
  useEffect(() => {

    async function fetchAccounts() {

      const response = await fetch(`${API_URL}/services/list/`, {
        method: "GET",
        headers: `Bearer ${userAccounts.accessToken}`
      })

      const data = await response.json()
      setUserAccounts(data.services)


    }


  })


  return <h1>Accounts List</h1>;
}

import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";






export default function Login() {

  // Navigation
  const navigate = useNavigate()

  // Loading Context
  const { login } = useAuth()

  // States
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  // Functions
  async function handleSubmit(e) {
    e.preventDefault()
    const response = await login(username, password)

    if (response.success) {
      navigate("/dashboard")
    } else {
      console.log(response)
      console.log("FUCK YOU!")
    }


  }
  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Login</button>
    </form>
  )
}

import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";






export default function Login() {

  // Navigation
  const navigate = useNavigate()

  // Loading Context
  const { login } = useAuth()

  // States
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  // Error States
  const [usernameError, setUsernameError] = useState("")
  const [passwordError, setPasswordError] = useState("")


  // Variables
  const error = usernameError || passwordError;


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
    <div className="authFormContainer">
      <h1>Login</h1>
      <span className="subHeading">Continue unifying your storage into one.</span>
      <form className="authForm" onSubmit={handleSubmit}>

        {error && <span className="inputError">{error}</span>}

        <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className={usernameError ? "wrongInput" : ""} />

        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className={passwordError ? "wrongInput" : ""} />

        <span className="authLink">Don't have an account? <Link to={"/register"} className="link">Register</Link> instead.</span>
        <button type="submit">Login</button>

      </form>
    </div>
  )
}

import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {


  // Navigation
  const navigate = useNavigate()

  // Context
  const { register } = useAuth()

  // Form States
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  // Form Error States
  const [usernameError, setUsernameError] = useState("")
  const [passwordError, setPasswordError] = useState("")
  const [confirmPasswordError, setConfirmPasswordError] = useState("")

  // Variables
  const error = usernameError || passwordError || confirmPasswordError;

  // Functions
  async function handleSubmit(e) {

    e.preventDefault()

    setUsernameError("")
    setPasswordError("")
    setConfirmPasswordError("")

    let hasErrors = false

    if (username.length < 3) {
      setUsernameError("Username must contain at least 3 characters.")
      hasErrors = true
    }
    if (password.length < 8) {
      setPasswordError("Password must contain at least 8 characters.")
      hasErrors = true
    }
    if (password !== confirmPassword) {
      setConfirmPasswordError("Passwords don't match.")
      hasErrors = true
    }

    if (hasErrors) return
    const response = await register(username, password)

    if (response.ok) {
      navigate("/login")
    }

  }


  return (

    <div className="authFormContainer">
      <h1>Register</h1>
      <span className="subHeading">Start unifying your storage into one.</span>
      <form className="authForm" onSubmit={handleSubmit}>

        {error && <span className="inputError">{error}</span>}

        <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className={usernameError ? "wrongInput" : ""} />

        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className={passwordError ? "wrongInput" : ""} />

        <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className={confirmPasswordError ? "wrongInput" : ""} />
        <span className="authLink">Already have an account? <Link to={"/login"} className="link">Login</Link> instead.</span>
        <button type="submit">Register</button>

      </form>
    </div>

  );
}

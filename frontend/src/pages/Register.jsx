import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function Register() {

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

  // Functions
  async function handleSubmit(e){

    e.preventDefault()

    setUsernameError("")
    setPasswordError("")
    setConfirmPassword("")

    let hasErrors = false

    if(username.length < 3){
      setUsernameError("Username must contain at least 3 characters.")
      hasErrors=true
    }
    if(password.length < 8){
      setPasswordError("Password must contain at least 8 characters.")
      hasErrors=true
    }
    if(password !== confirmPassword){
      setConfirmPasswordError("Password Don't Match.")
      hasErrors=true
    }

    if(hasErrors) return
    const response = await register(username, password)

  }


  return (

    <div className="authFormContainer">
      <h1>Register</h1>
      <span style={{fontSize:"16px", color:"gray", marginTop: "16px"}}>Become a part of our kingdom.</span>
      <form className="authForm" onSubmit={handleSubmit}>

      <input type="text" placeholder="Username" value={username} onChange={(e)=>setUsername(e.target.value)}/>
      <span className="inputError">{usernameError}</span>

      <input type="password" placeholder="Password" value={password} onChange={(e)=>setPassword(e.target.value)}/>
      <span className="inputError">{passwordError}</span>

      <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e)=>setConfirmPassword(e.target.value)}/>
      <span className="inputError">{confirmPasswordError}</span>

      <button type="submit">Register</button>

      </form>
    </div>

  );
}

import { createContext, useContext, useState } from "react";
import { API_URL } from "../config";

export const AuthContext = createContext()


export function AuthProvider({ children }) {

    const [user, setUser] = useState(() => {
        const storedUser = localStorage.getItem("userObject");
        return storedUser ? JSON.parse(storedUser) : null;
    })


    // REGISTRATION FUNCTION
    async function register(username, password) {

        const response = await fetch(`${API_URL}/accounts/register/`, {

            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })

        })

        if (!response.ok) {
            return {
                success: false,
                errors: await response.json()
            }
        }
        return {
            success: true
        }
    }


    // LOGIN FUNCTION
    async function login(username, password) {

        const response = await fetch(`${API_URL}/accounts/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        })

        if (!response.ok) {
            return {
                success: false,
                errors: await response.json()
            }
        }


        const data = await response.json()
        const userObj = {
            "username": username,
            "accessToken": data.access,
            "refreshToken": data.refresh
        }

        localStorage.setItem("userObject", JSON.stringify(userObj))
        setUser(userObj)
        return { success: true }

    }

    // LOGOUT FUNCTION
    function logout() {
        setUser(null)
        localStorage.removeItem("userObject")
    }



    return (
        <AuthContext.Provider value={{ register, login, logout, user }}>
            {children}
        </AuthContext.Provider>
    )
}


export function useAuth() {
    return useContext(AuthContext)
}
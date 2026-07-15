import { createContext, useContext, useState } from "react";
import { API_URL } from "../config";
import { configs } from "eslint-plugin-react-hooks";

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

        const response = await fetch(`${API_URL}/accounts/token/`, {
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


    // This Function Refresh AccessToken Using refreshToken otherwise logsout
    async function tokenRefresher() {

        const response = await fetch(`${API_URL}/accounts/token/refresh/`, {

            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "refresh": user.refreshToken })

        })

        if (response.ok) {

            const data = await response.json()

            const updatedUser = {
                ...user,
                accessToken: data.access,
            }

            setUser(updatedUser)
            localStorage.setItem("userObject", JSON.stringify(updatedUser))

            return {
                success: true,
                access: data.access
            }
        }

        return {
            success: false
        }
    }


    // API_Request Function
    async function apiRequest(endpoint, options = {}) {

        const config = {
            ...options,
            headers: {
                ...options.headers || {},
                "Authorization": `Bearer ${user.accessToken}`
            }
        }

        const response = await fetch(`${API_URL}/${endpoint}`, config)


        // Return if access token was valid
        if (response.status !== 401) {
            return response
        }

        // Getting a new access token and retrying otherwise
        const refreshed = await tokenRefresher()



        if (!refreshed.success) {
            logout()
            return
        }

        const retryConfig = {
            ...options,
            headers: {
                ...options.headers || {},
                "Authorization": `Bearer ${refreshed.access}`
            }
        }

        const newResponse = await fetch(`${API_URL}/${endpoint}`, retryConfig)

        if (newResponse.status === 401) {

            logout()
            return

        }

        return newResponse
    }


    return (
        <AuthContext.Provider value={{ register, login, logout, user, apiRequest }}>
            {children}
        </AuthContext.Provider>
    )
}


export function useAuth() {
    return useContext(AuthContext)
}
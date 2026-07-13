import { createContext, useContext } from "react";
import { API_URL } from "../config";

export const AuthContext = createContext()


export function AuthProvider({children}){


    // REGISTRATION FUNCTION
    async function register(username, password){
        
        const response = await fetch(`${API_URL}/accounts/register/`, {
        
            method:"POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        
        })

        if(!response.ok){
            return {
                success: false,
                errors: await response.json()}
        }
        return {
            success:true
        }
    }


    // LOGIN FUNCTION
    function login(username, password){
        
    }
    // LOGOUT FUNCTION
    function logout(){}



    return(
        <AuthContext.Provider value={{register}}>
            {children}
        </AuthContext.Provider>
    )
}


export function useAuth() {
    return useContext(AuthContext)
}
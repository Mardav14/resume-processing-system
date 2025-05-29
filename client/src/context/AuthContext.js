import {createContext, useState, useEffect} from 'react'
import {jwtDecode} from 'jwt-decode'
import {useNavigate} from 'react-router-dom'

const AuthContext = createContext()

export default AuthContext

export const AuthProvider = ({children}) => {
    
    let [authTokens, setAuthTokens] = useState(()=>localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')):null)
    let [user, setUser] = useState(()=>localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')):null)
    let [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    let loginUser = async (e)=>{
        e.preventDefault()
        let response = await fetch("http://127.0.0.1:8000/api/token/", {
            method : "POST",
            headers : {
                "Content-Type": "application/json" 
            },
            body : JSON.stringify({'username': e.target.username.value, 'password':e.target.password.value,}),

        })
        let data = await response.json()
        if(response.status === 200){
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem("authTokens", JSON.stringify(data))
            if(jwtDecode(data.access).is_hr){
                navigate('/hr-dashboard')
            }
            else{
                navigate('/user')
            }
        }
        else{
            alert("Something went wrong")
        }
        
    }
    let logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem("authTokens")
        navigate('/')
    }

    let UpdateToken = async ()=>{
        let response = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
            method : "POST",
            headers : {
                "Content-Type": "application/json" 
            },
            body : JSON.stringify({'refresh': authTokens?.refresh}),

        })
        let data = await response.json()
        if(response.status === 200){
            data.refresh = authTokens.refresh
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem("authTokens", JSON.stringify(data))
        }
        else{
           logoutUser()
        }
        if(loading){
            setLoading(false)
        }
    }

    let register = async (e, role) => {
        e.preventDefault();
        let formData = new FormData();
      
        formData.append('username', e.target.username.value);
        formData.append('password', e.target.password.value);
        console.log(role)
        if(role == 'hr'){
            formData.append('is_hr', true);
        }
        // Handle resume upload (assuming it's a file input)
        const resumeFile = e.target.resume.files[0];
        if (resumeFile) {
          formData.append('resume', resumeFile);

        }

        if(role != 'hr'){
            let response = await fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            body: formData
            });
            let data = await response.json();

            if (response.status === 201) {
          alert("account created!");
          navigate('login/')
        } else {
          alert("Something went wrong");
        }

        }
        else{
            let response = await fetch("http://127.0.0.1:8000/api/registerHr/", {
            method: "POST",
            body: formData
            });
            let data = await response.json();

            if (response.status === 201) {
            alert("account created!");
            navigate('login/')
            } else {
            alert("Something went wrong");
            }
        }
      
      
        
      };
      

    let contextData = {
        user : user,
        authTokens : authTokens,
        loginUser : loginUser,
        logoutUser : logoutUser,
        register : register
    }

    useEffect(()=>{
    if(loading){
        UpdateToken()
    }

        let fourMin = 1000 * 60 * 4 
        let interval = setInterval(()=>{
            if(authTokens){
                UpdateToken()
            }
        },fourMin)
        return ()=>clearInterval(interval)
    }, [authTokens, loading])

    return(
        <AuthContext.Provider value = {contextData} >
            {loading? null : children}
        </AuthContext.Provider>
    )
}
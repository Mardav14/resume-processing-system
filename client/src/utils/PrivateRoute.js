import {Navigate} from 'react-router-dom'
import { useContext} from 'react'
import React from 'react'
import AuthContext from '../context/AuthContext'

const PrivateRoute = ({children, ...rest}) => {
  let {user} = useContext(AuthContext)
  return user?  children: <Navigate to='/login' replace></Navigate>
}

export default PrivateRoute

import React, {useContext} from 'react'
import AuthContext from '../context/AuthContext'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const LoginPage = () => {
  let {loginUser} = useContext(AuthContext)
  return (
  
    <div className='container py-5' style={{width: "50%"}}>
    <Form onSubmit={loginUser}>
      <br/><br/>
    <Form.Group className="mb-3" controlId="formBasicUserName">
        <Form.Label><div className='baseText'>Username</div> </Form.Label>
        <Form.Control type="text" placeholder="Enter username" name = "username" />
       </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label><div className='baseText'>Password</div></Form.Label>
        <Form.Control type="password" placeholder="Password" name = "password"/>
      </Form.Group>
      
      <Button variant="primary" type="submit">
        Login
      </Button>
    </Form>
    </div>
      
 
  )
}

export default LoginPage

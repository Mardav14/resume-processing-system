import React, {useContext, useState} from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import AuthContext from '../context/AuthContext';
import { useParams } from 'react-router-dom'

const Register = () => {
  const params = useParams()
  const [role, setRole] = useState(params.role)
  const [filename, setFilename] = useState('')
  const {register} = useContext(AuthContext)
  return (
    <div className='container py-5' style={{width: "50%"}}>
    <Form onSubmit={(e)=>register(e, role)}>
      <br/><br/>
    <Form.Group className="mb-3" controlId="formBasicUserName">
        <Form.Label><div className='baseText'>Username</div></Form.Label>
        <Form.Control type="text" placeholder="Enter username" name = "username" />
       
    </Form.Group>
        
      <div className="form-group mb-3" style={{ display: role === 'hr' ? 'none' : 'block' }}>
      <label htmlFor="exampleFormControlFile1" className="baseText mb-2">Upload Resume</label>
      <input type="file" onChange={e => setFilename(e.target.files[0])} className="form-control" name="resume" />
      </div>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label><div className='baseText'>Password</div></Form.Label>
        <Form.Control type="password" placeholder="Password" name = "password"/>
      </Form.Group>
      
      <Button variant="primary" type="submit">
        Register
      </Button>
    </Form>
    </div>

  )
}

export default Register

import React from 'react'
import {Link} from 'react-router-dom'
//bootstrap imports
import Button  from 'react-bootstrap/Button';

const SelectRole = () => {
  return (
    
    <div style={{"display": "flex","justifyContent": "center", alignItems:"center"}}>
      
     <Link to='/register/hr'> <Button  className='RoleButton' variant="outline-light"><h2 className='signUpText' style={{boxWidth:"300px"}}>I Am Hiring</h2></Button></Link>
     <Link to='/register/candidate'> <Button  className='RoleButton' variant="outline-light"><h2 className='signUpText'>I Am looking for a Job</h2></Button></Link>
      </div>
  )
}

export default SelectRole

import React from 'react'
import AuthContext from '../context/AuthContext'
import { useEffect, useState, useContext } from 'react'
//bootstrap imports
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';


const HomePage = () => {
  let {user} = useContext(AuthContext)
  let [details, setDetails] = useState()
  let getDetails = async ()=>{

    let response = await fetch(`http://127.0.0.1:8000/api/candidate/${user.username}`, {
        method : "GET",
        headers : {
          "Content-Type": "application/json" 
      },
     
        })
    let data = await response.json() 
    setDetails(data)
    }

  useEffect(()=>{
    getDetails()
   
  }, [])
  
  return (
    <>
    <br/><br/><br/><br/>
    
    {details && 
    (<Card style={{ width: '75%', float: "left", marginLeft: "12%", marginTop: "40px", paddingTop:"1%",paddingBottom:"2%", }}>
      <Card.Body>
        <Card.Title>{details.full_name || 'Unnamed Candidate'}</Card.Title>
        <Card.Text>
          <strong>Email:</strong> {details.email || 'N/A'}<br />
          <strong>Phone:</strong> {details.phone || 'N/A'}<br />
          <strong>Years of Experience:</strong> {details.years_experience || 'N/A'}<br />
          <strong>Location:</strong> {details.location || 'N/A'}
        </Card.Text>
      </Card.Body>

      <ListGroup className="list-group-flush">
        <ListGroup.Item>
          <strong>Skills:</strong><br />
          {details.skills?.length > 0
            ? details.skills.join(', ')
            : 'N/A'}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Education:</strong><br />
          {details.education_list?.length > 0
            ? details.education_list.join(', ')
            : 'N/A'}
        </ListGroup.Item>
      </ListGroup>
    </Card>)
    }
    </>
  );
  
    
}

export default HomePage
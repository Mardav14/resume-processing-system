import React from 'react'
import image from "../../src/pages/img.jpg";
import { Footer } from '../components/Footer';
import {Link} from 'react-router-dom'
//bootstrap imports
import Button  from 'react-bootstrap/Button';


const OnBoarding = () => {
  
  return (
    <>
    <div>
      <h1 className='mainText'>MyATS:<br/><span style={{letterSpacing:"15px"}}> AI to Parse and Shortlist Resumes</span></h1>
      <div style={{"display": "flex","justifyContent": "center"}}>
     <Link to='/login'> <Button  className='signUpButton' variant="outline-light"><h2 className='signUpText'>Login</h2></Button></Link>
     <Link to='/select-role'> <Button  className='signUpButton' variant="outline-light"><h2 className='signUpText'>Sign Up</h2></Button></Link>
      </div>
      <img className='mainImg' src = {image}  alt="mainImg" width = "100%" />
      <br/><br/><br/>
    </div>
    <div className='mainFrame'>
      <div className='infoText'>
      <b>Welcome to MyATS,</b> This AI-powered resume parser and candidate shortlisting tool streamlines the hiring process by automatically extracting relevant details like skills, education, and experience from resumes. It intelligently compares candidate profiles against specified job requirements using natural language processing and similarity scoring to rank and shortlist the most suitable applicants. The tool enables recruiters to efficiently evaluate candidates with data-driven insights and download resumes directly through the interface.
    </div>
    </div>
    <br /><br/><br /><br/>
    <Footer />
    </>
  )
}

export default OnBoarding

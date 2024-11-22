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
      <h1 className='mainText'>INTER BOT:<br/><span style={{letterSpacing:"15px"}}> AI Bot to Conduct Interviews</span></h1>
      <div style={{"display": "flex","justifyContent": "center"}}>
     <Link to='/login'> <Button  className='signUpButton' variant="outline-light"><h2 className='signUpText'>Login</h2></Button></Link>
     <Link to='/select-role'> <Button  className='signUpButton' variant="outline-light"><h2 className='signUpText'>Sign Up</h2></Button></Link>
      </div>
      <img className='mainImg' src = {image}  alt="mainImg" width = "100%" />
      <br/><br/><br/>
    </div>
    <div className='mainFrame'>
      <div className='infoText'>
      <b>Welcome to InterBot,</b> your intelligent interview assistant. Designed to streamline the interview process, InterBot leverages advanced AI technology to conduct efficient and insightful interviews, ensuring you find the best candidates quickly and effectively. Whether you're hiring for technical roles or assessing soft skills, InterBot provides a consistent and unbiased interview experience, saving you time and enhancing your recruitment strategy. Experience the future of interviewing with InterBot.
    </div>
    </div>
    <br /><br/><br /><br/>
    <Footer />
    </>
  )
}

export default OnBoarding

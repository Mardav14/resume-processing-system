import React from 'react'
import { useState, useEffect } from 'react'
function QuizResult(props) {
  let [expScore, setExpScore] = useState(0)
  let [skillScore, setSkillScore] = useState(0)
  let [greetingScore, setGreetingScore] = useState(0)
  let [totalScore, setTotalScore] = useState(0)

  
  
  let getScore = async ()=>{
   
    let response = await fetch("http://127.0.0.1:8000/api/get-score", {
        method : "POST",
        headers : {
            "Content-Type": "application/json" 
        },
        body : JSON.stringify({'username': props.username, 'questions': props.questions, 'answers': props.allAnswers, 'url': props.url}),

    })
    console.log(props.allAnswers)
    let data = await response.json()
    if(response.status === 200){
        setGreetingScore((data[0]+ data[1])*10)
        setSkillScore((data[2]+ data[3]+ data[4])*10)
        setExpScore((data[5]+ data[6]+ data[7])*10)
        
        setTotalScore((data[0]+ data[1]+data[2]+ data[3]+ data[4]+data[5]+ data[6]+ data[7])*10)
    }
    else{
        alert("Something went wrong")
    }
    
}
  
  useEffect(()=>{
    getScore();
  }, [])
  return (
    <div className='containerQuiz' style={{width: "50%"}}>
    <h1 className='baseText'>RESULT</h1>
    <div className='show-score'>
      <table>
      <tr>
      <th style={{textAlign:"left"}}>Your Score: </th>
      <td style={{textAlign:"right"}}>{totalScore}/80</td>
      </tr>
      <tr>
      <th style={{textAlign:"left"}}>Professionalism Score: </th>
      <td style={{textAlign:"right"}}>{greetingScore}/20</td>
      </tr>
      <tr>
      <th style={{textAlign:"left"}}>Skill Score:</th>
      <td style={{textAlign:"right"}}>{skillScore}/30</td>
      </tr>
      <tr>
      <th style={{textAlign:"left"}}>Experience Score:</th>
      <td style={{textAlign:"right"}}>{expScore}/30</td>
      </tr>
      </table>
        <br/>
         
    </div>
    
    </div>
  )
}

export default QuizResult
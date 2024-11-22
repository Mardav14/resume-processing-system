import React, { useState, useEffect, useRef, useContext } from 'react'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import AuthContext from '../context/AuthContext'
import { useParams } from 'react-router-dom'
import QuizResult from './QuizResult';
import './Quiz.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form'
import webgazer from "webgazer"

const Quiz = () => {
    let {user} = useContext(AuthContext)
    const params = useParams()
    const title = params.title
    const [quizData, setQuizData] = useState()
    const [heading, setHeading] = useState()
    const [currentQuestion,setCurrentQuestion]=useState();
    const [showResult,setShowResult]=useState(false);
    const [timer, setTimer] = useState()
    const [displayTime, setDisplayTime] = useState("")
    const [allAnswers, setAllAnswers] = useState([])
    const ref = useRef()
    const [gazeData, setGazeData] = useState([]);
    const [averageGaze, setAverageGaze] = useState(0)
    const videoRef = useRef(null);

    const startWebcam = async () => {
        if (navigator.mediaDevices.getUserMedia && videoRef.current) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                    videoRef.current.style.display = 'block';
                }
            } catch (error) {
                console.error("Error accessing webcam", error);
            }
        } else {
            console.log("getUserMedia not supported!");
        }
    };

    // useEffect(() => {
    //     if(showResult == false){
    //     webgazer.setGazeListener((data) => {
    //         if (data) {
    //           setGazeData((prevData) => [...prevData, { x: data.x, y: data.y }]);
    //           console.log(data)
    //         }
    //       })
    //       .showVideo(false)
    //       .begin()
    //     }

    // return ()=>{
    //     webgazer.end()
    // }
    
    //   }, []); // Re-run effect if gazeData changes

      const calculateAverage = () => {
        if (gazeData.length === 0) {
          console.log('No gaze data available yet.');
          return;
        }
  
        const total = gazeData.reduce(
          (acc, point) => ({
            x: acc.x + point.x,
            y: acc.y + point.y,
          }),
          { x: 0, y: 0 }
        );
  
        const average = {
          x: total.x / gazeData.length,
          y: total.y / gazeData.length,
        };
        console.log(average)
        setAverageGaze(average)
      };

//fetch questions from backend
    let getQuestions = async ()=>{
        let response = await fetch("http://127.0.0.1:8000/api/questions", {
            method : "POST",
            headers : {
                "Content-Type": "application/json" 
            },
            body : JSON.stringify({'url': title, 'username': user.username}),

        })
        let data = await response.json()
        if(response.status === 200){
            
            // const questions = data.map(item => item.questions).flat()
            setQuizData(data.questions);
            setHeading(data.position)
            setTimer(data.duration)
            setCurrentQuestion(0)
            console.log(data.duration)
                      
                      
        }
        else{
            alert("Something went wrong")
        }
        
    }

  //speech to text  
    const startListening = () => SpeechRecognition.startListening({ continuous: true, language: 'en-IN' });
    const { transcript, resetTranscript } = useSpeechRecognition();
   
//text to speech
    useEffect(() => {
        // Ensure the current question exists before speaking
        if (quizData && quizData[currentQuestion]) {
          speakQuestion(quizData[currentQuestion]);
        }
      }, [currentQuestion]);

      

    
        const speakQuestion = (text, delay = 500) => {
            if (!text) return; // Ensure text is valid
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.5; // Set speech rate
          
            // Delay before speaking
            setTimeout(() => {
              window.speechSynthesis.speak(utterance);
            }, delay);
          };

//clock
    
    const getTimeRemaining = (e)=>{
        const total = Date.parse(e) - Date.parse(new Date())
        const hours = Math.floor((total / 1000 / 60 / 60) % 24)
        const minutes = Math.floor((total / 1000 / 60) % 60)
        const seconds = Math.floor((total / 1000) % 60)
        return {total, hours, minutes, seconds}
    }
    
    function startTimer(e){
        let{total, hours, minutes, seconds} = getTimeRemaining(e)
        if(total >= 0){
            setDisplayTime(
                (hours > 9 ? hours : "0" + hours)+ ":"+
                (minutes > 9 ? minutes : "0" + minutes)+ ":"+
                (seconds > 9 ? seconds : "0" + seconds)
    
            )
        }
        else{
            calculateAverage()
            setShowResult(true)
        }
    }
    const clearTimer = (e)=>{
        
        if(ref.current) clearInterval(ref.current)
            const id = setInterval(()=>{
                startTimer(e)
            }, 1000)
            ref.current = id;
        
    }
    const getSeconds = (timer)=>{
        let arr = timer.split(":")
        let arr_int = []
        let i = 0;
        arr.forEach((e)=>{
            arr_int[i] = parseInt(e)
            i++
        })
        return arr_int
    }
    const getDeadTime = ()=>{
        let deadline = new Date();
        let [hours,minutes, seconds] = getSeconds(timer)
        deadline.setSeconds(deadline.getSeconds() + seconds)
        deadline.setMinutes(deadline.getMinutes() + minutes)
        deadline.setHours(deadline.getHours() + hours)
        
        return deadline;
    }
    
    useEffect(()=>{
        startWebcam()
        getQuestions()
    }, [])
    useEffect(()=>{
        if(timer)
            clearTimer(getDeadTime())
    }, [timer])
    
//Quiz code
    
const changeQuestion = (e, i)=>{
    e.preventDefault()
    if(i< quizData.length-1){
        setCurrentQuestion(i+1);
          
        let newAllAnswers = [...allAnswers, transcript]
        setAllAnswers(newAllAnswers)
        console.log(allAnswers)
        resetTranscript()
        
            
        }
    else{
        let newAllAnswers = [...allAnswers, e.target.answer.value]
        setAllAnswers(newAllAnswers)
        console.log(allAnswers)
        calculateAverage()
        setShowResult(true)
    }
    }
    

    const resetAll=()=>{
        setShowResult(false);
        setCurrentQuestion(0);
        setAllAnswers([])
        setDisplayTime("")
        clearTimer(getDeadTime())
    }
  return (
   
    <div className='quizBody'>
         <br/><br/><br/><br/>
        
            {showResult ? (
                <QuizResult tryAgain={resetAll} allAnswers = {allAnswers} questions={quizData} username = {user.username} url={title}/>
            ):(
            <>
            <div className="containerQuiz mt-5">
            <h1 className='baseText'>{heading}</h1>
            <div className='p-20' >
            <br/><h3 className='baseText' style={{position: "relative", left:"500px", top:"-70px"}}>{displayTime}</h3>
      </div>
      
            {quizData? ( <div className = "question">
                <div style={{display:"inline", position:"relative", top:"-80px"}}>
                <span id="question-number">{currentQuestion+1}. </span>
                <span id="question-txt">{quizData[currentQuestion]}</span>

                </div>
            </div>):null}
           <div >
           <video ref={videoRef} autoPlay className="w-full h-auto object-cover rounded-lg" style={{ display: 'block', height: "450px" ,width:"500px", objectFit:"fill", transform: 'scaleX(-1)', position:"relative", top:"-70px", right:"300px" }}></video>
            <Form onSubmit={(e)=>{changeQuestion(e, currentQuestion)}} style={{width:"500px", position:"relative", top:"-80px"}}>
            <Form.Group className="mb-3 w-100" style={{display:"inline"}} controlId="formBasicUserName">

            {/* displays transcript */}
            <textarea rows = "17" cols = "100" class="form-control" type="text" placeholder={transcript} style={{position: "relative", left:"300px", top:"-370px"}} name = "answer" disabled/>
            </Form.Group>
            <div style={{position:"relative", right:"450px", top:"-320px"}}>
            <Button className="btn-primary" id="next-button" type="submit" style={{"fontFamily":"Arial", "backgroundColor":"rgb(68, 20, 90)", display:"inline", float:"right", position:"relative", left:"120px", bottom:"80px", width:"150px", height:"80px", border:"solid"}}>Submit</Button>
            <Button className="btn-primary" id="next-button" onClick={startListening} style={{"fontFamily":"Arial", "backgroundColor":"rgb(68, 20, 90)", display:"inline", float:"right", position:"relative", left:"120px", bottom:"80px" , width:"150px", height:"80px",border:"solid"}}>Start Recording</Button>
            <Button className="btn-primary" id="next-button" onClick={SpeechRecognition.stopListening} style={{"fontFamily":"Arial", "backgroundColor":"rgb(68, 20, 90)", display:"inline", float:"right", position:"relative", left:"120px", bottom:"80px" , width:"150px", height:"80px", border:"solid"}}>Stop Recording</Button>
            </div>
            </Form>
            </div>
            
           
            </div>
            
            </>)}
       
        
    </div>
  )
}

export default Quiz
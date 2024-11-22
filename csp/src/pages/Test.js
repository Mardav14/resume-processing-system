// import React, { useEffect, useState } from "react";

// const Test = () => {
//   const [gazeData, setGazeData] = useState([]);

//   useEffect(() => {
//     const initializeWebGazer = async () => {
//       try {
//         // Initialize WebGazer
//         console.log("here")
//         await window.webgazer.begin();

//         console.log("WebGazer initialized");
        
//         // Start the interval for prediction
//         const interval = setInterval(() => {
//           var prediction = window.webgazer.getCurrentPrediction()
//           // .then(()=>{
//           //   setGazeData((prevData) => [...prevData,{ x: prediction.x, y: prediction.y }])
//           //   console.log("Current Prediction:", prediction);
//           //   console.log(gazeData)
//           // })
//           if (prediction) {
//             var x = prediction.x;
//             var y = prediction.y;
//             console.log(x)
//             console.log(y)
//           }
          
//             // setGazeData((prevData) => [...prevData,{ x: prediction.x, y: prediction.y }]);
//             // console.log("Current Prediction:", prediction);
          
//         }, 5000);

//         return () => {
//           clearInterval(interval);
//           window.webgazer.end(); // Cleanup WebGazer
//         };
//       } catch (error) {
//         console.error("Error initializing WebGazer:", error);
//       }
//     };

//     initializeWebGazer();

//     // Cleanup function
//     return () => {
//       if (window.webgazer) {
//         window.webgazer.end();
//       }
//     };
//   }, []);

//   return <div>Tracking Gaze...</div>;
// };

// export default Test;

// import React, {useEffect, useState} from 'react'

// const Test = () => {

//   const [gazeData, setGazeData] = useState([])

//   useEffect(()=>{
//     const webgazer = window.webgazer
//     webgazer.setGazeListener((data, clock)=>{
//       if(data)
//         setGazeData((prevData) => [...prevData, { x: data.x, y: data.y }]);
//       console.log(data)
//       // console.log(gazeData)
//     }).begin()
//     setTimeout(()=>{
//       webgazer.pause()
//     },10000)

//     // const interval = setInterval(()=>{
//     //   const webgazer = window.webgazer
//     //   var prediction = webgazer.getCurrentPrediction()
//     //   .then(()=>{
//     //     console.log(prediction)
//     //   })
      

//     // }, 5000)

//     // return ()=>{
//     //   clearInterval(interval)
//     // }
//   })
//   return (
//     <div>
      
//     </div>
//   )
// }

// export default Test

import React, { useEffect, useState } from 'react';
import webgazer from "webgazer"

const Test = () => {
  const [gazeData, setGazeData] = useState([]);

  useEffect(() => {
    webgazer.setGazeListener((data) => {
        if (data) {
          // setGazeData((prevData) => [...prevData, { x: data.x, y: data.y }]);
          console.log(data)
        }
      }).begin()

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

      console.log('Average Gaze Coordinates:', average);
    };

    // Set an interval to calculate the average every 5 seconds
    const interval = setTimeout(() => {
      // calculateAverage();
    }, 5000);

  }, [gazeData]); // Re-run effect if gazeData changes

  return <div>Tracking Gaze... Check the console for gaze averages.</div>;
};

export default Test;

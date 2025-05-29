import React from 'react'
import AuthContext from '../context/AuthContext'
import { useEffect, useState, useContext } from 'react'
//bootstrap imports
import { Button, Form, Modal, Table } from 'react-bootstrap'


const HrDashboard = () => {

  let {user} = useContext(AuthContext)
  let [results, setResults] = useState({})
  let [showModal, setShowModal] = useState(false)
  let [selectedCandidate, setSelectedCandidate] = useState(null)
  let [loading, setLoading] = useState(false);


    let Shortlist = async (e) => {
  e.preventDefault();
  setLoading(true);  // Start loading

  try {
    let response = await fetch("http://127.0.0.1:8000/api/shortlist", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        'years_experience': e.target.exp.value,
        'required_skills': e.target.skill.value,
        'required_education': e.target.edu.value
      })
    });

    let data = await response.json();
    if (response.status === 200) {
      console.log(data);
      setResults(data);
    } else {
      alert("Something went wrong");
    }
  } catch (error) {
    alert("Network error");
  }

  setLoading(false);  // Stop loading
};



  const handleViewDetails = async(username) => {

        let response = await fetch(`http://127.0.0.1:8000/api/candidate/${username}`, {
            method : "GET",
        })
        let data = await response.json()
        if(response.status === 200){
          console.log(data)
            setSelectedCandidate(data)
        }
        else{
            alert("Something went wrong")
        }
    setShowModal(true)
  }

  const handleDownloadResume = async (username) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/resume/${username}`, {
      method: "GET"
    });

    if (!response.ok) {
      throw new Error("Failed to download");
    }

    // Extract filename from headers
    const disposition = response.headers.get('Content-Disposition');
    let filename = `${username}_resume`; // default fallback

    if (disposition && disposition.includes('filename=')) {
      filename = disposition
        .split('filename=')[1]
        .replace(/['"]/g, '')
        .trim();
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);  // use actual filename
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (err) {
    alert('Failed to download resume');
    console.error(err);
  }
};



  return (
    <div className='container py-5' style={{width: "80%"}}>
    <Form onSubmit={Shortlist}>
      <br/><br/>
    <Form.Group className="mb-3 w-1/2">
        <Form.Label><div className='baseText'>Enter Minimum years of experience required</div> </Form.Label>
        <Form.Control style={{width: "50%"}} type="text" name = "exp" />
       </Form.Group>
    <Form.Group className="mb-3">
        <Form.Label><div className='baseText'>Enter Qualification requirement</div> </Form.Label>
        <Form.Control type="text" placeholder="qualification requirement" name = "edu" />
       </Form.Group>
    <Form.Group className="mb-3">
        <Form.Label><div className='baseText'>Enter Skills Required</div> </Form.Label>
        <Form.Control type="text" placeholder="skills required" name = "skill" />
       </Form.Group>
      <br/>
      <Button variant="primary" type="submit">
        Shortlist Candidates
      </Button>
    </Form>
    
      {loading && (
        
  <div className="my-5">
    
    <div className="progress">
      <div
        className="progress-bar progress-bar-striped progress-bar-animated bg-info"
        role="progressbar"
        style={{ width: '100%' }}
      >
        Shortlisting...
      </div>
    </div>
  </div>
)}

{results.required_skills?.length > 0 && !loading && (
  <div className="mb-4 p-3 my-5 border rounded bg-light">
    <h5 className="mb-3">Extracted Required Skills</h5>
    <div className="d-flex flex-wrap justify-content-start gap-3">
      {results.required_skills.map((skill, index) => (
        <div
          key={index}
          className="px-3 py-2 border rounded text-center"
          style={{ minWidth: '120px', flexGrow: 1 }}
        >
          {skill}
        </div>
      ))}
    </div>
  </div>
)}
      {Object.keys(results).length> 0 && !loading &&(
        <div className="mt-5">
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th></th> {/* View Details */}
                <th></th> {/* Resume */}
                <th>Skills Match</th>
                <th>Qualification Match</th>
                <th>Final Score</th>
              </tr>
            </thead>
           <tbody>
  {[...Object.entries(results.scores)]
    .map(([username, score]) => {
      const totalSkills = results.required_skills.length;
      const skillMatch = score.skill_score;
      const qualificationMatch = Math.floor(score.education_similarity * 100);
      const finalScore = Math.round(((skillMatch / totalSkills) * 100 + qualificationMatch) / 2);

      return {
        username,
        email: score.email || 'user@example.com',
        skillMatch,
        qualificationMatch,
        finalScore,
        totalSkills
      };
    })
    .sort((a, b) => b.finalScore - a.finalScore) // Descending sort
    .map(candidate => (
      <tr key={candidate.username}>
        <td>{candidate.username}</td>
        <td>{candidate.email}</td>
        <td><Button onClick={() => handleViewDetails(candidate.username)}>View Details</Button></td>
        <td><Button onClick={() => handleDownloadResume(candidate.username)}>Resume</Button></td>
        <td>{`${candidate.skillMatch} / ${candidate.totalSkills}`}</td>
        <td>{candidate.qualificationMatch}%</td>
        <td>{candidate.finalScore}%</td>
      </tr>
    ))}
</tbody>
          </Table>
        </div>
      )}
     
{/* Modal for Candidate Details */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Candidate Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedCandidate && (
            <div>
              <p><strong>Full Name:</strong> {selectedCandidate.full_name || 'N/A'}</p>
              <p><strong>Email:</strong> {selectedCandidate.email || 'N/A'}</p>
              <p><strong>Phone No.:</strong> {selectedCandidate.phone || 'N/A'}</p>
              <p><strong>Skills:</strong> {selectedCandidate.skills?.join(', ') || 'N/A'}</p>
              <p><strong>Years of Experience:</strong> {selectedCandidate.years_experience || 'N/A'}</p>
              <p><strong>Location:</strong> {selectedCandidate.location || 'N/A'}</p>
              <p><strong>Education:</strong> {selectedCandidate.education_list?.join(', ') || 'N/A'}</p>
            </div>
          )}
        </Modal.Body>
      </Modal>

  </div>
)
    
}

export default HrDashboard



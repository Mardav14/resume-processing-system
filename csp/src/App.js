import './App.css';
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import Register from './pages/Register'
import OnBoarding from './pages/OnBoarding'
import SelectRole from './pages/SelectRole'
import Quiz from './pages/Quiz'
import Test from './pages/Test';

import { BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import PrivateRoute from './utils/PrivateRoute'
import NavBar from './components/NavBar'
import {AuthProvider} from './context/AuthContext'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import HrDashboard from './pages/HrDashboard';
import CreateJob from './pages/CreateJob';

function App() {
  return (
    <div className="App">
   
      <Router>
        <AuthProvider>
          <NavBar />
          <Routes>
          <Route element={<OnBoarding />} path="/" exact /> 
          <Route element={<PrivateRoute ><HomePage /></ PrivateRoute >} path="user" />
          <Route element={<LoginPage />} path="/login" />
          <Route element={<SelectRole />} path="/select-role" />
          <Route element={<Register />} path="/register/:role" />
          <Route element={<HrDashboard />} path="/hr-dashboard" />
          <Route element={<Quiz />} path="/quiz/:title" />
          <Route element={<CreateJob />} path="/create-job" />
          <Route element={<Test />} path="/test" />
          
          </Routes>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;

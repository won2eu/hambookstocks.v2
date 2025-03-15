import './App.css';
import Navbar from './components/Navbar';
import PageSlider from './components/PageSlider'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


function App() {
  return (
    <div className="App">
    <Navbar />
    <PageSlider />
    </div>
  );
}

export default App;
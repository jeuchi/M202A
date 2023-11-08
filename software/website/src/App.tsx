import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './Home';
import Proposal from './Proposal';

function App() {
  return (
    <div className="App">
      <div className="navbar bg-neutral text-neutral-content items-center">
        <div className="flex-none pl-5">
          <a href="/" className="normal-case text-2xl">
            RoadSense
          </a>
        </div>
        <div className="pl-20">
              <a href="proposal" className="text-l hover:underline hover:decoration-blue-400 font-medium">
                Proposal
              </a>
        </div>
      </div>
      <div className="mx-auto max-w-6xl pt-10">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/proposal" element={<Proposal />} />
            <Route path="*" element={<Home />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;

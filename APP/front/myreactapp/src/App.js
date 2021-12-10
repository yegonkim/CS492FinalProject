import Homepage from "./pages/hompage";
import Diary from "./pages/diary";
import Register from "./pages/register";
import { Routes, Route} from "react-router-dom";
import './App.css';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/diary" element={<Diary />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}

export default App;

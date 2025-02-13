// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Movies from "./pages/Movies";
import Watchlist from "./pages/Watchlist";
import AddMovie from "./pages/AddMovie";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ProtectedRoute from "./component/ProtectedRoute";
import "./App.css";

function App() {
  return (
    <Router>
      <nav className="navbar">
        <div className="logo">🎬 MovieMania</div>
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/movies">Browse Movies</Link></li>
          <li><Link to="/watchlist">My Watchlist ⭐</Link></li>
          <li><Link to="add-movie">➕ Add Movie</Link></li>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/signup">Sign Up</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/movies" element={<Movies />} />
        <Route path="/watchlist" element={<Watchlist />} />
        <Route path="add-movie" element={<AddMovie />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route path="/watchlist" element={<ProtectedRoute><Watchlist /></ProtectedRoute>} />
        <Route path="/add-movie" element={<ProtectedRoute><AddMovie /></ProtectedRoute>} />

      </Routes>
    </Router>
  );
}

export default App;

import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            Movie App
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <Link className="nav-link active" to="/">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/movies">
                  Movies
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/add-movie">
                  Add Movie
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Home Page Content */}
      <div className="container mt-5 text-center">
        <h1 className="display-3 text-primary">Welcome to the Movie App!</h1>
        <p className="lead mt-4">
          Browse through your favorite movies or add new ones to the collection. Enjoy!
        </p>
        <div className="mt-5">
          <Link to="/movies" className="btn btn-lg btn-primary">
            View Movies
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;

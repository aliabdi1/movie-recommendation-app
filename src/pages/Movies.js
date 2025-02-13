import React, { useEffect, useState } from "react";
import "./movie.css";

const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";

function Movies() {
  const [movies, setMovies] = useState([]);
  const [watchlist, setWatchlist] = useState([]);

  // ✅ Fetch movies
  useEffect(() => {
    fetch(`${apiUrl}/movies`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch movies.");
        return res.json();
      })
      .then((data) => setMovies(data))
      .catch((err) => console.error("Error fetching movies:", err));
  }, []);

  // ✅ Fetch watchlist on load
  useEffect(() => {
    fetch(`${apiUrl}/users/1/watchlist`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch watchlist.");
        return res.json();
      })
      .then((data) => setWatchlist(data))
      .catch((err) => console.error("Error fetching watchlist:", err));
  }, []);

  // ✅ Toggle watchlist function
  const toggleWatchlist = (movieId) => {
    const isInWatchlist = watchlist.some((movie) => movie.id === movieId);

    fetch(`${apiUrl}/users/1/watchlist/${movieId}`, {
      method: isInWatchlist ? "DELETE" : "POST",
      headers: { "Content-Type": "application/json" },
      body: isInWatchlist ? null : JSON.stringify({}) // Send an empty object if no data
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to update watchlist.");
        return res.json();
      })
      .then(() => {
        setWatchlist((prev) =>
          isInWatchlist
            ? prev.filter((movie) => movie.id !== movieId)
            : [...prev, movies.find((movie) => movie.id === movieId)]
        );
      })
      .catch((error) => console.error("Error updating watchlist:", error));
  };

  return (
    <div className="movies-container">
      <h1>Browse Movies 🍿</h1>
      <div className="movies-grid">
        {movies.map((movie) => (
          <div key={movie.id} className="movie-card">
            <h2>{movie.title}</h2>
            <p>{movie.genre}</p>
            {movie.release_year && <p>📅 {movie.release_year}</p>}  
            <button
              className={`btn-watchlist ${
                watchlist.some((w) => w.id === movie.id) ? "in-watchlist" : ""
              }`}
              onClick={() => toggleWatchlist(movie.id)}
            >
              {watchlist.some((w) => w.id === movie.id)
                ? "⭐ In Watchlist"
                : "☆ Add to Watchlist"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Movies;

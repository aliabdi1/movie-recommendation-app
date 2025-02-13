// src/pages/Watchlist.js
import React, { useEffect, useState } from "react";

const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";
const userId = 1; 

function Watchlist() {
  const [watchlist, setWatchlist] = useState([]);
  const [editingMovie, setEditingMovie] = useState(null);
  const [newRating, setNewRating] = useState("");


  const fetchWatchlist = () => {
    fetch(`${apiUrl}/users/${userId}/watchlist`)
      .then((res) => res.json())
      .then((data) => setWatchlist(data))
      .catch((err) => console.error("Error fetching watchlist:", err));
  };

  useEffect(() => {
    fetchWatchlist();
  }, []);

  // Delete movie from watchlist
  const handleDelete = (movieId) => {
    fetch(`${apiUrl}/users/${userId}/watchlist/${movieId}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then(() => fetchWatchlist()) // Refresh the list
      .catch((err) => console.error("Error deleting movie:", err));
  };

  // Edit movie rating
  const handleEdit = (movie) => {
    setEditingMovie(movie.id);
    setNewRating(movie.rating || "");
  };

  const handleSave = (movieId) => {
    fetch(`${apiUrl}/users/${userId}/watchlist/${movieId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ rating: newRating }),
    })
      .then((res) => res.json())
      .then(() => {
        setEditingMovie(null);
        fetchWatchlist(); // Refresh the list
      })
      .catch((err) => console.error("Error updating rating:", err));
  };

  return (
    <div className="watchlist-container">
      <h1>⭐ My Watchlist</h1>
      {watchlist.length === 0 ? (
        <p>No movies in your watchlist yet.</p>
      ) : (
        <div className="movies-grid">
          {watchlist.map((movie) => (
            <div key={movie.id} className="movie-card">
              <h2>{movie.title}</h2>
              <p>{movie.genre}</p>

              {editingMovie === movie.id ? (
                <div>
                  <input
                    type="number"
                    placeholder="Rating (1-10)"
                    value={newRating}
                    onChange={(e) => setNewRating(e.target.value)}
                    min="1"
                    max="10"
                  />
                  <button onClick={() => handleSave(movie.id)}>💾 Save</button>
                  <button onClick={() => setEditingMovie(null)}>❌ Cancel</button>
                </div>
              ) : (
                <div>
                  <p>⭐ Rating: {movie.rating || "Not Rated"}</p>
                  <button onClick={() => handleEdit(movie)}>✏️ Edit Rating</button>
                </div>
              )}

              <button onClick={() => handleDelete(movie.id)}>🗑️ Remove</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Watchlist;

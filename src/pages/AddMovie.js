// src/pages/AddMovie.js
import React, { useState } from "react";

const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";


function AddMovie() {
  const [title, setTitle] = useState("");
  const [genre, setGenre] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch(`${apiUrl}/movies`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, genre }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to add movie");
        }
        return res.json();
      })
      .then((data) => {
        setMessage("🎉 Movie added successfully!");
        setTitle("");
        setGenre("");
      })
      .catch((err) => {
        console.error("Error adding movie:", err);
        setMessage("❌ Failed to add movie.");
      });
  };

  return (
    <div className="add-movie-container">
      <h1>🎬 Add a New Movie</h1>
      <form onSubmit={handleSubmit} className="add-movie-form">
        <input
          type="text"
          placeholder="Movie Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Genre"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          required
        />
        <button type="submit">➕ Add Movie</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default AddMovie;

import React, { useEffect, useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";

function Movies() {
  const [movies, setMovies] = useState([]);
  const [editingMovie, setEditingMovie] = useState(null);
  const [watchlist, setWatchlist] = useState([]);

  // Fetch all movies
  useEffect(() => {
    fetch("http://localhost:5555/movies")
      .then((response) => response.json())
      .then((data) => setMovies(data))
      .catch((error) => console.error("Error fetching movies:", error));
  }, []);

  // Fetch user's watchlist when component loads
  useEffect(() => {
    fetch("http://localhost:5555/users/1/watchlist")
      .then((res) => res.json())
      .then((data) => setWatchlist(data))
      .catch((error) => console.error("Error fetching watchlist:", error));
  }, []);

  function toggleWatchlist(movieId) {
    const isInWatchlist = watchlist.some((movie) => movie.id === movieId);

    fetch(`http://localhost:5555/users/1/watchlist/${movieId}`, {
      method: isInWatchlist ? "DELETE" : "POST",
    })
      .then((res) => res.json())
      .then(() => {
        setWatchlist((prev) =>
          isInWatchlist
            ? prev.filter((movie) => movie.id !== movieId)
            : [...prev, movies.find((movie) => movie.id === movieId)]
        );
      })
      .catch((error) => console.error("Error updating watchlist:", error));
  }

  function handleAddMovie(newMovie) {
    setMovies([...movies, newMovie]);
    setEditingMovie(null);
  }

  function handleDelete(id) {
    if (!window.confirm("Are you sure you want to delete this movie?")) return;

    fetch(`http://localhost:5555/movies/${id}`, {
      method: "DELETE",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to delete movie.");
        }
        return res.json();
      })
      .then(() => {
        setMovies(movies.filter((movie) => movie.id !== id));
      })
      .catch((error) => alert(error.message));
  }

  function handleEdit(movie) {
    setEditingMovie(movie);
  }

  function handleUpdateMovie(updatedMovie) {
    setMovies(movies.map((movie) => (movie.id === updatedMovie.id ? updatedMovie : movie)));
    setEditingMovie(null);
  }

  return (
    <div className="container mt-5">
      <h2 className="text-center text-2xl font-bold">Movies</h2>
      <AddMovieForm onAddMovie={handleAddMovie} />

      <ul className="list-group mt-4">
        {movies.map((movie) => (
          <li key={movie.id || Math.random()} className="list-group-item d-flex justify-content-between align-items-center">
            {editingMovie && editingMovie.id === movie.id ? (
              <EditMovieForm movie={movie} onUpdateMovie={handleUpdateMovie} />
            ) : (
              <>
                <span>
                  {movie.title} ({movie.genre})
                </span>
                <div>
                  <button
                    onClick={() => handleEdit(movie)}
                    className="btn btn-warning btn-sm me-2"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(movie.id)}
                    className="btn btn-danger btn-sm me-2"
                  >
                    Delete
                  </button>
                  <button
                    onClick={() => toggleWatchlist(movie.id)}
                    className={`btn btn-sm ${
                      watchlist.some((w) => w.id === movie.id) ? "btn-success" : "btn-secondary"
                    }`}
                  >
                    {watchlist.some((w) => w.id === movie.id) ? "Remove from Watchlist" : "Add to Watchlist"}
                  </button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

// Add Movie Form
function AddMovieForm({ onAddMovie }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const formik = useFormik({
    initialValues: { title: "", genre: "" },
    validationSchema: Yup.object({
      title: Yup.string().required("Title is required"),
      genre: Yup.string().required("Genre is required"),
    }),
    onSubmit: (values, { resetForm }) => {
      setLoading(true);
      setError("");
      fetch("http://localhost:5555/movies", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      })
        .then((res) => res.json())
        .then((newMovie) => {
          onAddMovie(newMovie);
          resetForm();
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message);
          setLoading(false);
        });
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} className="card p-4">
      <div className="mb-3">
        <input
          name="title"
          type="text"
          placeholder="Movie Title"
          {...formik.getFieldProps("title")}
          className="form-control"
        />
        {formik.touched.title && formik.errors.title && <p className="text-danger">{formik.errors.title}</p>}
      </div>

      <div className="mb-3">
        <input
          name="genre"
          type="text"
          placeholder="Genre"
          {...formik.getFieldProps("genre")}
          className="form-control"
        />
        {formik.touched.genre && formik.errors.genre && <p className="text-danger">{formik.errors.genre}</p>}
      </div>

      {error && <p className="text-danger">{error}</p>}
      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? "Adding..." : "Add Movie"}
      </button>
    </form>
  );
}

// Edit Movie Form
function EditMovieForm({ movie, onUpdateMovie }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const formik = useFormik({
    initialValues: { title: movie.title, genre: movie.genre },
    validationSchema: Yup.object({
      title: Yup.string().required("Title is required"),
      genre: Yup.string().required("Genre is required"),
    }),
    onSubmit: (values) => {
      setLoading(true);
      fetch(`http://localhost:5555/movies/${movie.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      })
        .then((res) => res.json())
        .then((updatedMovie) => {
          onUpdateMovie(updatedMovie);
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message);
          setLoading(false);
        });
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} className="card p-4">
      <div className="mb-3">
        <input
          name="title"
          type="text"
          {...formik.getFieldProps("title")}
          className="form-control"
        />
        {formik.touched.title && formik.errors.title && <p className="text-danger">{formik.errors.title}</p>}
      </div>

      <div className="mb-3">
        <input
          name="genre"
          type="text"
          {...formik.getFieldProps("genre")}
          className="form-control"
        />
        {formik.touched.genre && formik.errors.genre && <p className="text-danger">{formik.errors.genre}</p>}
      </div>

      {error && <p className="text-danger">{error}</p>}
      <button type="submit" className="btn btn-success" disabled={loading}>
        {loading ? "Updating..." : "Update"}
      </button>
    </form>
  );
}

export default Movies;

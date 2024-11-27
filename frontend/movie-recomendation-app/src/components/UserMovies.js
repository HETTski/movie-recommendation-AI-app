import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './UserMovies.css';

const UserMovies = () => {
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/user/movies/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setMovies(response.data);
      } catch (error) {
        console.error('Error fetching user movies:', error);
        setError('Failed to fetch movies. Please try again.');
      }
    };

    fetchMovies();
  }, []);

  return (
    <div className="user-movies-container">
      <h2>Your Movies</h2>
      {error && <p className="error">{error}</p>}
      <ul>
        {movies.length > 0 ? (
          movies.map((movie) => (
            <li key={movie.id}>
              <strong>{movie.title}</strong>: {movie.description}
            </li>
          ))
        ) : (
          <p>No movies found. Add some to your list!</p>
        )}
      </ul>
    </div>
  );
};

export default UserMovies;

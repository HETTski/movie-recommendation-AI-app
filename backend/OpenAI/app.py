from flask import Flask, request, jsonify
import requests
import openai
from config import TMDB_API_KEY, OPENAI_API_KEY

# Konfiguracja klucza API OpenAI
openai.api_key = OPENAI_API_KEY

# Słownik nazw gatunków do ich ID w TMDb
GENRE_IDS = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "science fiction": 878,
    "tv movie": 10770,
    "thriller": 53,
    "war": 10752,
    "western": 37
}

app = Flask(__name__)

def get_movie_recommendations(genres):
    """Zwraca rekomendacje filmów na podstawie gatunków."""
    genre_ids = ",".join(map(str, genres))
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&with_genres={genre_ids}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error {response.status_code} when sending request to TMDb")
        return []

def get_now_playing_movies():
    """Zwraca filmy obecnie grane w kinach."""
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error {response.status_code} when sending request to TMDb")
        return []

def generate_gpt_response(prompt):
    """Generuje odpowiedź czatu za pomocą GPT."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in movies."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint obsługujący rozmowę z chatbotem."""
    data = request.json
    user_input = data.get("message", "")
    show_now_playing = data.get("show_now_playing", False)

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # Analiza preferencji użytkownika
    genres = [genre_id for genre_name, genre_id in GENRE_IDS.items() if genre_name in user_input.lower()]

    # Generowanie odpowiedzi przez GPT
    gpt_prompt = f"The user said: '{user_input}'. Respond in the context of movie recommendations."
    gpt_response = generate_gpt_response(gpt_prompt)

    recommendations = ""
    
    # Filmy grane obecnie w kinach
    if show_now_playing:
        now_playing_movies = get_now_playing_movies()
        if genres:
            now_playing_movies = [movie for movie in now_playing_movies if any(genre in movie['genre_ids'] for genre in genres)]
        if now_playing_movies:
            recommendations += "Here are some movies currently playing in theaters:\n"
            recommendations += "\n".join([f"{movie['title']} - {movie['overview'][:100]}..." for movie in now_playing_movies[:5]])
        else:
            recommendations += "No 'now playing' movies match your genre preferences.\n\n"

    # Rekomendacje na podstawie gatunków
    if genres:
        genre_based_movies = get_movie_recommendations(genres)
        if genre_based_movies:
            recommendations += "Here are some popular movies based on your genre preferences:\n"
            recommendations += "\n".join([f"{movie['title']} - {movie['overview'][:100]}..." for movie in genre_based_movies[:5]])
        else:
            recommendations += "No popular movies match your genre preferences."
    else:
        recommendations += "Please specify some genres to get movie recommendations."

    return jsonify({
        "gpt_response": gpt_response,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

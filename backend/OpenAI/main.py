import requests
import openai
from config import TMDB_API_KEY, OPENAI_API_KEY

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

# Dictionary of genre names to TMDb genre IDs
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

def get_movie_recommendations(genres):
    """
    Function to get movie recommendations based on genres.
    """
    genre_ids = ",".join(map(str, genres))
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&with_genres={genre_ids}"
    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get("results", [])
        return movies
    else:
        print(f"Error {response.status_code} when sending request to TMDb")
        return []

def get_now_playing_movies():
    """
    Function to get movies currently playing in theaters.
    """
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get("results", [])
        return movies
    else:
        print(f"Error {response.status_code} when sending request to TMDb")
        return []

def filter_movies_by_genre(movies, genres):
    """
    Function to filter movies by genres.
    """
    filtered_movies = [movie for movie in movies if any(genre in movie['genre_ids'] for genre in genres)]
    return filtered_movies

def generate_gpt_response(prompt):
    """
    Function to generate chatbot response using GPT.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def chatbot_conversation(user_input, show_now_playing=False):
    """
    Main function that conducts a conversation with the user.
    """
    # Step 1: Analyze user preferences
    prompt = f"The user said: '{user_input}'. Respond in the context of movie recommendations."
    gpt_response = generate_gpt_response(prompt)
    print(f"GPT response: {gpt_response}")
    
    return gpt_response

    # Step 2: Get movie genres from user input
    genres = []
    for genre_name, genre_id in GENRE_IDS.items():
        if genre_name in user_input.lower():
            genres.append(genre_id)

    recommendations = ""
    
    # Step 3: Show "Now Playing" movies if requested
    if show_now_playing:
        now_playing_movies = get_now_playing_movies()
        if genres:
            now_playing_movies = filter_movies_by_genre(now_playing_movies, genres)
        if now_playing_movies:
            recommendations += "Here are some movies currently playing in theaters:\n"
            recommendations += "\n".join([f"{movie['title']} - {movie['overview'][:100]}..." for movie in now_playing_movies[:5]])
            recommendations += "\n\n"
        else:
            recommendations += "No 'now playing' movies match your genre preferences.\n\n"

    # Step 4: Show popular movies based on specified genres
    if genres:
        genre_based_movies = get_movie_recommendations(genres)
        if genre_based_movies:
            recommendations += "Here are some popular movies based on your genre preferences:\n"
            recommendations += "\n".join([f"{movie['title']} - {movie['overview'][:100]}..." for movie in genre_based_movies[:5]])
        else:
            recommendations += "No popular movies match your genre preferences."
    else:
        # Fallback if no genres were specified
        recommendations += "Please specify some genres to get popular movie recommendations."

    return recommendations


# Example conversation
if __name__ == "__main__":
    user_input = input("Enter your movie preferences: ")
    now_playing_choice = input("Do you want to see movies that are now playing in theaters? (yes/no): ").strip().lower()
    show_now_playing = now_playing_choice == "yes"
    
    chatbot_response = chatbot_conversation(user_input, show_now_playing=show_now_playing)
    print("Chatbot:", chatbot_response)

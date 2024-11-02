# main.py

import requests
import openai
from config import TMDB_API_KEY, OPENAI_API_KEY

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

def get_movie_recommendations(genres):
    """
    Function to get movie recommendations based on genres.
    """
    # Request to TMDb
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&with_genres={genres}"
    print(f"Sending request to TMDb: {url}")
    
    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get("results", [])
        print(f"Number of movies found: {len(movies)}")
        return movies
    else:
        print(f"Error {response.status_code} when sending request to TMDb")
        return []

def get_now_playing_movies():
    """
    Function to get movies currently playing in theaters.
    """
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US"
    print(f"Sending request to TMDb: {url}")
    
    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get("results", [])
        print(f"Number of movies found: {len(movies)}")
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
        model="gpt-4",  # Choose the appropriate model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def chatbot_conversation(user_input):
    """
    Main function that conducts a conversation with the user.
    """
    # Step 1: Analyze user preferences
    prompt = f"The user said: '{user_input}'. Respond in the context of movie recommendations."
    gpt_response = generate_gpt_response(prompt)
    print(f"GPT response: {gpt_response}")
    
    # Step 2: Determine if the user wants to watch something currently playing or older
    now_playing = "now playing" in user_input.lower() or "in theaters" in user_input.lower()
    
    # Step 3: Get movie genres (may require processing by GPT)
    genres = []
    if "action" in user_input.lower():
        genres.append(28)  # Example: Genre ID for 'action' in TMDb
    if "comedy" in user_input.lower():
        genres.append(35)  # Example: Genre ID for 'comedy' in TMDb
    if "drama" in user_input.lower():
        genres.append(18)  # Example: Genre ID for 'drama' in TMDb
    # Add more genres as needed

    # Step 4: Get movies based on now playing or popular categories
    if now_playing:
        # Fetch movies that are currently playing in theaters
        movies = get_now_playing_movies()
        # Filter movies by genres, if any genres were specified
        if genres:
            movies = filter_movies_by_genre(movies, genres)
    else:
        # Fetch popular movies by specified genres if not looking for "now playing"
        genre_ids = ",".join(map(str, genres))
        movies = get_movie_recommendations(genre_ids)
    
    # Step 5: Generate recommendations for the user
    if movies:
        recommendations = "\n".join([f"{movie['title']} - {movie['overview'][:100]}..." for movie in movies[:5]])
        final_response = f"Here are some movies you might like:\n{recommendations}"
    else:
        final_response = "Unfortunately, I couldn't find any movies matching your preferences."

    return final_response


# Example conversation
if __name__ == "__main__":
    user_input = input("Enter your movie preferences: ")
    chatbot_response = chatbot_conversation(user_input)
    print("Chatbot:", chatbot_response)

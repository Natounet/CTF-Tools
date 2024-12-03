# Writeup for Challenge: #1 Movie Scrap

---

### Challenge Description

The challenge consists of connecting to a remote server and participating in a movie quiz. The goal is to guess the user rating for **10 movies**. Each movie rating must be provided within **5 seconds**. To accomplish this, we scrape **The Movie Database (TMDB)** to retrieve the correct rating and send it back to the server.

---

### Solution Approach

#### Step 1: Connect to the Server
We use a Python script with the `socket` library to establish a connection to the provided host and port:
nc amsi-sorbonne.fr 4005


Upon connection, the server sends a list of movie titles wrapped in quotes. These are the movies for which we need to guess the ratings.

#### Step 2: Scrape TMDB for Ratings
Using the movie names provided by the server, we construct search queries to **TMDB**:
- Search for each movie on TMDB using its name.
- Locate the correct movie link on the search results page.
- Scrape the movie details page for the user rating (`data-percent` attribute in the `user_score_chart` class).

#### Step 3: Send Ratings to the Server
Once the ratings are extracted:
- We send each rating back to the server.
- After correctly answering, the server may send another movie title or conclude the session.

#### Step 4: Automate the Entire Process
The provided Python script automates this process:
1. Connect to the server and parse movie names from the response.
2. Search for each movie on TMDB and extract ratings.
3. Send the ratings back to the server, handling the quiz loop until completion.

---

### Python Script

Below is the Python script that solves the challenge:

```python
import socket
import re
import requests
from bs4 import BeautifulSoup

def connect_to_server(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        movies = re.findall(r'"(.*?)"', banner)
        return movies, sock
    except Exception as e:
        print(f"Error: {e}")
        return [], None

def search_movie_on_tmdb(movie_name):
    search_url = f"https://www.themoviedb.org/search?query={movie_name.replace(' ', '%20')}&language=en"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_link = soup.find('a', href=True, class_="result")
        if movie_link:
            return f"https://www.themoviedb.org{movie_link['href']}"
    return None

def fetch_movie_details(movie_url):
    response = requests.get(movie_url)
    if response.status_code == 200:
        return response.text
    return None

def extract_user_score(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    user_score_div = soup.find('div', class_='user_score_chart', attrs={'data-percent': True})
    return user_score_div['data-percent'] if user_score_div else None

def send_score_to_server(sock, score):
    sock.sendall(f"{score}\n".encode('utf-8'))
    return sock.recv(1024).decode('utf-8').strip()

def main():
    host, port = "amsi-sorbonne.fr", 4005
    movies, sock = connect_to_server(host, port)
    if not sock:
        print("Connection failed.")
        return

    try:
        for movie_name in movies:
            movie_url = search_movie_on_tmdb(movie_name)
            if movie_url:
                movie_details = fetch_movie_details(movie_url)
                if movie_details:
                    score = extract_user_score(movie_details)
                    if score:
                        response = send_score_to_server(sock, score)
                        if "OK !" not in response:
                            break
    finally:
        sock.close()

if __name__ == "__main__":
    main()

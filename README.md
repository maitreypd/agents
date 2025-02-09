# Spotify Assistant

A Spotify assistant built on top of Chainlit that helps users create playlists, search for tracks by genre, add tracks to playlists, and retrieve playlist IDs. This project leverages the Spotify API, ChatOpenAI, LangChain, and Langgraph to provide a conversational interface for interacting with Spotify.

---

## Demo
A demo video file Spotify_demo.mov is added to this repository

## Capabilities

- **Create Playlist**: Create a new playlist on Spotify.
- **Search Tracks by Genre**: Search for tracks within a specified genre on Spotify.
- **Add Track to Playlist**: Add tracks to an existing Spotify playlist.
- **Get Playlist ID by Name**: Retrieve the playlist ID for a given playlist name.
- **Conversational Workflow**: Uses Langgraph to manage state and conversation flow with conditional routing between different actions.
- **LLM-Powered Decision Making**: Utilizes ChatOpenAI (GPT-4o) to determine the next action based on user input and conversation history.

---

## Prerequisites

- **Python**: Python 3.8 or higher.
- **Spotify Developer Account**: Required to obtain API credentials.
- **OpenAI API Key**: Required for accessing ChatOpenAI models.
- **Poetry**: Used for dependency management and project configuration.
- **pyproject.toml**: The project is configured using Poetry via the `pyproject.toml` file.

### Environment Variables

Configuration variables will be read using `os.getenv()`. Ensure the following environment variables are available in your system's environment (note that no `.env` file is used):

- `SPOTIFY_ACCESS_TOKEN`: Your Spotify access token for API calls.
- `USER_ACCESS_TOKEN`: Your Spotify user access token.
- `SPOTIFY_USER_ID`: Your Spotify user ID.
- `OPENAI_KEY`: Your OpenAI API key.

---

## Technologies Used

- **Python**: The programming language used for development.
- **Chainlit**: A framework for building conversational applications.
- **Spotify API**: Provides access to Spotify’s music catalog and user playlists.
- **ChatOpenAI**: Leverages GPT models for natural language processing.
- **LangChain**: Facilitates chaining together different language model calls.
- **Langgraph**: Manages conversation state using a graph-based approach.
- **Requests**: For making HTTP requests to the Spotify API.
- **Poetry**: Dependency management and project configuration.

---

## How to Run
1. git clone git@github.com:maitreypd/agents.git .
2. cd agents
3. poetry install
4. chainlit run main.py -w

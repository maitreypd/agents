from typing import List

from langchain_core.tools import tool
import requests

from config.config import USER_ACCESS_TOKEN, SPOTIFY_USER_ID, SPOTIFY_ACCESS_TOKEN


class SpotifyTools:
    @staticmethod
    @tool
    async def get_playlist_id_by_name(playlist_name: str) -> str:
        """
        Searches the current user's playlists for a playlist matching the given name.
        Returns the playlist ID if found; otherwise returns None.
        """
        url = f"https://api.spotify.com/v1/users/{SPOTIFY_USER_ID}/playlists"
        headers = {"Authorization": f"Bearer {USER_ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for playlist in data.get("items", []):
                if playlist.get("name", "").lower() == playlist_name.lower():
                    return f"Playlist id is found for given playlist {playlist.get('id')}"
        return "No ID found"

    @staticmethod
    @tool
    async def search_tracks_by_genre(genre):
        """
        Searches for tracks in the Spotify catalog that match the specified genre.

        Args:
            genre (str): The genre to search for.

        Returns:
            list: A list of dictionaries containing track information.
        """
        url = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}'
        }
        params = {
            'q': f'genre:"{genre}"',
            'type': 'track',
            'limit': 10
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching search results: {response.status_code}, {response.text}")

        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])
        track_list = []
        for track in tracks:
            track_info = {
                'name': track['name'],
                'artist': ', '.join(artist['name'] for artist in track['artists']),
                'album': track['album']['name'],
                'preview_url': track['preview_url'],
                'spotify_url': track['external_urls']['spotify']
            }
            track_list.append(track_info)

        return track_list

    @staticmethod
    @tool
    async def create_playlist(playlist_name: str = None):
        """
        Create a new playlist on Spotify.
        If playlist_name is not provided, ask the user for one.
        """
        url = f"https://api.spotify.com/v1/users/{SPOTIFY_USER_ID}/playlists"
        headers = {
            "Authorization": f"Bearer {USER_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": playlist_name,
            "public": True  # Change to True if you want a public playlist
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            data = response.json()
            playlist_id = data.get("id")
            return f"Playlist '{playlist_name}' created successfully with ID: {playlist_id}"
        else:
            return f"Error creating playlist: {response.status_code} - {response.text}"

    @staticmethod
    @tool
    async def add_track_to_playlist(playlist_id: str = None, track_uris: List[str] = None):
        """
        Add an item (track) to an existing Spotify playlist.
        If playlist_id is not provided, ask the user for the playlist name and search for its ID.
        If item (track URI) is not provided, ask the user for it.
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {USER_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        # for track_id in track_uris:
        payload = {"uris": track_uris}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            return f"Items '{track_uris}' added successfully to playlist {playlist_id}"
        else:
            return f"Error adding item to playlist: {response.status_code} - {response.text}"
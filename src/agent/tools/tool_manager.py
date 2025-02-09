from langgraph.prebuilt import ToolNode

from tools.spotify_tools import SpotifyTools


class ToolManager:
    tools = [
        SpotifyTools.create_playlist,
        SpotifyTools.add_track_to_playlist,
        SpotifyTools.get_playlist_id_by_name,
        SpotifyTools.search_tracks_by_genre
    ]
    tool_node = ToolNode(tools=tools)
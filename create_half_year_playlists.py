import os
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set your Spotify API credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

# Scope needed for accessing saved tracks and managing playlists
scope = "user-library-read playlist-modify-public"

# Set up Spotipy with user authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Fetch all saved tracks and determine the earliest added_at date
def fetch_saved_tracks_and_earliest_date():
    print("Initializing time travel through your Spotify library...")
    tracks = []
    min_date = None
    results = sp.current_user_saved_tracks(limit=50)
    latest_year = datetime.now().year
    while results:
        for item in results['items']:
            tracks.append(item)
            added_at = item['added_at']
            track_year = datetime.strptime(added_at, "%Y-%m-%dT%H:%M:%SZ").year
            if min_date is None or added_at < min_date:
                min_date = added_at
                if track_year < latest_year:
                    latest_year = track_year
                    print(f"Time traveling back to {track_year}...")
        if results['next']:
            results = sp.next(results)
        else:
            break
    print(f"Earliest track found from {latest_year}. Preparing to sort tracks into half-yearly playlists...")
    return tracks, min_date

# Create half-yearly playlists and distribute tracks
def create_and_distribute_playlists(tracks, min_date):
    min_date = datetime.strptime(min_date, "%Y-%m-%dT%H:%M:%SZ")
    min_year = min_date.year
    start_half = 1 if min_date.month <= 6 else 2
    current_date = datetime.now()
    current_year = current_date.year
    current_half = 1 if current_date.month <= 6 else 2
    user_id = sp.current_user()["id"]
    playlist_track_map = defaultdict(list)

    # Organize tracks by their target playlist
    for track in tracks:
        added_at = track['added_at']
        added_date = datetime.strptime(added_at, "%Y-%m-%dT%H:%M:%SZ")
        year = added_date.year
        half = '1/2' if added_date.month <= 6 else '2/2'
        playlist_name = f"{year} - {half} test"
        playlist_track_map[playlist_name].append(track['track']['uri'])

    # Create playlists and add tracks
    for year in range(min_year, current_year + 1):
        for half in ['1/2', '2/2']:
            if year == current_year and ((half == '1/2' and current_half == 2) or (half == '2/2' and current_half == 1)):
                continue
            playlist_name = f"{year} - {half}"
            track_uris = playlist_track_map.get(playlist_name, [])
            if track_uris:
                # Check if playlist exists, if not, create it
                playlist_id = find_playlist_by_name(playlist_name, user_id)
                if not playlist_id:
                    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
                    playlist_id = playlist['id']
                    print(f"Created playlist: {playlist_name}")
                # Add tracks to playlist in batches of 100
                for i in range(0, len(track_uris), 100):
                    sp.user_playlist_add_tracks(user_id, playlist_id, track_uris[i:i+100])
                print(f"Added {len(track_uris)} tracks to playlist: {playlist_name}")

# Helper function to find a playlist by name
def find_playlist_by_name(name, user_id):
    playlists = sp.user_playlists(user_id)
    while playlists:
        for playlist in playlists['items']:
            if playlist['name'] == name:
                return playlist['id']
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break
    return None

# Main process
if __name__ == "__main__":
    saved_tracks, earliest_date = fetch_saved_tracks_and_earliest_date()
    create_and_distribute_playlists(saved_tracks, earliest_date)

from flask import Blueprint

bp = Blueprint('spotifyapp', __name__)


spotify_client_id = "8f775a31bc9b4e67a8ae753400cd7cfb"
spotify_client_secret = "770936463c1a47068ef59d26f1ceb143"
scope='user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-modify user-library-read'

auth_manager = SpotifyOAuth(client_id=spotify_client_id,
                        client_secret=spotify_client_secret,
                        redirect_uri='http://localhost:5000',
                        scope=scope)
sp = spotipy.Spotify(client_credentials_manager=auth_manager)

devices = sp.devices()
active_device = next((device for device in devices['devices'] if device['is_active']), None)


@bp.route("/spotify/playpause")
def spotify_playpause():
    if active_device is None:
        print("No active device found.")
        return "No Active Device"
    try:
        if sp.current_playback()['is_playing']:
            # Pause playback
            print("Pausing music...")
            sp.pause_playback(device_id=active_device['id'])        
            print(f"Toggled playback on device {active_device['name']}")
            return "Paused"
        else:
            # Resume playback
            print("Resuming music...")
            sp.start_playback(device_id=active_device['id'])
            print(f"Toggled playback on device {active_device['name']}")
            return "Unpaused"
    except Exception as e:
        print(f"An error occurred while toggling playback: {e}")
        return "error"

@bp.route("/spotify/shuffletoggle")
def spotify_shuffletoggle():
    if active_device is None:
        print("No active device found.")
        return "No Active Device"
    try:
        print(sp.current_playback())
        if sp.current_playback()['shuffle_state']:
            # Pause playback
            print("Unshuffling music...")
            sp.shuffle(False, device_id=active_device['id'])        
            print(f"Unshuffled playback on device {active_device['name']}")
            return "Unshuffled"
        else:
            # Resume playback
            print("Shuffling music...")
            sp.shuffle(True,device_id=active_device['id'])
            print(f"Shuffled playback on device {active_device['name']}")
            return "Shuffled"
    except Exception as e:
        print(f"An error occurred while toggling playback: {e}")
        return "error"

@bp.route("/spotify/repeattoggle")
def spotify_repeattoggle():
    if active_device is None:
        print("No active device found.")
        return "No Active Device"
    try:
        if sp.current_playback()['repeat_state'] == 'context':
            print("Not repeating music...")
            sp.repeat("off", device_id=active_device['id'])        
            print(f"Not repeating playback on device {active_device['name']}")
            return "Repeat Off"
        elif sp.current_playback()['repeat_state'] == 'track':
            print("Repeat all music...")
            sp.repeat("context",device_id=active_device['id'])
            print(f"Repeat all playback on device {active_device['name']}")
            return "Repeat All"
        elif sp.current_playback()['repeat_state'] == 'off':
            print("Repeat current music...")
            sp.repeat("track",device_id=active_device['id'])
            print(f"Repeat current playback on device {active_device['name']}")
            return "Repeat once"
    except Exception as e:
        print(f"An error occurred while toggling playback: {e}")
        return "error"
    
@bp.route("/spotify/next")
def next():
    if active_device is None:
        print("No active device found.")
        return "No Active Device"
    try:
        sp.next_track(device_id=active_device['id'])
        print(f"Skipped track on device {active_device['name']}")
        return "Skipped Track"
    except Exception as e:
        print(f"An error occurred while toggling playback: {e}")
        return "error"


@bp.route("/spotify/back")
def back():
    if active_device is None:
        print("No active device found.")
        return "No Active Device"
    try:
        sp.previous_track(device_id=active_device['id'])
        print(f"Back tracked on device {active_device['name']}")
        return "Back Tracked"
    except Exception as e:
        print(f"An error occurred while toggling playback: {e}")
        return "error"

@bp.route("/spotify/volume/<direction>")
def manage_volume(direction):
    if active_device is None:
        print("No active device found.")
        return "No Active Device"
    try:
        # Get the current playback state
        # Extract the device ID
        device_id = active_device['id']
        
        # Get the current volume
        current_volume = active_device['volume_percent']

        if direction == 'down':
            sp.volume(device_id=device_id, volume_percent=max(0, min(current_volume-5, 100)))
            print(f"Decreased volume from {current_volume}% to " + (current_volume-5) + "%")
            return "New Volume: " + current_volume-5
        elif direction == 'up':
            sp.volume(device_id=device_id, volume_percent=max(0, min(current_volume+5, 100)))
            print(f"Decreased volume from {current_volume}% to " + (current_volume+5) + "%")
            return "New Volume: " + current_volume+5
    
    except Exception as e:
        print(f"Error managing volume: {e}")
        return "error"


from flask import Blueprint


bp = Blueprint('spotifyapp', __name__)







@bp.route("/spotify/playpause")
def spotify_playpause():
    

@bp.route("/spotify/shuffletoggle")
def spotify_shuffletoggle():
    

@bp.route("/spotify/repeattoggle")
def spotify_repeattoggle():
    
    
@bp.route("/spotify/next")
def nextsong():
    


@bp.route("/spotify/back")
def back():
    

@bp.route("/spotify/volume/<direction>")
def manage_volume(direction):
    


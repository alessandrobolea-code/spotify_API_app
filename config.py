"""
File di configurazione per le credenziali Spotify
"""
import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

# Leggi le credenziali dalle variabili d'ambiente
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Verifica che le credenziali siano presenti
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError(
        "Credenziali Spotify mancanti! "
        "Assicurati di aver creato il file .env con SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET"
    )

# Configurazioni API
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL = 'https://api.spotify.com/v1'

# Redirect URI per OAuth
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

# Impostazioni di ricerca (con valori di default)
DEFAULT_SEARCH_LIMIT = int(os.getenv('SEARCH_LIMIT', 10))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Mapping dei generi specifici a macro-categorie
GENRE_MAPPING = {
    # Pop
    'pop': 'Pop',
    'dance pop': 'Electronic',
    'electropop': 'Pop',
    'art pop': 'Indie',
    'indie pop': 'Indie',
    'synth-pop': 'Electronic',
    'power pop': 'Pop',
    'pop rock': 'Rock',
    'teen pop': 'Pop',
    'k-pop': 'K-Pop',
    'j-pop': 'J-Pop',
    'latin pop': 'Latin',
    'italian pop': 'Pop Italiano',
    'french pop': 'French Pop',
    'german pop': 'Pop',

    # Rock
    'rock': 'Rock',
    'classic rock': 'Rock',
    'hard rock': 'Rock',
    'alternative rock': 'Rock',
    'indie rock': 'Indie Rock',
    'punk rock': 'Rock',
    'folk rock': 'Rock',
    'progressive rock': 'Rock',
    'psychedelic rock': 'Rock',
    'garage rock': 'Rock',
    'glam rock': 'Rock',
    'soft rock': 'Rock',
    'southern rock': 'Rock',
    'surf rock': 'Rock',
    'art rock': 'Rock',

    # Metal
    'metal': 'Metal',
    'heavy metal': 'Metal',
    'death metal': 'Metal',
    'black metal': 'Metal',
    'thrash metal': 'Metal',
    'power metal': 'Metal',
    'progressive metal': 'Metal',
    'metalcore': 'Metal',
    'nu metal': 'Metal',
    'alternative metal': 'Grunge',

    # Hip Hop / Rap
    'hip hop': 'Hip Hop',
    'rap': 'Hip Hop',
    'trap': 'Hip Hop',
    'underground hip hop': 'Hip Hop',
    'conscious hip hop': 'Hip Hop',
    'gangster rap': 'Hip Hop',
    'old school hip hop': 'Hip Hop',
    'southern hip hop': 'Hip Hop',
    'east coast hip hop': 'Hip Hop',
    'west coast rap': 'Hip Hop',
    'canadian hip hop': 'Hip Hop',
    'uk hip hop': 'Hip Hop',
    'german hip hop': 'Hip Hop',
    'french hip hop': 'Hip Hop',
    'italian hip hop': 'Hip Hop Italiano',
    'italian underground hip hop': 'Hip Hop Italiano',
    'trap italiano': 'Hip Hop Italiano',
    'rap italiano': 'Hip Hop Italiano',
    'italian trap': 'Hip Hop Italiano',

    # R&B / Soul
    'r&b': 'R&B',
    'rhythm and blues': 'R&B',
    'soul': 'R&B',
    'neo soul': 'R&B',
    'contemporary r&b': 'R&B',
    'alternative r&b': 'R&B',
    'motown': 'R&B',

    # Funk / Disco
    'funk': 'Funk',
    'disco': 'Funk',
    'nu-disco': 'Funk',

    # Electronic / Dance
    'electronic': 'Electronic',
    'edm': 'Electronic',
    'house': 'Electronic',
    'techno': 'Electronic',
    'trance': 'Electronic',
    'dubstep': 'Electronic',
    'drum and bass': 'Electronic',
    'electro': 'Electronic',
    'dance': 'Electronic',
    'big room': 'Electronic',
    'future bass': 'Electronic',
    'tropical house': 'Electronic',
    'deep house': 'Electronic',
    'tech house': 'Electronic',
    'progressive house': 'Electronic',
    'electro house': 'Electronic',
    'electronica': 'Electronic',

    # Jazz
    'jazz': 'Jazz',
    'smooth jazz': 'Jazz',
    'jazz fusion': 'Jazz',
    'bebop': 'Jazz',
    'swing': 'Jazz',
    'contemporary jazz': 'Jazz',

    # Blues
    'blues': 'Blues',
    'electric blues': 'Blues',
    'chicago blues': 'Blues',
    'delta blues': 'Blues',

    # Country
    'country': 'Country',
    'contemporary country': 'Country',
    'country rock': 'Country',
    'outlaw country': 'Country',
    'bluegrass': 'Country',

    # Reggae / Latin
    'reggae': 'Reggae',
    'dancehall': 'Reggae',
    'dub': 'Reggae',
    'ska': 'Reggae',
    'reggaeton': 'Latin',
    'latin': 'Latin',
    'salsa': 'Latin',
    'bachata': 'Latin',
    'cumbia': 'Latin',
    'merengue': 'Latin',
    'latin rock': 'Latin',
    'spanish pop': 'Latin',
    'banda': 'Latin',

    # Classical
    'classical': 'Classical',
    'opera': 'Classical',
    'baroque': 'Classical',
    'romantic': 'Classical',
    'modern classical': 'Classical',

    # Indie / Alternative
    'indie': 'Indie',
    'alternative': 'Indie',
    'indie folk': 'Indie',
    'chamber pop': 'Indie',

    # Folk / Acoustic
    'folk': 'Folk',
    'acoustic': 'Folk',
    'singer-songwriter': 'Folk',
    'americana': 'Folk',

    # World
    'world': 'World',
    'afrobeat': 'World',
    'bossa nova': 'World',
    'flamenco': 'World',
    'celtic': 'World',

    # Ambient / Chill / Lo-Fi
    'ambient': 'Ambient',
    'chillout': 'Ambient',
    'downtempo': 'Ambient',
    'chill': 'Ambient',
    'lo-fi': 'Lo-Fi',
    'chillwave': 'Lo-Fi',
    'bedroom pop': 'Lo-Fi',

    # Grunge
    'grunge': 'Grunge',

    # French Pop / Chanson
    'french indie pop': 'French Pop',
    'chanson': 'French Pop',
    'belgian pop': 'French Pop',

    # Cantautori Italiani
    'italian adult pop': 'Cantautori Italiani',
    'cantautore': 'Cantautori Italiani',

    # Tag specifici artisti
    'permanent wave': 'Indie',
    'sheffield indie': 'Indie',
    'neo-psychedelic': 'Indie'
}

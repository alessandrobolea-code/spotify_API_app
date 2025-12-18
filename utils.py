"""
Funzioni di utilità per visualizzare i dati
"""


def display_artists(artists):
    """
    Visualizza le informazioni degli artisti in modo formattato
    
    Args:
        artists: Lista di artisti da visualizzare
    """
    if not artists:
        print("Nessun artista trovato.")
        return
    
    print(f"\n{'='*70}")
    print(f"Trovati {len(artists)} artisti:")
    print(f"{'='*70}\n")
    
    for i, artist in enumerate(artists, 1):
        print(f"{i}. {artist['name']}")
        print(f"   Generi: {', '.join(artist['genres']) if artist['genres'] else 'N/A'}")
        print(f"   Popolarità: {artist['popularity']}/100")
        print(f"   Followers: {artist['followers']['total']:,}")
        print(f"   Spotify URL: {artist['external_urls']['spotify']}")
        
        if artist['images']:
            print(f"   Immagine: {artist['images'][0]['url']}")
        
        print()


def display_tracks(tracks):
    """
    Visualizza le informazioni delle canzoni in modo formattato
    
    Args:
        tracks: Lista di canzoni da visualizzare
    """
    if not tracks:
        print("Nessuna canzone trovata.")
        return
    
    print(f"\n{'='*70}")
    print(f"Trovate {len(tracks)} canzoni:")
    print(f"{'='*70}\n")
    
    for i, track in enumerate(tracks, 1):
        artists_names = ', '.join([artist['name'] for artist in track['artists']])
        duration_min = track['duration_ms'] // 60000
        duration_sec = (track['duration_ms'] % 60000) // 1000
        
        print(f"{i}. {track['name']}")
        print(f"   Artista: {artists_names}")
        print(f"   Album: {track['album']['name']}")
        print(f"   Durata: {duration_min}:{duration_sec:02d}")
        print(f"   Popolarità: {track['popularity']}/100")
        print(f"   Spotify URL: {track['external_urls']['spotify']}")
        print()


def display_saved_tracks(saved_tracks_items):
    """
    Visualizza i brani salvati (preferiti)
    
    Args:
        saved_tracks_items: Lista di items dai brani salvati
    """
    if not saved_tracks_items:
        print("Nessun brano salvato trovato.")
        return
    
    print(f"\n{'='*80}")
    print(f"I TUOI BRANI PREFERITI ({len(saved_tracks_items)} brani)")
    print(f"{'='*80}\n")
    
    for i, item in enumerate(saved_tracks_items, 1):
        track = item['track']
        added_at = item['added_at'][:10]  # Solo la data
        
        artists_names = ', '.join([artist['name'] for artist in track['artists']])
        duration_min = track['duration_ms'] // 60000
        duration_sec = (track['duration_ms'] % 60000) // 1000
        
        print(f"{i}. {track['name']}")
        print(f"   Artista: {artists_names}")
        print(f"   Album: {track['album']['name']}")
        print(f"   Durata: {duration_min}:{duration_sec:02d}")
        print(f"   Aggiunto il: {added_at}")
        print(f"   Popolarità: {track['popularity']}/100")
        print(f"   URL: {track['external_urls']['spotify']}")
        print()


def display_top_items(items, item_type='tracks'):
    """
    Visualizza top tracks o top artists
    
    Args:
        items: Lista di brani o artisti
        item_type: 'tracks' o 'artists'
    """
    if not items:
        print(f"Nessun {item_type} trovato.")
        return
    
    title = "I TUOI BRANI PIÙ ASCOLTATI" if item_type == 'tracks' else "I TUOI ARTISTI PIÙ ASCOLTATI"
    
    print(f"\n{'='*80}")
    print(title)
    print(f"{'='*80}\n")
    
    if item_type == 'tracks':
        for i, track in enumerate(items, 1):
            artists_names = ', '.join([artist['name'] for artist in track['artists']])
            duration_min = track['duration_ms'] // 60000
            duration_sec = (track['duration_ms'] % 60000) // 1000
            
            print(f"{i}. {track['name']} - {artists_names}")
            print(f"   Album: {track['album']['name']}")
            print(f"   Durata: {duration_min}:{duration_sec:02d}")
            print(f"   Popolarità: {track['popularity']}/100")
            print(f"   URL: {track['external_urls']['spotify']}")
            print()
    else:  # artists
        for i, artist in enumerate(items, 1):
            print(f"{i}. {artist['name']}")
            print(f"   Generi: {', '.join(artist['genres'][:3]) if artist['genres'] else 'N/A'}")
            print(f"   Popolarità: {artist['popularity']}/100")
            print(f"   Followers: {artist['followers']['total']:,}")
            print(f"   URL: {artist['external_urls']['spotify']}")
            print()


def format_number(num):
    """
    Formatta un numero con separatori delle migliaia
    
    Args:
        num: Numero da formattare
        
    Returns:
        str: Numero formattato
    """
    return f"{num:,}"


def format_duration(duration_ms):
    """
    Formatta la durata da millisecondi a mm:ss
    
    Args:
        duration_ms: Durata in millisecondi
        
    Returns:
        str: Durata formattata (es. "3:45")
    """
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"

def display_playlists(playlists):
    """
    Visualizza le playlist dell'utente
    
    Args:
        playlists: Lista di playlist
    """
    if not playlists:
        print("Nessuna playlist trovata.")
        return
    
    print(f"\n{'='*80}")
    print(f"LE TUE PLAYLIST ({len(playlists)})")
    print(f"{'='*80}\n")
    
    for i, playlist in enumerate(playlists, 1):
        owner = playlist['owner']['display_name']
        tracks_total = playlist['tracks']['total']
        visibility = "Pubblica" if playlist['public'] else "Privata"
        
        print(f"{i}. {playlist['name']}")
        print(f"   Creata da: {owner}")
        print(f"   Brani: {tracks_total}")
        print(f"   Visibilità: {visibility}")
        
        if playlist.get('description'):
            print(f"   Descrizione: {playlist['description']}")
        
        print(f"   URL: {playlist['external_urls']['spotify']}")
        print()
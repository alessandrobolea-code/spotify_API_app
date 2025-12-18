"""
Script principale per cercare artisti e canzoni su Spotify
"""
from spotify_client import SpotifyClient
from utils import (
    display_artists, 
    display_tracks, 
    display_saved_tracks, 
    display_top_items,
    display_playlists
)
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def menu():
    """
    Mostra il menu principale
    """
    print("\n" + "="*60)
    print("SPOTIFY SEARCH TOOL")
    print("="*60)
    print("1. Cerca artista")
    print("2. Cerca canzone")
    print("3. Visualizza i tuoi brani preferiti")
    print("4. Visualizza i tuoi top brani")
    print("5. Visualizza i tuoi top artisti")
    print("6. Visualizza le tue playlist")
    print("7. Crea una nuova playlist")
    print("8. Crea playlist dai top brani")
    print("9. Crea playlist dai brani salvati")
    print("10. 🎨 Dividi brani per genere (AUTO)")
    print("11. Esci")
    print("="*60)
    
    return input("Scegli un'opzione (1-11): ")


def search_artist_flow(client):
    """
    Flusso per cercare un artista
    """
    artist_name = input("\nInserisci il nome dell'artista: ")
    print(f"\nCerco '{artist_name}'...")
    
    try:
        artists = client.search_artist(artist_name)
        display_artists(artists)
    except Exception as e:
        print(f"❌ Errore: {e}")


def search_track_flow(client):
    """
    Flusso per cercare una canzone
    """
    track_name = input("\nInserisci il titolo della canzone: ")
    print(f"\nCerco '{track_name}'...")
    
    try:
        tracks = client.search_track(track_name)
        display_tracks(tracks)
    except Exception as e:
        print(f"❌ Errore: {e}")


def view_saved_tracks_flow(client):
    """
    Flusso per visualizzare i brani preferiti
    """
    try:
        choice = input("\nVuoi vedere:\n1. Primi 50 brani\n2. TUTTI i brani\nScelta (1-2): ")
        
        if choice == '1':
            result = client.get_saved_tracks(limit=50)
            display_saved_tracks(result['items'])
            print(f"\nTotale brani salvati nel tuo account: {result['total']}")
        else:
            tracks = client.get_all_saved_tracks()
            display_saved_tracks(tracks)
    
    except Exception as e:
        print(f"❌ Errore: {e}")


def view_top_tracks_flow(client):
    """
    Flusso per visualizzare i top brani
    """
    print("\nPeriodo di tempo:")
    print("1. Ultime 4 settimane")
    print("2. Ultimi 6 mesi")
    print("3. Di sempre")
    
    choice = input("Scegli (1-3): ")
    
    time_ranges = {
        '1': ('short_term', 'ultime 4 settimane'),
        '2': ('medium_term', 'ultimi 6 mesi'),
        '3': ('long_term', 'sempre')
    }
    
    time_range, period_name = time_ranges.get(choice, ('medium_term', 'ultimi 6 mesi'))
    
    try:
        print(f"\nRecupero i tuoi top brani ({period_name})...")
        tracks = client.get_top_tracks(time_range=time_range, limit=20)
        print(f"\n🎵 TOP 20 BRANI - {period_name.upper()}")
        display_top_items(tracks, 'tracks')
    except Exception as e:
        print(f"❌ Errore: {e}")


def view_top_artists_flow(client):
    """
    Flusso per visualizzare i top artisti
    """
    print("\nPeriodo di tempo:")
    print("1. Ultime 4 settimane")
    print("2. Ultimi 6 mesi")
    print("3. Di sempre")
    
    choice = input("Scegli (1-3): ")
    
    time_ranges = {
        '1': ('short_term', 'ultime 4 settimane'),
        '2': ('medium_term', 'ultimi 6 mesi'),
        '3': ('long_term', 'sempre')
    }
    
    time_range, period_name = time_ranges.get(choice, ('medium_term', 'ultimi 6 mesi'))
    
    try:
        print(f"\nRecupero i tuoi top artisti ({period_name})...")
        artists = client.get_top_artists(time_range=time_range, limit=20)
        print(f"\n🎤 TOP 20 ARTISTI - {period_name.upper()}")
        display_top_items(artists, 'artists')
    except Exception as e:
        print(f"❌ Errore: {e}")


def view_playlists_flow(client):
    """
    Flusso per visualizzare le playlist
    """
    try:
        print("\nRecupero le tue playlist...")
        playlists = client.get_user_playlists(limit=50)
        display_playlists(playlists)
    except Exception as e:
        print(f"❌ Errore: {e}")


def create_playlist_flow(client):
    """
    Flusso per creare una playlist personalizzata
    """
    print("\n" + "="*60)
    print("CREA NUOVA PLAYLIST")
    print("="*60)
    
    name = input("\nNome della playlist: ").strip()
    
    if not name:
        print("❌ Il nome della playlist non può essere vuoto")
        return
    
    description = input("Descrizione (opzionale): ").strip()
    
    public_choice = input("Playlist pubblica? (s/n): ").lower()
    public = public_choice == 's'
    
    try:
        playlist = client.create_playlist(name, description, public)
        
        # Chiedi se vuoi aggiungere brani ora
        add_tracks = input("\nVuoi aggiungere brani alla playlist? (s/n): ").lower()
        
        if add_tracks == 's':
            print("\nCerca i brani da aggiungere (uno alla volta):")
            print("Digita 'fine' quando hai finito\n")
            
            track_uris = []
            
            while True:
                search_query = input("Cerca brano (o 'fine'): ").strip()
                
                if search_query.lower() == 'fine':
                    break
                
                if not search_query:
                    continue
                
                # Cerca il brano
                tracks = client.search_track(search_query, limit=5)
                
                if not tracks:
                    print("❌ Nessun brano trovato")
                    continue
                
                # Mostra i risultati
                print("\nRisultati:")
                for i, track in enumerate(tracks, 1):
                    artists = ', '.join([a['name'] for a in track['artists']])
                    print(f"{i}. {track['name']} - {artists}")
                
                choice = input("\nScegli un brano (1-5, 0 per saltare): ")
                
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(tracks):
                        selected_track = tracks[choice_num - 1]
                        track_uris.append(selected_track['uri'])
                        print(f"✓ Aggiunto: {selected_track['name']}")
                except ValueError:
                    print("❌ Scelta non valida")
            
            # Aggiungi i brani alla playlist
            if track_uris:
                client.add_tracks_to_playlist(playlist['id'], track_uris)
                print(f"\n✓ {len(track_uris)} brani aggiunti alla playlist!")
    
    except Exception as e:
        print(f"❌ Errore: {e}")


def create_playlist_from_top_flow(client):
    """
    Flusso per creare playlist dai top brani
    """
    print("\n" + "="*60)
    print("CREA PLAYLIST DAI TOP BRANI")
    print("="*60)
    
    name = input("\nNome della playlist: ").strip()
    
    if not name:
        name = "My Top Tracks"
    
    print("\nPeriodo di tempo:")
    print("1. Ultime 4 settimane")
    print("2. Ultimi 6 mesi")
    print("3. Di sempre")
    
    choice = input("Scegli (1-3): ")
    
    time_ranges = {
        '1': 'short_term',
        '2': 'medium_term',
        '3': 'long_term'
    }
    
    time_range = time_ranges.get(choice, 'medium_term')
    
    limit_input = input("\nQuanti brani vuoi includere? (1-50, default 50): ").strip()
    
    try:
        limit = int(limit_input) if limit_input else 50
        limit = max(1, min(limit, 50))
    except ValueError:
        limit = 50
    
    try:
        client.create_playlist_from_top_tracks(name, time_range, limit)
    except Exception as e:
        print(f"❌ Errore: {e}")


def create_playlist_from_saved_flow(client):
    """
    Flusso per creare playlist dai brani salvati
    """
    print("\n" + "="*60)
    print("CREA PLAYLIST DAI BRANI SALVATI")
    print("="*60)
    
    name = input("\nNome della playlist: ").strip()
    
    if not name:
        name = "My Liked Songs Backup"
    
    max_input = input("\nQuanti brani vuoi includere? (lascia vuoto per tutti): ").strip()
    
    try:
        max_tracks = int(max_input) if max_input else None
    except ValueError:
        max_tracks = None
    
    try:
        client.create_playlist_from_saved_tracks(name, max_tracks)
    except Exception as e:
        print(f"❌ Errore: {e}")


def create_playlists_by_genre_flow(client):
    """
    Flusso per creare playlist divise per genere
    """
    print("\n" + "="*60)
    print("🎨 CREAZIONE PLAYLIST PER GENERE")
    print("="*60)
    print("\nQuesta funzione:")
    print("  • Analizza tutti i tuoi brani salvati")
    print("  • Li raggruppa per genere musicale")
    print("  • Crea playlist separate per ogni genere")
    print("="*60)
    
    min_tracks_input = input("\nNumero minimo di brani per playlist (default 5): ").strip()
    
    try:
        min_tracks = int(min_tracks_input) if min_tracks_input else 5
        min_tracks = max(1, min_tracks)  # Almeno 1
    except ValueError:
        min_tracks = 5
    
    public_choice = input("Creare playlist pubbliche? (s/n, default n): ").lower()
    make_public = public_choice == 's'
    
    try:
        client.create_playlists_by_genre(min_tracks, make_public)
    except Exception as e:
        print(f"❌ Errore: {e}")


def main():
    """
    Funzione principale
    """
    print("🎵 Inizializzazione Spotify Client...\n")
    
    try:
        client = SpotifyClient(
            CLIENT_ID, 
            CLIENT_SECRET,
            redirect_uri=REDIRECT_URI
        )
        
        print("✓ Client inizializzato correttamente")
        
        while True:
            choice = menu()
            
            if choice == '1':
                search_artist_flow(client)
            elif choice == '2':
                search_track_flow(client)
            elif choice == '3':
                view_saved_tracks_flow(client)
            elif choice == '4':
                view_top_tracks_flow(client)
            elif choice == '5':
                view_top_artists_flow(client)
            elif choice == '6':
                view_playlists_flow(client)
            elif choice == '7':
                create_playlist_flow(client)
            elif choice == '8':
                create_playlist_from_top_flow(client)
            elif choice == '9':
                create_playlist_from_saved_flow(client)
            elif choice == '10':
                create_playlists_by_genre_flow(client)
            elif choice == '11':
                print("\n👋 Arrivederci!")
                break
            else:
                print("\n❌ Opzione non valida, riprova.")
    
    except Exception as e:
        print(f"\n❌ Errore critico: {e}")


if __name__ == "__main__":
    main()
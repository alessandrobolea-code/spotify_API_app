"""
Client per interagire con l'API di Spotify
"""
import requests
import base64
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
import secrets
import time
from config import GENRE_MAPPING, SPOTIFY_AUTH_URL, SPOTIFY_API_URL, DEFAULT_SEARCH_LIMIT

class SpotifyClient:
    """
    Client per effettuare ricerche su Spotify
    """
    def __init__(self, client_id, client_secret, redirect_uri='http://localhost:8888/callback'):
        """
        Inizializza il client Spotify
        
        Args:
            client_id: Client ID di Spotify
            client_secret: Client Secret di Spotify
            redirect_uri: URI di redirect per OAuth (deve essere configurato nella dashboard Spotify)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.user_access_token = None  # Token per accesso ai dati utente
    
    
    def get_access_token(self):
        """
        Ottiene un access token da Spotify
        
        Returns:
            str: Access token
            
        Raises:
            Exception: Se l'autenticazione fallisce
        """
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post(SPOTIFY_AUTH_URL, headers=headers, data=data)
        
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            print("✓ Autenticazione riuscita")
            return self.access_token
        else:
            raise Exception(f"Errore autenticazione: {response.status_code} - {response.text}")
    
    def search_artist(self, artist_name, limit=DEFAULT_SEARCH_LIMIT):
        """
        Cerca un artista su Spotify
        
        Args:
            artist_name: Nome dell'artista
            limit: Numero massimo di risultati
            
        Returns:
            list: Lista di artisti trovati
        """
        if not self.access_token:
            self.get_access_token()
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': limit
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/search",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()['artists']['items']
        else:
            raise Exception(f"Errore ricerca: {response.status_code}")
    
    def search_track(self, track_name, limit=DEFAULT_SEARCH_LIMIT):
        """
        Cerca una canzone su Spotify
        
        Args:
            track_name: Nome della canzone
            limit: Numero massimo di risultati
            
        Returns:
            list: Lista di canzoni trovate
        """
        if not self.access_token:
            self.get_access_token()
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {
            'q': track_name,
            'type': 'track',
            'limit': limit
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/search",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()['tracks']['items']
        else:
            raise Exception(f"Errore ricerca: {response.status_code}")
    
    
    
    def get_user_authorization_url(self):
        """
        Genera l'URL per l'autorizzazione utente
        
        Returns:
            str: URL per l'autorizzazione
        """
        # Scopes necessari per accedere ai preferiti e gestire playlist
        scopes = [
            'user-library-read',        # Leggere i brani salvati
            'user-top-read',            # Leggere i top brani/artisti
            'playlist-read-private',    # Leggere le playlist private
            'playlist-modify-public',   # Modificare playlist pubbliche
            'playlist-modify-private',  # Modificare playlist private
            'user-read-private',        # Leggere info profilo utente
            'user-read-email'           # Leggere email utente
        ]
        
        # Genera uno state random per sicurezza
        state = secrets.token_urlsafe(16)
        
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(scopes),
            'state': state,
            'show_dialog': True  # Mostra sempre il dialog di autorizzazione
        }
    
        auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
        return auth_url, state
        
    def get_user_access_token_from_code(self, code):
        """
        Ottiene un access token utente dal codice di autorizzazione
        
        Args:
            code: Codice di autorizzazione ricevuto dal callback
            
        Returns:
            str: Access token utente
        """
        token_url = 'https://accounts.spotify.com/api/token'
        
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(token_url, headers=headers, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.user_access_token = token_data['access_token']
            print("✓ Autenticazione utente riuscita!")
            return self.user_access_token
        else:
            raise Exception(f"Errore nell'ottenere il token utente: {response.status_code} - {response.text}")
    
    def authorize_user(self):
        """
        Guida l'utente attraverso il processo di autorizzazione
        
        Returns:
            str: Access token utente
        """
        print("\n" + "="*70)
        print("AUTORIZZAZIONE SPOTIFY")
        print("="*70)
        print("\nPer accedere ai tuoi dati personali, devi autorizzare l'applicazione.")
        print("Si aprirà una pagina nel browser. Accedi e autorizza l'app.")
        print("\nDopo l'autorizzazione, verrai reindirizzato a una pagina.")
        print("Copia l'URL COMPLETO di quella pagina e incollalo qui.")
        print("="*70 + "\n")
        
        # Genera URL di autorizzazione
        auth_url, state = self.get_user_authorization_url()
        
        # Apri il browser
        print(f"Apertura del browser...")
        print(f"Se non si apre automaticamente, copia questo URL:\n{auth_url}\n")
        webbrowser.open(auth_url)
        
        # Attendi che l'utente incolli l'URL di callback
        callback_url = input("\nIncolla l'URL completo della pagina di redirect: ").strip()
        
        # Estrai il codice dall'URL
        try:
            parsed_url = urlparse(callback_url)
            params = parse_qs(parsed_url.query)
            
            if 'error' in params:
                raise Exception(f"Autorizzazione negata: {params['error'][0]}")
            
            code = params['code'][0]
            returned_state = params.get('state', [None])[0]
            
            # Verifica lo state per sicurezza (opzionale ma consigliato)
            if returned_state != state:
                print("⚠️ Warning: State mismatch (possibile attacco CSRF)")
            
            # Ottieni il token
            return self.get_user_access_token_from_code(code)
            
        except (KeyError, IndexError) as e:
            raise Exception(f"URL non valido. Assicurati di copiare l'URL completo. Errore: {e}")
    
    def get_saved_tracks(self, limit=50, offset=0):
        """
        Ottiene i brani salvati (preferiti) dell'utente
        
        Args:
            limit: Numero massimo di brani da recuperare (max 50 per richiesta)
            offset: Offset per la paginazione
            
        Returns:
            list: Lista di brani salvati con informazioni aggiuntive
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}'
        }
        
        params = {
            'limit': min(limit, 50),  # Spotify permette max 50 per richiesta
            'offset': offset
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/me/tracks",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("Token scaduto o non valido. Riautorizza l'applicazione.")
        else:
            raise Exception(f"Errore nel recupero dei preferiti: {response.status_code} - {response.text}")
    
    def get_all_saved_tracks(self):
        """
        Ottiene TUTTI i brani salvati dell'utente (gestisce la paginazione automaticamente)
        
        Returns:
            list: Lista completa di tutti i brani salvati
        """
        all_tracks = []
        offset = 0
        limit = 50
        
        print("Recupero dei brani preferiti...")
        
        while True:
            result = self.get_saved_tracks(limit=limit, offset=offset)
            tracks = result['items']
            
            if not tracks:
                break
            
            all_tracks.extend(tracks)
            print(f"  Recuperati {len(all_tracks)}/{result['total']} brani...")
            
            # Se abbiamo recuperato tutti i brani, esci
            if len(all_tracks) >= result['total']:
                break
            
            offset += limit
        
        print(f"✓ Recuperati tutti i {len(all_tracks)} brani preferiti!\n")
        return all_tracks
    
    def get_top_tracks(self, time_range='medium_term', limit=20):
        """
        Ottiene i brani più ascoltati dell'utente
        
        Args:
            time_range: Periodo di tempo ('short_term', 'medium_term', 'long_term')
                       short_term = ~4 settimane
                       medium_term = ~6 mesi
                       long_term = diversi anni
            limit: Numero di brani (max 50)
            
        Returns:
            list: Lista dei brani più ascoltati
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}'
        }
        
        params = {
            'time_range': time_range,
            'limit': min(limit, 50)
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/me/top/tracks",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise Exception(f"Errore nel recupero dei top brani: {response.status_code}")
    
    def get_top_artists(self, time_range='medium_term', limit=20):
        """
        Ottiene gli artisti più ascoltati dell'utente
        
        Args:
            time_range: Periodo di tempo ('short_term', 'medium_term', 'long_term')
            limit: Numero di artisti (max 50)
            
        Returns:
            list: Lista degli artisti più ascoltati
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}'
        }
        
        params = {
            'time_range': time_range,
            'limit': min(limit, 50)
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/me/top/artists",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise Exception(f"Errore nel recupero dei top artisti: {response.status_code}")
        
    def get_current_user(self):
        """
        Ottiene le informazioni dell'utente corrente
        
        Returns:
            dict: Informazioni dell'utente (id, display_name, ecc.)
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}'
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/me",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Errore nel recupero info utente: {response.status_code}")


    def create_playlist(self, name, description="", public=True):
        """
        Crea una nuova playlist per l'utente
        
        Args:
            name: Nome della playlist
            description: Descrizione della playlist
            public: Se True, la playlist è pubblica, altrimenti privata
            
        Returns:
            dict: Informazioni della playlist creata
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        # Ottieni l'ID dell'utente
        user = self.get_current_user()
        user_id = user['id']
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'name': name,
            'description': description,
            'public': public
        }
        
        response = requests.post(
            f"{SPOTIFY_API_URL}/users/{user_id}/playlists",
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            playlist = response.json()
            print(f"✓ Playlist '{name}' creata con successo!")
            print(f"  ID: {playlist['id']}")
            print(f"  URL: {playlist['external_urls']['spotify']}")
            return playlist
        else:
            raise Exception(f"Errore nella creazione della playlist: {response.status_code} - {response.text}")


    def add_tracks_to_playlist(self, playlist_id, track_uris):
        """
        Aggiunge brani a una playlist
        
        Args:
            playlist_id: ID della playlist
            track_uris: Lista di URI dei brani (es. ['spotify:track:xxx', 'spotify:track:yyy'])
            
        Returns:
            dict: Snapshot ID della playlist aggiornata
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}',
            'Content-Type': 'application/json'
        }
        
        # Spotify permette max 100 brani per richiesta
        max_tracks = 100
        
        # Se ci sono più di 100 brani, dividili in chunk
        for i in range(0, len(track_uris), max_tracks):
            chunk = track_uris[i:i + max_tracks]
            
            data = {
                'uris': chunk
            }
            
            response = requests.post(
                f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks",
                headers=headers,
                json=data
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Errore nell'aggiungere brani: {response.status_code} - {response.text}")
            
            print(f"✓ Aggiunti {len(chunk)} brani alla playlist")
        
        return response.json()


    def get_user_playlists(self, limit=50):
        """
        Ottiene le playlist dell'utente
        
        Args:
            limit: Numero massimo di playlist da recuperare
            
        Returns:
            list: Lista delle playlist dell'utente
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}'
        }
        
        params = {
            'limit': min(limit, 50)
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/me/playlists",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise Exception(f"Errore nel recupero delle playlist: {response.status_code}")


    def get_playlist_tracks(self, playlist_id):
        """
        Ottiene i brani di una playlist
        
        Args:
            playlist_id: ID della playlist
            
        Returns:
            list: Lista dei brani nella playlist
        """
        if not self.user_access_token:
            print("Necessaria l'autorizzazione utente...")
            self.authorize_user()
        
        headers = {
            'Authorization': f'Bearer {self.user_access_token}'
        }
        
        all_tracks = []
        offset = 0
        limit = 100
        
        while True:
            params = {
                'limit': limit,
                'offset': offset
            }
            
            response = requests.get(
                f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                tracks = data['items']
                
                if not tracks:
                    break
                
                all_tracks.extend(tracks)
                
                if len(all_tracks) >= data['total']:
                    break
                
                offset += limit
            else:
                raise Exception(f"Errore nel recupero dei brani: {response.status_code}")
        
        return all_tracks


    def create_playlist_from_top_tracks(self, name="My Top Tracks", time_range='medium_term', limit=50):
        """
        Crea automaticamente una playlist con i tuoi top brani
        
        Args:
            name: Nome della playlist
            time_range: Periodo di tempo ('short_term', 'medium_term', 'long_term')
            limit: Numero di brani da includere
            
        Returns:
            dict: Informazioni della playlist creata
        """
        print(f"\nCreo playlist '{name}'...")
        
        # Ottieni i top tracks
        print("Recupero i tuoi top brani...")
        top_tracks = self.get_top_tracks(time_range=time_range, limit=limit)
        
        if not top_tracks:
            raise Exception("Nessun brano trovato")
        
        # Crea la playlist
        period_names = {
            'short_term': 'ultime 4 settimane',
            'medium_term': 'ultimi 6 mesi',
            'long_term': 'sempre'
        }
        period = period_names.get(time_range, 'periodo selezionato')
        
        description = f"I miei {len(top_tracks)} brani più ascoltati ({period}) - Creata automaticamente"
        playlist = self.create_playlist(name, description, public=False)
        
        # Estrai gli URI dei brani
        track_uris = [track['uri'] for track in top_tracks]
        
        # Aggiungi i brani alla playlist
        print(f"Aggiungo {len(track_uris)} brani alla playlist...")
        self.add_tracks_to_playlist(playlist['id'], track_uris)
        
        print(f"\n✓ Playlist completata!")
        print(f"  {len(track_uris)} brani aggiunti")
        print(f"  Apri su Spotify: {playlist['external_urls']['spotify']}")
        
        return playlist


    def create_playlist_from_saved_tracks(self, name="My Liked Songs Backup", max_tracks=None):
        """
        Crea una playlist con tutti (o alcuni) i tuoi brani salvati
        
        Args:
            name: Nome della playlist
            max_tracks: Numero massimo di brani (None = tutti)
            
        Returns:
            dict: Informazioni della playlist creata
        """
        print(f"\nCreo playlist '{name}'...")
        
        # Ottieni i brani salvati
        print("Recupero i tuoi brani salvati...")
        saved_tracks = self.get_all_saved_tracks()
        
        if not saved_tracks:
            raise Exception("Nessun brano salvato trovato")
        
        # Limita se richiesto
        if max_tracks:
            saved_tracks = saved_tracks[:max_tracks]
        
        # Crea la playlist
        description = f"Backup di {len(saved_tracks)} brani dai miei preferiti - Creata automaticamente"
        playlist = self.create_playlist(name, description, public=False)
        
        # Estrai gli URI dei brani
        track_uris = [item['track']['uri'] for item in saved_tracks if item['track']]
        
        # Aggiungi i brani alla playlist
        print(f"Aggiungo {len(track_uris)} brani alla playlist...")
        self.add_tracks_to_playlist(playlist['id'], track_uris)
        
        print(f"\n✓ Playlist completata!")
        print(f"  {len(track_uris)} brani aggiunti")
        print(f"  Apri su Spotify: {playlist['external_urls']['spotify']}")
        
        return playlist
    
    def get_artist_info(self, artist_id):
        """
        Ottiene informazioni dettagliate su un artista (inclusi i generi)
        
        Args:
            artist_id: ID dell'artista
            
        Returns:
            dict: Informazioni complete dell'artista
        """
        if not self.access_token:
            self.get_access_token()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(
            f"{SPOTIFY_API_URL}/artists/{artist_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None


    def simplify_genre(self, genre):
        """
        Converte un genere specifico in una macro-categoria
        
        Args:
            genre: Genere specifico (es. "indie rock")
            
        Returns:
            str: Macro-categoria (es. "Rock")
        """
        genre_lower = genre.lower()
        return GENRE_MAPPING.get(genre_lower, 'Other')


    def group_tracks_by_genre(self, tracks_items, min_tracks=5):
        """
        Raggruppa i brani per genere semplificato
        
        Args:
            tracks_items: Lista di items dai brani salvati
            min_tracks: Numero minimo di brani per creare una playlist
            
        Returns:
            dict: Dizionario {genere: [lista di brani]}
        """
        genre_groups = {}
        processed = 0
        total = len(tracks_items)
        
        print(f"\n🔍 Analizzo {total} brani per genere...")
        print("Questo potrebbe richiedere qualche minuto...\n")
        
        for item in tracks_items:
            track = item['track']
            
            if not track or not track.get('artists'):
                continue
            
            # Prendi il primo artista (quello principale)
            artist_id = track['artists'][0]['id']
            
            # Ottieni info artista (con rate limiting)
            artist_info = self.get_artist_info(artist_id)
            
            if artist_info and artist_info.get('genres'):
                # Prendi il primo genere e semplificalo
                first_genre = artist_info['genres'][0]
                simplified_genre = self.simplify_genre(first_genre)
            else:
                simplified_genre = 'Other'
            
            # Aggiungi al gruppo
            if simplified_genre not in genre_groups:
                genre_groups[simplified_genre] = []
            
            genre_groups[simplified_genre].append(track)
            
            processed += 1
            
            # Mostra progresso ogni 10 brani
            if processed % 10 == 0 or processed == total:
                percentage = (processed / total) * 100
                print(f"  Progresso: {processed}/{total} ({percentage:.1f}%)")
            
            # Rate limiting: piccola pausa ogni 5 richieste
            if processed % 5 == 0:
                time.sleep(0.2)
        
        # Filtra generi con meno di min_tracks brani
        filtered_groups = {
            genre: tracks 
            for genre, tracks in genre_groups.items() 
            if len(tracks) >= min_tracks
        }
        
        # Sposta i brani dei generi filtrati in "Other"
        excluded_tracks = []
        for genre, tracks in genre_groups.items():
            if len(tracks) < min_tracks:
                excluded_tracks.extend(tracks)
        
        if excluded_tracks:
            if 'Other' not in filtered_groups:
                filtered_groups['Other'] = []
            filtered_groups['Other'].extend(excluded_tracks)
        
        return filtered_groups


    def create_playlists_by_genre(self, min_tracks=5, make_public=False):
        """
        Crea playlist separate per ogni genere musicale dai brani salvati
        
        Args:
            min_tracks: Numero minimo di brani per creare una playlist
            make_public: Se True, crea playlist pubbliche
            
        Returns:
            list: Lista delle playlist create
        """
        print("\n" + "="*70)
        print("CREAZIONE PLAYLIST PER GENERE")
        print("="*70)
        
        # Step 1: Recupera tutti i brani salvati
        print("\n📥 Recupero tutti i tuoi brani salvati...")
        saved_tracks = self.get_all_saved_tracks()
        
        if not saved_tracks:
            print("❌ Nessun brano salvato trovato.")
            return []
        
        print(f"✓ Recuperati {len(saved_tracks)} brani")
        
        # Step 2: Raggruppa per genere
        genre_groups = self.group_tracks_by_genre(saved_tracks, min_tracks)
        
        if not genre_groups:
            print("\n❌ Nessun genere trovato con abbastanza brani.")
            return []
        
        # Step 3: Mostra riepilogo
        print(f"\n" + "="*70)
        print("📊 RIEPILOGO GENERI")
        print("="*70)
        
        sorted_genres = sorted(genre_groups.items(), key=lambda x: len(x[1]), reverse=True)
        
        for genre, tracks in sorted_genres:
            print(f"  • {genre}: {len(tracks)} brani")
        
        total_tracks = sum(len(tracks) for tracks in genre_groups.values())
        print(f"\nTotale: {len(genre_groups)} playlist da creare con {total_tracks} brani")
        print("="*70)
        
        # Step 4: Conferma dall'utente
        confirm = input("\n✨ Procedere con la creazione delle playlist? (s/n): ").lower()
        
        if confirm != 's':
            print("❌ Operazione annullata.")
            return []
        
        # Step 5: Crea le playlist
        print("\n🎵 Creazione playlist in corso...\n")
        
        created_playlists = []
        
        for i, (genre, tracks) in enumerate(sorted_genres, 1):
            try:
                # Nome e descrizione della playlist
                playlist_name = f"My {genre} Favorites"
                playlist_description = f"{len(tracks)} {genre.lower()} tracks from my liked songs - Auto-generated"
                
                # Crea la playlist
                print(f"[{i}/{len(sorted_genres)}] Creo '{playlist_name}'...")
                playlist = self.create_playlist(playlist_name, playlist_description, make_public)
                
                # Aggiungi i brani
                track_uris = [track['uri'] for track in tracks]
                self.add_tracks_to_playlist(playlist['id'], track_uris)
                
                created_playlists.append(playlist)
                
                # Piccola pausa tra playlist
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Errore nella creazione della playlist '{genre}': {e}")
                continue
        
        # Step 6: Riepilogo finale
        print("\n" + "="*70)
        print("✅ COMPLETATO!")
        print("="*70)
        print(f"\n🎉 Create {len(created_playlists)} playlist con successo!")
        
        for playlist in created_playlists:
            print(f"  • {playlist['name']}")
            print(f"    {playlist['external_urls']['spotify']}")
        
        print("\n💡 Apri Spotify per vedere le tue nuove playlist!")
        print("="*70)
        
        return created_playlists

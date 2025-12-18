# Spotify Search Tool

Uno strumento Python per interagire con Spotify: cerca artisti e canzoni, visualizza i tuoi brani preferiti, top artisti/brani e playlist, e crea playlist personalizzate, anche automaticamente divise per genere.

---

## Funzionalità principali

- 🔍 **Cerca artisti**  
- 🎵 **Cerca canzoni**  
- 💾 **Visualizza brani salvati**  
- 📈 **Visualizza top brani e top artisti**  
- 📂 **Visualizza le tue playlist**  
- ➕ **Crea nuove playlist**  
- 🎨 **Crea playlist dai top brani, dai brani salvati o divise per genere automaticamente**  

---

## Requisiti

- Python 3.8+  
- Libreria `spotipy` (o qualsiasi libreria che usi `SpotifyClient`)  
- Accesso a [Spotify for Developers](https://developer.spotify.com/)

---

## Configurazione

1. Crea un'app su [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Inserisci come URI di reindirizzamento: 'http://127.0.0.1:8888/callback'
3. Recupera le credenziali:
   - `CLIENT_ID`
   - `CLIENT_SECRET`  
4. Creare un file .env con le credenziali come in .env.example

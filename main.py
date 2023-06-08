import streamlit as st
import spotify

def text_finder(txt):
    a = txt.find("https://open.spotify.com")
    txt = txt[a:]
    return txt

def downloader(link, type):
    if type == 'AL':
        ITEMS = spotify.album(link)
    elif type == 'AR':
        ITEMS = spotify.artist(link)
    elif type == 'PL':
        ITEMS = spotify.playlist(link)
    else:
        ITEMS = []

    MESSAGE = ""
    COUNT = 0
    for song in ITEMS:
        if type == 'PL':
            song = song['track']
        COUNT += 1
        MESSAGE += f"{COUNT}. {song['name']}\n"

    for song in ITEMS:
        if type == 'PL':
            song = song['track']
        download_song(song['href'])

    return MESSAGE

def download_song(link):
    song = spotify.Song(link)
    song.YTLink()
    try:
        song.YTDownload()
        song.SongMetaData()
        caption = f'Track: {song.trackName}\nAlbum: {song.album}\nArtist: {song.artist}'
        st.audio(open(f'{song.trackName}.mp3', 'rb'), format='audio/mp3', caption=caption)
    except:
        st.error(f'404\n"{song.trackName}" Not Found')

def main():
    st.title('Spotify Downloader')

    st.write('Hi! This is the Spotify Downloader. You can use the commands below.')

    command = st.selectbox('Select a command:', ['Album', 'Artist', 'Single'])

    if command == 'Album':
        album_name = st.text_input('Enter the album name:')
        album_artist = st.text_input('Enter the artist name:')
        if st.button('Download'):
            link = spotify.searchalbum(f"{album_name} - {album_artist}")
            if link:
                result = downloader(link, 'AL')
                st.success(result)
            else:
                st.error('No results found.')

    elif command == 'Artist':
        artist_name = st.text_input('Enter the artist name:')
        if st.button('Download'):
            link = spotify.searchartist(artist_name)
            if link:
                result = downloader(link, 'AR')
                st.success(result)
            else:
                st.error('No results found.')

    elif command == 'Single':
        song_name = st.text_input('Enter the song name:')
        if st.button('Download'):
            link = spotify.searchsingle(song_name)
            if link:
                download_song(link)
            else:
                st.error('No results found.')

if __name__ == '__main__':
    main()


import chardet
from guitarpro import gp5, Song, Track, GPException, NoteType
import guitarpro

from harp_gp.keys import HOLES


def write_song(song: Song, track: Track, file_path: str):
    for measure in track.measures:
        for voice in measure.voices:
            for beat in voice.beats:
                # if not beat.text:
                for note in beat.notes:
                    if note.type == NoteType.normal:
                        beat.text = HOLES.get(note.realValue, '')

    guitarpro.write(song, file_path, encoding=song.encoding)


def get_song(file_path: str) -> Song | None:
    with open(file_path, "rb") as f:
        file_content = f.read()
        encoding = chardet.detect(file_content)['encoding']
    # TODO Подумать над кодировкой, возможно сделать выпадающий список еще один для ручного выбора
    if not encoding:
        encoding = 'cp1252'
    try:
        song = guitarpro.parse(file_path, encoding=encoding)
    except GPException:
        return None
    song.encoding = encoding
    return song


def get_track(song: Song, track_name: str) -> Track | None:
    track_number = int(track_name.split(". ")[0])
    for track in song.tracks:
        if track.number == track_number:
            return track
    return None


def get_tracks(song: Song) -> list[Track]:
    tracks = []
    if song is None:
        return tracks
    for track in song.tracks:
        tracks.append(track)
    # tracks.sort(key=lambda x: x.number)
    return tracks

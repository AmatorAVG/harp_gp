from guitarpro import gp5, Song, Track
import guitarpro

# from guitarpro.models import Song
# from pyguitarpro.models.track import Track
# from pyguitarpro.models.measure import Measure, Voice
# from guitarpro.models import Beat
# from guitarpro.models import Note
# from guitarpro.models import Annotation

# file_path = '../../tracks/test.gp5'
# output_file_path = 'path/to/output/file.gp5'
#
# song = guitarpro.parse(file_path)
# track = song.tracks[0]
#
# for measure in track.measures:
#     for voice in measure.voices:
#         for beat in voice.beats:
#             if beat.text:
#                 beat.text = beat.text + '_1'
#             for note in beat.notes:
#                 print(note)
#
# guitarpro.write(song, file_path)


def get_song(file_path: str) -> Song:
    song = guitarpro.parse(file_path)
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

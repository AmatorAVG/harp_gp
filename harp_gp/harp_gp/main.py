from guitarpro import gp5
import guitarpro
# from guitarpro.models import Song
# from pyguitarpro.models.track import Track
# from pyguitarpro.models.measure import Measure, Voice
# from guitarpro.models import Beat
# from guitarpro.models import Note
# from guitarpro.models import Annotation

file_path = '../../tracks/test.gp5'
output_file_path = 'path/to/output/file.gp5'

song = guitarpro.parse(file_path)
track = song.tracks[0]

for measure in track.measures:
    for voice in measure.voices:
        for beat in voice.beats:
            if beat.text:
                beat.text = beat.text + '_1'
            for note in beat.notes:
                print(note)

guitarpro.write(song, file_path)

import chardet
from guitarpro import Song, Track, GPException, NoteType
import guitarpro

from harp_gp.keys import KEYS, TUNINGS


def sort_expression(expression):
    """Сортирует строку математического выражения в отсортированный вид.

    Args:
        expression: Строка с математическим выражением.

    Returns:
        Отсортированная строка.
    """
    # Разделяем выражение на отдельные элементы
    elements = expression.split()

    # Сортируем элементы по абсолютной величине
    sorted_elements = sorted(
        elements, key=lambda x: abs(int(x.replace("+", "").replace("-", "").replace("'", "").replace("o", "")))
    )

    # Возвращаем отсортированную строку
    return " ".join(sorted_elements)


def write_song(song: Song, track: Track, key: str, tuning: str, file_path: str):
    for measure in track.measures:
        for voice in measure.voices:
            for beat in voice.beats:
                beat_text = ""
                notes_cnt = 0
                for note in beat.notes:
                    if note.type == NoteType.normal:
                        beat_text += (
                            TUNINGS[tuning].get(note.realValue - KEYS[key], "") + " "
                        )
                        notes_cnt += 1
                        if notes_cnt > 1:
                            chord_text = f"({sort_expression(beat_text)})"
                            if chord_text.find("-") >= 0 > chord_text.find("+"):
                                chord_text = f"-{chord_text.replace('-', '')}"
                            elif chord_text.find("+") >= 0 > chord_text.find("-"):
                                chord_text = f"+{chord_text.replace('+', '')}"
                            beat.text = chord_text.replace(" ", "")
                        else:
                            beat.text = beat_text
    guitarpro.write(song, file_path, encoding=song.encoding)


def get_song(file_path: str) -> Song | None:
    with open(file_path, "rb") as f:
        file_content = f.read()
        encoding = chardet.detect(file_content)["encoding"]
    # TODO Подумать над кодировкой, возможно сделать выпадающий список еще один для ручного выбора
    if not encoding:
        encoding = "cp1252"
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

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from harp_gp.keys import KEYS, TUNINGS
from harp_gp.parser import get_song, get_tracks, get_track, write_song


class TrackDropDown(DropDown):
    def select(self, data):
        super().select(data)
        root = self.parent.children[1]
        root.ids.track_lbl.text = data
        root.track = get_track(root.song, data)


class KeyDropDown(DropDown):
    def select(self, data):
        super().select(data)
        root = self.parent.children[1]
        root.key = data
        root.ids.select_key_btn.text = "Key: " + data


class TuningDropDown(DropDown):
    def select(self, data):
        super().select(data)
        root = self.parent.children[1]
        root.tuning = data
        root.ids.select_tuning_btn.text = "Tuning: " + data


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):

    key = "C"
    tuning = "Standard Richter"
    song = None
    track = None
    tracks = []
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    select_track_btn = ObjectProperty(None)
    file_lbl = ObjectProperty(None)
    track_lbl = ObjectProperty(None)
    new_file = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.song = get_song(filename[0]) if filename else None
        self.ids.file_lbl.text = filename[0] if filename else "Open gp file!"
        self.ids.track_lbl.opacity = self.ids.select_track_btn.opacity = (
            1 if filename and self.song else 0
        )
        if self.song:
            self.tracks = get_tracks(self.song)
            self.ids.track_lbl.text = "Select track!"
        elif filename:
            self.ids.file_lbl.text = "Unsupported file!"
        self.dismiss_popup()

    def save(self, path, filename):
        if filename:
            write_song(self.song, self.track, self.key, self.tuning, filename)

        self.dismiss_popup()

    def show_track_dropdown(self, instance):
        # Создаем DropDown
        dropdown = TrackDropDown()

        # Добавляем кнопки в DropDown
        for track in self.tracks:
            track_btn = Button(
                text=f"{track.number}. {track.name}", size_hint_y=None, height=44
            )
            track_btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(track_btn)
        # TODO Переопределить select чтобы парсить уже конретный трек
        dropdown.open(instance)

    def show_key_dropdown(self, instance):
        dropdown = KeyDropDown()
        for key in KEYS:
            key_btn = Button(text=key, size_hint_y=None, height=44)
            key_btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(key_btn)
        dropdown.open(instance)

    def show_tuning_dropdown(self, instance):
        dropdown = TuningDropDown()
        for tuning in TUNINGS:
            tuning_btn = Button(text=tuning, size_hint_y=None, height=44)
            tuning_btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(tuning_btn)
        dropdown.open(instance)


class Editor(App):
    pass


Factory.register("Root", cls=Root)
Factory.register("LoadDialog", cls=LoadDialog)
Factory.register("SaveDialog", cls=SaveDialog)


if __name__ == "__main__":
    Editor().run()

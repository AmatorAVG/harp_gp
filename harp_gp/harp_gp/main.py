from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from harp_gp.parser import get_song, get_tracks, get_track


class TrackDropDown(DropDown):
    def select(self, data):
        super().select(data)
        root = self.parent.children[1]

        root.ids.track_lbl.text = data
        root.track = get_track(root.song, data)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):

    song = None
    track = None
    tracks = []
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    select_track_btn = ObjectProperty(None)
    file_lbl = ObjectProperty(None)
    track_lbl = ObjectProperty(None)

    # def toggle_label(self):
    #     if self.ids.track_select.opacity == 0:
    #         self.ids.track_select.opacity = 1  # Показываем метку
    #     else:
    #         self.ids.track_select.opacity = 0  # Скрываем метку

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
        # with open(os.path.join(path, filename[0])) as stream:
        #     self.text_input.text = stream.read()
        self.ids.select_track_btn.opacity = 1
        self.ids.file_lbl.text = filename[0] if filename else "Open gp file!"
        self.ids.track_lbl.opacity = 1 if filename else 0
        self.ids.track_lbl.text = "Select track!"
        self.song = get_song(filename[0]) if filename else None
        self.tracks = get_tracks(self.song)

        self.dismiss_popup()

    def save(self, path, filename):
        # with open(os.path.join(path, filename), 'w') as stream:
        #     stream.write(self.text_input.text)

        self.dismiss_popup()

    def show_dropdown(self, instance):
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


class Editor(App):
    pass


Factory.register("Root", cls=Root)
Factory.register("LoadDialog", cls=LoadDialog)
Factory.register("SaveDialog", cls=SaveDialog)


if __name__ == "__main__":
    Editor().run()

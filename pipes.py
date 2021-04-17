from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.image import Image
from kivy.clock import Clock
import numpy as np

class Pipe(Widget):
    pipe_gap = NumericProperty(200)

    pipe_cap = NumericProperty(20)
    pipe_cap_width = NumericProperty(64)

    pipe_center = NumericProperty(0)

    btm_body_pos = NumericProperty(0)
    btm_cap_pos = NumericProperty(0)

    top_body_pos = NumericProperty(0)
    top_cap_pos = NumericProperty(0)

    pipe_body_texture = ObjectProperty(None)
    btm_pipe_coords = ListProperty( (0, 0, 1, 0, 1, 1, 0, 1) )
    top_pipe_coords = ListProperty( (0, 0, 1, 0, 1, 1, 0, 1) )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pipe_body_texture = Image(source = 'pipe_jay_body.png').texture
        self.pipe_body_texture.wrap = 'repeat'

    # Widget Class Function
    def on_size(self, *args):
        btm_half_body = self.btm_cap_pos - self.btm_body_pos
        
        self.btm_pipe_coords[5] = btm_half_body/20.0
        self.btm_pipe_coords[7] = btm_half_body/20.0
        
        top_half_body = self.top - self.top_body_pos
        self.top_pipe_coords[5] = top_half_body/20.0
        self.top_pipe_coords[7] = top_half_body/20.0

    def on_pipe_center(self, *args):
        Clock.schedule_once(self.on_size, 0)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
import numpy as np
from kivy.properties import NumericProperty

from pipes import Pipe

num_pipes = 5
pipe_dist = Window.width / (num_pipes - 1)

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        '''
        Gets texture version of cloud image
        '''
        self.cloud_texture = Image(source = 'cloud.png').texture
        self.floor_texture = Image(source = 'flappyJayFloor.png').texture

        '''
        Allows clouds to repeat through out the sky
        '''
        
        self.cloud_texture.wrap = 'repeat'
        self.floor_texture.wrap = 'repeat'

        '''
        Determines how big the cloud size is before being repeated
        '''
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_effect(self, elapsed_time):
        '''
        Updates the position of the cloud, and the modulo so it can be wrapped
        '''
        self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + elapsed_time) % Window.width, self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ( (self.floor_texture.uvpos[0] + elapsed_time / 2.0) % Window.width, self.floor_texture.uvpos[1])

        '''
        Draws the texture over and over
        '''
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)


class FlappyApp(App):
    amount_pipes = []
    def on_start(self):
        '''
        Acts as a frame rate
        ''' 
        Clock.schedule_interval(self.root.ids.background.scroll_effect, 1/60.0)
    
    def start_game(self):
        
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = np.random.randint(pipe.floor_height + 100, self.root.height - 100)
            pipe.size_hint = None, None
            pipe.pos = (i * pipe_dist, pipe.floor_height)
            pipe.size = (pipe.pipe_cap_width, self.root.height - pipe.floor_height)

            self.amount_pipes.append(pipe)  
            self.root.add_widget(pipe)

        Clock.schedule_interval(self.scroll_pipes, 1/60.0)

    def scroll_pipes(self, elapsed_time):
        for pipes in self.amount_pipes:
            pipes.x -= elapsed_time * 100
        
        pipe_xs_list = list(map(lambda pipes: pipes.x, self.amount_pipes))
        last_pipe = max(pipe_xs_list)
        if last_pipe <= Window.width - pipe_dist:
            first_pipe = self.amount_pipes[pipe_xs_list.index(min(pipe_xs_list))]
            first_pipe.x = Window.width





if __name__ == '__main__':
    FlappyApp().run()
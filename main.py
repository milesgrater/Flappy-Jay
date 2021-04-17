from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from random import randint
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from pipes import Pipe
import database_code

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
    
    def on_size(self, *args):
        '''
        Determines how big the cloud size is before being repeated
        '''
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

class Jay(Image):
    jay_velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "flappy-jay-bird.png"
        self.jay_velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "flappy-jay-bird.png"
        super().on_touch_up(touch)

class FlappyApp(App):
    amount_pipes = []
    jay_gravity = 300
    was_colliding = False

    def flap_wings(self, elapsed_time):
        jay = self.root.ids.jay
        jay.y = jay.y + jay.jay_velocity * elapsed_time
        jay.jay_velocity = jay.jay_velocity - self.jay_gravity * elapsed_time
        self.collision()

    def collision(self):
        jay = self.root.ids.jay
        is_colliding = False
        for pipe in self.amount_pipes:
            if pipe.collide_widget(jay):
                is_colliding = True
                if jay.y < (pipe.pipe_center - pipe.pipe_gap / 2.0):
                    self.game_over()
                if jay.top > (pipe.pipe_center + pipe.pipe_gap / 2.0):
                    self.game_over()
        if jay.y < 112:
            self.game_over()
        if jay.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.root.ids.player_score.text = str(int(self.root.ids.player_score.text) + 1)

        self.was_colliding = is_colliding

    def game_over(self):
        player_score = self.root.ids.player_score.text
        username = 'Alabama'
        database_code.addScore(username, player_score)
        self.root.ids.jay.pos = (20, (self.root.height - 112) / 2.0)
        for pipe in self.amount_pipes:
            self.root.remove_widget(pipe)
        self.frames.cancel()
        self.root.ids.startbutton.disabled = False
        self.root.ids.startbutton.opacity = 1



    def next_frame(self, elapsed_time):
            self.flap_wings(elapsed_time)
            self.scroll_pipes(elapsed_time)
            self.root.ids.background.scroll_effect(elapsed_time)

    
    def start_game(self):
        self.root.ids.player_score.text = "0"
        self.was_colliding = False
        self.amount_pipes = []
        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)
        num_pipes = 5
        pipe_dist = Window.width / (num_pipes - 1)
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(112 + 100, self.root.height - 100)
            pipe.size_hint = (None, None)
            pipe.pos = (Window.width + i * pipe_dist, 112)
            pipe.size = (64, self.root.height - 112)

            self.amount_pipes.append(pipe)  
            self.root.add_widget(pipe)

    def scroll_pipes(self, elapsed_time):
        for pipes in self.amount_pipes:
            pipes.x -= elapsed_time * 100
        
        num_pipes = 5
        pipe_dist = Window.width / (num_pipes - 1)

        pipe_xs_list = list(map(lambda pipe: pipe.x, self.amount_pipes))
        last_pipe = max(pipe_xs_list)
        if last_pipe <= Window.width - pipe_dist:
            first_pipe = self.amount_pipes[pipe_xs_list.index(min(pipe_xs_list))]
            first_pipe.x = Window.width





if __name__ == '__main__':
    FlappyApp().run()
    cursor.close()
    connection.close()
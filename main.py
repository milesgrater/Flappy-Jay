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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from pipes import Pipe
import database_code


class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        """

        Gets texture version of cloud image

        """       
       
        self.cloud_texture = Image(source = 'cloud.png').texture
        self.floor_texture = Image(source = 'flappyJayFloor.png').texture

        """

        Allows clouds to repeat through out the sky

        """
        
        self.cloud_texture.wrap = 'repeat'
        self.floor_texture.wrap = 'repeat'

        self.cloud_texture.uvsize = ( (Window.width / self.cloud_texture.width, -1))

    def scroll_effect(self, elapsed_time):

        """

        Updates the position of the cloud, and the modulo so it can be 
        
        """
        self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + elapsed_time) % Window.width, self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ( (self.floor_texture.uvpos[0] + elapsed_time / 2.0) % Window.width, self.floor_texture.uvpos[1])

        """
        Draws the texture over and over

        """
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)
    
    def on_size(self, *args):

        """
        Determines how big the cloud size is before being repeated

        """
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

class Jay(Image):

    """
    
    Creates Jay in game and allows bird to go up and down on touch

    """

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

    def show_leaderboard(self):

        """

        Shows leaderboard 

        """

        lb_grid = GridLayout(cols = 2)
        lb_box = BoxLayout(orientation = 'vertical')
        lb_results = database_code.getUsernameScore_Sort()

        if (lb_results == []):
            no_entries_label = Label(text = 'There are no current entries in the leaderboard!')
            second_entries_label = Label(text = 'Play a game to enter your score!')
            return_btn_box = Button(text = 'Return to Main Menu', size_hint = (.5, .4), pos_hint = {"center_x": .5, "center_y": .5})

            lb_box.add_widget(no_entries_label)
            lb_box.add_widget(second_entries_label)
            lb_box.add_widget(return_btn_box)

            lb_box_popup = Popup(title = 'Leaderboard',
                                content = lb_box,
                                size_hint = (None, None),
                                size = (400, 400)
                               )
            return_btn_box.bind(on_press = lb_box_popup.dismiss)
            lb_box_popup.open()
        else:
            for result in lb_results:
                temp = result
                lb_grid.add_widget(Label(text = str(temp[0]), font_size = 13))
                lb_grid.add_widget(Label(text = str(temp[1]), font_size = 13))

            return_btn_float = Button(text = 'Return to Main Menu', size_hint = (.3, .2), pos_hint = {"center_x": .5, "center_y": .5})
            lb_grid.add_widget(return_btn_float)

            lb_popup = Popup(title = 'Leaderboard',
                            content = lb_grid,
                            size_hint = (None, None),
                            size = (400, 400)
                            )
            return_btn_float.bind(on_press = lb_popup.dismiss)
            lb_popup.open()

    def flap_wings(self, elapsed_time):

        """ 

        Changes y value of the jay

        """

        jay = self.root.ids.jay
        jay.y = jay.y + jay.jay_velocity * elapsed_time
        jay.jay_velocity = jay.jay_velocity - self.jay_gravity * elapsed_time
        self.collision()

    def collision(self):

        """

        Collision Function for Jay

        """

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

        """

        Game Over Function

        """

        self.player_score = self.root.ids.player_score.text
        game_over_box = FloatLayout()
        self.game_over_im = Image(source = 'Game Over.png')
        self.game_over_return_btn = Button(text = 'Return to Main Menu', size_hint = (.5, .2), pos_hint = {"center_x" : .5, "center_y" : .1, "bottom": 1})
        self.input_label = Label(text = 'Enter a username: ', pos_hint = {"center_x": .3, "center_y": .96})
        self.username_input = TextInput(text = '', multiline = False, size_hint = (.2, .1), pos_hint = {"center_x": .5, "top": 1})
        self.add_username_btn = Button(text = 'Submit Username', size_hint = (.2, .1), pos_hint = {"center_x" : .75, "center_y" : .95})
        game_over_box.add_widget(self.game_over_im)
        game_over_box.add_widget(self.game_over_return_btn)
        game_over_box.add_widget(self.input_label)
        game_over_box.add_widget(self.username_input)
        game_over_box.add_widget(self.add_username_btn)
        game_over_popup = Popup(
            title = 'Game Over',
            content = game_over_box,
            size = (100, 100),
            auto_dismiss = False
        )
        self.game_over_return_btn.bind(on_press = game_over_popup.dismiss)
        self.add_username_btn.bind(on_press = self.press)

        game_over_popup.open()

        self.root.ids.jay.pos = (20, (self.root.height - 112) / 2.0)
        for pipe in self.amount_pipes:
            self.root.remove_widget(pipe)

        self.frames.cancel()
        self.root.ids.startbutton.disabled = False
        self.root.ids.startbutton.opacity = 1
        self.root.ids.leaderboardbutton.disabled = False
        self.root.ids.leaderboardbutton.opacity = 1
        self.root.ids.player_score.text = ""
        self.root.ids.title.opacity = 1
        self.root.ids.jay.opacity = 0
    
    def press(self, instance):

        """

        Submits username and score to database

        """

        username = self.username_input.text
        score = self.player_score
        database_code.addScore(username, score)

        self.username_input.text = ''



    def next_frame(self, elapsed_time):

            """ 
            
            Defines Frames in game

            """

            self.flap_wings(elapsed_time)
            self.scroll_pipes(elapsed_time)
            self.root.ids.background.scroll_effect(elapsed_time)
    
    def on_start(self):

        """

        Intialization of the game

        """

        self.root.ids.player_score.text = ""
        self.root.ids.title.opacity = 1
        self.root.ids.jay.opacity = 0


    def start_game(self):

        """

        Creates Pipes in game
        Sets up game enviroment

        """

        self.root.ids.player_score.text = "0"
        self.root.ids.leaderboardbutton.disabled = True
        self.root.ids.leaderboardbutton.opacity = 0
        self.was_colliding = False
        self.root.ids.title.opacity = 0
        self.root.ids.jay.opacity = 1
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

        """

        Makes pipes keep appearing and scrolling throughout game

        """

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
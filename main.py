from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock


class Background(Widget):
    cloud_texture = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Gets texture version of cloud image
        self.cloud_texture = Image(source = 'cloud.png').texture

        # Allows clouds to repeat through out the sky
        self.cloud_texture.wrap = 'repeat'

        # Determines how big the cloud size is before being repeated
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)

    def scroll_textures(self, elasped_time):
        # Updates the position of the cloud, and the modulo so it can be wrapped
        self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + elasped_time) % Window.width ,self.cloud_texture.uvpos[1])

        # Draws the texture over again
        texture = self.property('cloud_texture')
        texture.dispatch(self)

    pass


class FlappyApp(App):
    def on_start(self):
        # Acts as a frame rate 
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)
        
    pass

    
FlappyApp().run()
import os

# Allows this to be run from a blank CMD instance for Mari
if os.getenv("USERNAME") == "energ":
    os.chdir("F:\\Game Jam Workspace\\Secrets")

from DSEngine import *
from pygame import Vector2
from pygame.display import update
#from classes import dialogue
#from classes import sound_utils
from functools import partial
import glob
import re

# window = Window(fps=120, size=(1280, 720))
# type2d = Type2D("GUI")
# rect = Rect2D(position=Vector2(150, 55), size=Vector2(5, 5))
# image1 = Image2D(filename="Test.png", position=Vector2(150, 55))
# image2 = Image2D(filename="Test1.png", position=Vector2(150, 55))
# spritesheet1 = Spritesheet(image1, image1, image1, image1, image1, image2, image2, image2, image2, image2)
# spritesheet2 = Spritesheet(image2, image1)
# animationsheet = AnimationSheet(default=image1, normal=spritesheet1, back=spritesheet2)
# sprite = AnimatedSprite2D(sheet=animationsheet, position=Vector2(150, 55))
# audio_man = AudioManager()
# type2d.init(window)
# rect.init(window)
# sprite.init(window)
# #print(audio_man.tracks)
# while window.running:
    # keys = window.frame()
    # #print(sprite.is_colliding_with(rect))
    # acc = Vector2(0.0, 0.0)
    # acc.x = (keys[key_to_scancode("d")]-keys[key_to_scancode("a")])*window.delta_s*200
    # acc.y = (keys[key_to_scancode("s")]-keys[key_to_scancode("w")])*window.delta_s*200
    # if not pygame.mixer.music.get_busy() and not sprite.playing and acc != Vector2(0.0, 0.0):
        # audio_man.play("beep")
    # sprite.move(acc)
    # update()

class Player(AnimatedSprite2D):
    def __init__(self,**args):

        super().__init__(**args)
        self.debug=True
    def render(self,window:Window):
        window.current_camera.position=self.position-tuple(divide/2 for divide in window.size)
        super().render(window)

class HookedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listeners = []

    def add_listener(self, func):
        self._listeners.append(func)

    def remove_listener(self, func):
        self._listeners.remove(func)

    def on_change(self, item_id, old_value, new_value):
        for listener in self._listeners:
            listener(item_id, old_value, new_value)

    def __setitem__(self, key, value):
        old_value = self.get(key, None)
        
        if old_value != value:
            self.on_change(key, old_value, value)
        
        super().__setitem__(key, value)

class Main:
    def __init__(self, fps, window_width, window_height):
        self.fps = fps
        self.window_width = window_width
        self.window_height = window_height
        self.window = Window(fps=self.fps, size=(self.window_width, self.window_height))
        
        self.player_state = HookedDict(direction = "down", coords = (self.window_width // 2, self.window_height // 2), state = "idle")
        self.player_state.add_listener(self.update_player)
        
        self.__postinit__()
        
        
        self.__main__()
        
    def update_player(self, item_id, old_value, new_value): # When the self.player_state dictionary is updated, this method is called. Allows management of the players state in a single central area.
        if item_id == "coords":
            #self.player.position = pygame.Vector2(new_value[0], new_value[1])
            self.player.move_to(pygame.Vector2(new_value[0], new_value[1])) # move is using velocity and not position so created move_to
            #print(f"Player was moved to x={new_value[0]}, y={new_value[1]}")
        elif item_id == "direction":
            self.player.play_sheet(self.player_state["state"] + "_" + new_value)
        elif item_id == "state":
            self.player.play_sheet(new_value + "_" + self.player_state["direction"])
        else:
            pass
            
    def convert_paths_to_images(self, paths_list):
        images_list = []
        for path in paths_list:
            new_img = Image2D(path)
            new_img.init(self.window)
            images_list.append(new_img)
        return images_list
    

    def __postinit__(self):
        self.type2d = Type2D("GUI")
        self.type2d.init(self.window)
        
        
        self.player_frame_time = 1
        self.player_default = Image2D(filename=f"assets/textures/player/idle_{self.player_state['direction']}_0000.png", position=Vector2(*self.player_state["coords"])) # why does an image have a position? does this not represent an abstract idea of an image? i guess i'll find out somehow

        ### PLAYER IDLE SHEETS

        #TODO: Change these to non-glob things

        self.idle_up_sheet = Spritesheet(self.player_frame_time, Image2D("assets/textures/player/idle_up_0000.png"))
        self.idle_down_sheet = Spritesheet(self.player_frame_time, Image2D("assets/textures/player/idle_down_0000.png"))
        self.idle_left_sheet = Spritesheet(self.player_frame_time, Image2D("assets/textures/player/idle_left_0000.png"))
        self.idle_right_sheet = Spritesheet(self.player_frame_time, Image2D("assets/textures/player/idle_right_0000.png"))

        ### PLAYER WALKING SHEETS
        self.walking_up_sheet = Spritesheet(self.player_frame_time, Image2D("assets/textures/player/walk_up_0000.png"), Image2D("assets/textures/player/walk_up_0002.png"), Image2D("assets/textures/player/walk_up_0004.png"), Image2D("assets/textures/player/walk_up_0006.png"))
        self.walking_down_sheet = Spritesheet(self.player_frame_time,  Image2D("assets/textures/player/walk_down_0000.png"), Image2D("assets/textures/player/walk_down_0002.png"), Image2D("assets/textures/player/walk_down_0004.png"), Image2D("assets/textures/player/walk_down_0006.png"))
        self.walking_left_sheet = Spritesheet(self.player_frame_time,  Image2D("assets/textures/player/walk_left_0000.png"), Image2D("assets/textures/player/walk_left_0002.png"), Image2D("assets/textures/player/walk_left_0004.png"), Image2D("assets/textures/player/walk_left_0006.png"))
        self.walking_right_sheet = Spritesheet(self.player_frame_time,  Image2D("assets/textures/player/walk_right_0000.png"), Image2D("assets/textures/player/walk_right_0002.png"), Image2D("assets/textures/player/walk_right_0004.png"), Image2D("assets/textures/player/walk_right_0006.png")) #walking != walk

        #NOTE: still doesn't render even with direct paths uff

        print(f"Postinit - type of asset is {type(Image2D('assets/textures/player/walk_right_0000.png'))}")
        # Postinit - type of asset is <class 'DSEngine.etypes.Image2D'>

        ### PLAYER ANIMATION SHEET
        self.player_animation_sheet = AnimationSheet(
            default=self.player_default,
            idle_up=self.idle_up_sheet,
            idle_down=self.idle_down_sheet,
            idle_left=self.idle_left_sheet,
            idle_right=self.idle_right_sheet,
            walking_up=self.walking_up_sheet,
            walking_down=self.walking_down_sheet,
            walking_left=self.walking_left_sheet,
            walking_right=self.walking_right_sheet
        )
        
        # Creating the player using all that stuff
        self.player = Player(sheet=self.player_animation_sheet, position=Vector2(*self.player_state["coords"]))
        
        self.player.init(self.window)# Mari u forgot to init the player

        Rect2D().init(self.window)
    
    def change_player_state(self, new_direction=None, offset_x=0, offset_y=0, new_state = None):
        if new_direction:
            self.player_state["direction"] = new_direction
            self.player.play_sheet(self.player_state["state"] + "_" + self.player_state["direction"])
            print(self.player_state["state"]+"_"+self.player_state["direction"])
        
        if (not offset_x == 0) or (not offset_y == 0):
            self.player_state["coords"] = (self.player_state["coords"][0] + offset_x, self.player_state["coords"][1] + offset_y)
            print((offset_x,offset_y,self.player_state["coords"]))
        if new_state:
            self.player.play_sheet(self.player_state["state"] + "_" + self.player_state["direction"])
        print(self.player.position)
    
    def __main__(self):
        key_actions = {
            pygame.key.key_code('w'): partial(self.change_player_state, offset_y=-2, new_direction="up", new_state="walking"),
            pygame.key.key_code('s'): partial(self.change_player_state, offset_y=2, new_direction="down", new_state="walking"),
            pygame.key.key_code('a'): partial(self.change_player_state, offset_x=-2, new_direction="left", new_state="walking"),
            pygame.key.key_code('d'): partial(self.change_player_state, offset_x=2, new_direction="right", new_state="walking"),
            pygame.K_UP: partial(self.change_player_state, offset_y=-2, new_direction="up", new_state="walking"),
            pygame.K_DOWN: partial(self.change_player_state, offset_y=2, new_direction="down", new_state="walking"),
            pygame.K_LEFT: partial(self.change_player_state, offset_x=-2, new_direction="left", new_state="walking"),
            pygame.K_RIGHT: partial(self.change_player_state, offset_x=2, new_direction="right", new_state="walking")
        }

        while self.window.running:
            keys = self.window.frame()
            
            for action_key, callable in key_actions.items():
                if keys[action_key]:
                    callable()
                    self.player.current_sheet.sheet[self.player.frame].render(self.window)
                    #print(self.player.current_sheet.sheet[self.player.frame].position)
             
main = Main(120, 1280, 720)
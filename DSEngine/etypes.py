import pygame, sys
import psutil, time
from .camera import Camera2D
from .tiles import TileMap

SG_needed=False #Set to True when you need PySimpleGui

if SG_needed:
    import PySimpleGUI as sg

def key_to_scancode(key: str):
    return pygame.key.key_code(key)

class Window:
    def __init__(self, fps=60, title="DSEngine Window", size: tuple=(800, 600), bg: tuple=(0, 0, 0), icon=pygame.image.load("default.icon.png"), zoom=pygame.Vector2(1,1), profiler=False):
        self.layers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[],
                       7:[], 8:[], 9:[], 10:[], "GUI":[]}
        print("Window init")
        self.fps, self.title, self.size, self.bg, self.icon, self.zoom = fps, title, size, bg, icon, zoom
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.delta_s = 0
        self.elapsed_ms = 0
        self.seconds = 0
        self.no_update = False
        self.current_camera = Camera2D(position=pygame.Vector2(0, 0))
        self.pressed_keys = pygame.key.get_pressed()
        self.prev_keys=pygame.key.ScancodeWrapper()
        self.prof = profiler
        if self.prof:
            self.cpu_usage = 0
            self.memory_info = 0
            self.fps = 0
            layout = [
                [sg.Text("CPU Usage:", size=(15, 1)), sg.Text(size=(10, 1), key="-CPU-")],
                [sg.Text("Memory Usage:", size=(15, 1)), sg.Text(size=(10, 1), key="-MEM-")],
                [sg.Text("FPS:", size=(15, 1)), sg.Text(size=(10, 1), key="-FPS-")],
            ]
            # Create PySimpleGUI Window
            self.profiler_window = sg.Window("Profiler", layout, finalize=True, keep_on_top=True)
        self.bg_rect = pygame.Rect(0, 0, size[0], size[1])
        if bg != (0, 0, 0):
            self.surface.fill(bg)
            pygame.display.flip()
        self.running = True
        
    
    def update_profiler_metrics(self):
        global cpu_usage, memory_info, fps
        self.cpu_usage = psutil.cpu_percent()
        try: self.memory_info = psutil.virtual_memory().percent
        except: pass
        self.fps = int(self.clock.get_fps())
    
    def render_profiler(self):
        self.update_profiler_metrics()
        # Update the Profiler Window in PySimpleGUI
        self.profiler_window["-CPU-"].update(f"{self.cpu_usage}%")
        self.profiler_window["-MEM-"].update(f"{self.memory_info}%")
        self.profiler_window["-FPS-"].update(f"{self.fps}")
        event, values = self.profiler_window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            self.profiler_window.close()
            sys.exit()

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return pygame.Vector2(x, y)
    
    def frame(self):
        self.prev_keys=self.pressed_keys
        global keys
        self.delta = self.clock.tick(self.fps)
        self.delta_s = self.delta/1000
        self.elapsed_ms += self.delta
        self.seconds = self.elapsed_ms/100
        if not self.no_update:
            pygame.draw.rect(self.surface, self.bg, self.bg_rect)
        for event in pygame.event.get():      
            if event.type == pygame.QUIT: 
                self.running = False
                pygame.quit()
                sys.exit()
        for j in range(1, 10+1):
            #print(j)
            for i in self.layers[j]:
                i.render(self)
        for i in self.layers["GUI"]:
            i.render(self)
        if self.zoom!=pygame.Vector2(1,1):
            surface=pygame.transform.scale(self.surface,(self.size[0]*self.zoom.x, self.size[1]*self.zoom.y))
            self.surface.blit(surface,(0,0))
        if not self.no_update:
            pygame.display.flip()
            pygame.display.update()
        if self.prof:
            self.render_profiler()
        self.pressed_keys = pygame.key.get_pressed()
        return self.pressed_keys
    
    def key_just_pressed(self,scancode:int):
        return self.pressed_keys[scancode] and not self.prev_keys[scancode]
        

class Type2D:
    def __init__(self, layer=1, position=pygame.Vector2(0.0, 0.0), rotation=0.0):
        self.layer = layer
        self.position = position
        self.rotation = rotation
    
    def init(self, window: Window):
        window.layers[self.layer].append(self)
        self.window = window
    
    def remove(self, window: Window):
        window.layers[self.layer].remove(self)
        self.window = None
    
    def render(self, window: Window):
        pass

class Rect2D(Type2D):
    def __init__(self, layer=1, position=pygame.Vector2(0.0, 0.0), color=(255, 255, 255), size=pygame.Vector2(100.0, 100.0),offset=pygame.Vector2(0,0), invisible=False):
        self.sprite = pygame.sprite.Sprite()
        self.visible=True
        self.collision=True
        self.window = None
        self.layer = layer
        self.position = position
        self.color = color
        self.size = size
        self.collisionoffset=offset
        self.area = False
        self.prev_pos = self.position
        self.invisible = invisible
        self.rect = pygame.Rect(position.x+self.collisionoffset.x, position.y+self.collisionoffset.y, size.x, size.y)
        self.collision_sides = {"left":False, "right":False,
                                "bottom":False, "top":False}
        self.tweens=[]
        super().__init__(layer=self.layer, position=self.position)

    class Tween:
        def __init__(self,handler,start,end,time) -> None:
            self.start=start
            self.end=end
            self.handler=handler
            self.time=time
            self.rem_time=time
        def run(self,fps):
            self.rem_time-=1/fps
            process=self.rem_time/self.time
            difference=self.end-self.start
            val=(difference*process)+self.start
            self.handler(val)

    def tween(self,handler,start,end,time):
        self.tweens.append(self.Tween(handler,start,end,time))

    def is_on_floor(self):
      return self.collision_sides["bottom"]

    def is_on_ceiling(self):
      return self.collision_sides["top"]

    def detect_collision(self, i):
        if i != self and isinstance(i,Rect2D) and not i.area and i.collision:
            side = self.get_collision_side(i)
            if side != None:
                self.collision_sides[side] = True

    
    def detect_collisions(self):
        if self.collision and self.window != None:
            self.collision_sides = {"left":False, "right":False,
                                    "bottom":False, "top":False}
            for i in self.window.layers[self.layer]:
                if isinstance(i,TileMap):
                    i.collisions(self)
                else:
                    if i != self and "type(i) == Rect2D" and not i.area and i.collision:
                        side = self.get_collision_side(i)
                        if side != None:
                            self.collision_sides[side] = True
        
    def get_collision_side(self, rect2):
        if self.is_colliding_with(rect2):
            dr = abs(self.rect.right - rect2.rect.left)
            dl = abs(self.rect.left - rect2.rect.right)
            db = abs(self.rect.bottom - rect2.rect.top)
            dt = abs(self.rect.top - rect2.rect.bottom)
            if min(dl, dr) < min(dt, db):
                direction = "left" if dl < dr else "right"
            else:
                direction = "bottom" if db < dt else "top"
            return direction
        else:
            return None
    
    def is_colliding_with(self, rect2: Type2D):
        return self.rect.colliderect(rect2.rect)
    
    def render(self, window: Window):
        if self.visible:
            self.window = window
            self.detect_collisions()
            self.rect.topleft = (self.position.x+self.collisionoffset.x-window.current_camera.position.x, self.position.y+self.collisionoffset.y-window.current_camera.position.y)
            if not self.invisible: pygame.draw.rect(window.surface, self.color, self.rect)
            super().render(window)
            for e in self.tweens:
                e.run()
    
    def is_moving(self):
        return self.prev_pos == self.position
    
    def move(self, vec: pygame.Vector2):
        oldpos = self.position
        oldtl = self.rect.topleft
        vecx = vec.x
        vecy = vec.y
        self.position = pygame.Vector2(self.position.x+vecx, self.position.y+vecy)
        self.rect.topleft = (self.position.x, self.position.y)
        if vecx > 0:
            if not self.collision_sides["right"]:
                pass
            else:
                self.position.x = oldpos.x
                self.rect.topleft = (oldpos.x, self.rect.topleft[1])
        else:
            if not self.collision_sides["left"]:
                vecx = vecx
            else:
                self.position.x = oldpos.x
                self.rect.topleft = (oldpos.x, self.rect.topleft[1])
        if vecy > 0:
            if not self.collision_sides["bottom"]:
                pass
            else:
                self.position.y = oldpos.y
                self.rect.topleft = (self.rect.topleft[0], oldpos.y)
        else:
            if not self.collision_sides["top"]:
                vecy = vecy
            else:
                self.position.y = oldpos.y
                self.rect.topleft = (self.rect.topleft[0], oldpos.y)
        self.rect.topleft+=self.collisionoffset
        #self.position = pygame.Vector2(self.position.x+vecx, self.position.y+vecy)
        #self.rect.topleft = (self.position.x, self.position.y)
        self.prev_pos = self.position
    def move_to(self,pos:pygame.Vector2):
        self.move(pos-self.position)

class Surface(Rect2D):
    def __init__(self, layer=1, position=pygame.Vector2(0.0, 0.0), color=(255, 255, 255), size=pygame.Vector2(100.0, 100.0),offset=pygame.Vector2(0,0)):
        super().__init__(layer,position,color,size,offset)
        self.surface=pygame.Surface(size)
        self.layers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[],
                       7:[], 8:[], 9:[], 10:[], "GUI":[]}
        self.window=None
        self.elapsed_ms=0
        self.current_camera = Camera2D(position=pygame.Vector2(0, 0))
        self.pressed_keys,self.prev_keys=pygame.key.ScancodeWrapper(),pygame.key.ScancodeWrapper()
    
    def render(self, window: Window):
        if self.visible:
            self.window = window
            self.detect_collisions()
            self.rect.topleft = (self.position.x+self.collisionoffset.x-window.current_camera.position.x, self.position.y+self.collisionoffset.y-window.current_camera.position.y)
            window.surface.blit(self.surface,self.position,self.rect)
    
    def frame(self):
        self.prev_keys=self.pressed_keys
        self.pressed_keys = pygame.key.get_pressed()
        if self.window !=None:
            global keys
            self.delta = self.window.clock.tick(self.window.fps)
            self.elapsed_ms += self.delta
            self.seconds = self.elapsed_ms/100
            pygame.draw.rect(self.surface, (0,0,0), self.rect)
            for event in pygame.event.get():      
                if event.type == pygame.QUIT: 
                    self.running = False
                    pygame.quit()
                    sys.exit()
            for j in range(1, 10+1):
                #print(j)
                for i in self.layers[j]:
                    i.render(self)
            for i in self.layers["GUI"]:
                i.render(self)
            self.window.frame()
            pygame.display.flip()
            pygame.display.update()
            
        
        return self.pressed_keys
    
    def key_just_pressed(self,scancode:int):
        return self.pressed_keys[scancode] and not self.prev_keys[scancode]
                

class Image2D(Rect2D):
    def __init__(self, filename: str, layer=1, position=pygame.Vector2(0.0, 0.0),offset=pygame.Vector2(0,0), size=pygame.Vector2(1, 1)):
        self.sprite = pygame.sprite.Sprite()
        self.debug = False
        self.layer = layer
        self.position = position
        self.name = filename
        self.image = pygame.image.load(self.name)
        self.image = self.image.convert_alpha()
        super().__init__(layer=self.layer, position=self.position)
        
        self.rect = self.image.get_rect()
        if size != pygame.Vector2(1, 1):
            self.size=size
        else:
            self.size = None
        self.collisionoffset=offset
        self.rect.x += self.collisionoffset.x
        self.rect.y += self.collisionoffset.y
    
    def render(self, window: Window):
        if self.visible:
            unoffset=pygame.Vector2(self.collisionoffset.x,self.collisionoffset.y)
            self.rect.topleft = (self.position.x+self.collisionoffset.x-window.current_camera.position.x, self.position.y+self.collisionoffset.y-window.current_camera.position.y)
            window.surface.blit(pygame.transform.scale(self.image, (self.size.x, self.size.y)) if self.size != None else self.image, self.rect.topleft-unoffset)
            self.detect_collisions()
            if self.debug:
                super().render(window)
    def changeimage(self,source,changecollision=True):
        self.image = pygame.image.load(source)
        self.name=source
        self.image = self.image.convert_alpha()
        
        if changecollision:
            self.rect = self.image.get_rect()
            self.rect.x += self.collisionoffset.x
            self.rect.y += self.collisionoffset.y

class Area2D(Rect2D):
    def __init__(self, layer: int = 1, position=pygame.Vector2(0.0, 0.0), size=pygame.Vector2(0.0, 0.0)):#, size=pygame.Vector2(0.0, 0.0)):
        self.sprite = pygame.sprite.Sprite()
        self.debug = False
        self.layer = layer
        self.position = position
        self.bodies_touching = []
        self.areas_touching = []
        self.area = True
        self.size = size
        super().__init__(layer=self.layer, position=self.position, size=size)
    
    def detect_collisions(self):
        self.bodies_touching = []
        self.areas_touching = []
        for i in self.window.layers[self.layer]:
            if i != self and type(i) == Rect2D and not i.area and i.collision:
                side = self.get_collision_side(i)
                if side != None:
                    if not i.area:
                        self.bodies_touching.append(i)
                    else:
                        self.areas_touching.append(i)
    
    def render(self, window: Window):
        if self.visible:
            self.rect.topleft = (self.position.x+self.collisionoffset.x-window.current_camera.position.x, self.position.y+self.collisionoffset.y-window.current_camera.position.y)

            # window.surface.blit(self.image, self.rect)
            self.detect_collisions()
            if self.debug:
                super().render(window)

class AudioManager:
    def __init__(self, **tracks):
        self.tracks = {}
        for i in tracks.keys():
            if type(tracks[i]) == AudioPlayer:
                self.tracks[i] = tracks[i]
    
    def play(self, track):
        try:
            self.tracks[track].play()
            return 0
        except KeyError:
            return -1

class AudioPlayer:
    def __init__(self, file: str) -> None:
        self.f = pygame.mixer.Sound(file)
        self.chan = pygame.mixer.find_channel()

    def play(self):
        self.chan.queue(self.f)
    def pause(self):
        self.chan.pause()
    def resume(self):
        self.chan.unpause()


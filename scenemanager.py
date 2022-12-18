import pyglet
from pyglet import shapes

# ----- Window Events -----
# on_mouse_motion(x, y, dx, dy)
# on_mouse_scroll(x, y, scroll_x, scroll_y)
# on_mouse_drag(x, y, dx, dy, buttons, modifiers)
# on_mouse_press(x, y, button, modifiers)
# on_mouse_release(x, y, button, modifiers)
# on_key_press(symbol, modifiers)
# on_draw()

# ----- Scene Template -----
# class Scene:

#     manager: "SceneManager"

#     def set_scene(self, scene_name):
#         self.manager.set_scene(scene_name)

#     def activate(self):
#         pass

#     def deactivate(self):
#         pass

#     def draw(self):
#         pass

#     def update_scene(self, dt):
#         pass

#     def on_key_press(self, symbol, modifiers):
#         pass

#     def on_key_release(self, symbol, modifiers):
#         pass


class SplashScene:
    manager: "SceneManager"

    def __init__(self, cur_circle, ui_batch):
        self.cur_circle = cur_circle
        self.ui_batch = ui_batch
        self.splashImg = pyglet.resource.image('res/splash.jpg')

    def set_scene(self, scene_name):
        self.manager.set_scene(scene_name)

    def activate(self):
        print('Splash scene activated')
        self.splashSprite = pyglet.sprite.Sprite(img=self.splashImg,
                                                 x=self.manager.window.width/2 - self.splashImg.width/2,
                                                 y=self.manager.window.height/2 - self.splashImg.height/2,
                                                 batch=self.ui_batch
                                                 )
        self.splashSprite.visible = True

    def deactivate(self):
        print('Splash scene deactivated')
        # Do I need to do any clean up here? E.g. clear sprites?

    # def update_scene(self, dt):
    #     pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.cur_circle.x = x
        self.cur_circle.y = y

    def on_mouse_press(self, x, y, button, modifiers):
        self.set_scene("MenuScene")

    def on_key_press(self, symbol, modifiers):
        pass

    def draw(self):
        self.ui_batch.draw()


class MenuScene:
    manager: "SceneManager"

    def set_scene(self, scene_name):
        self.manager.set_scene(scene_name)

    def activate(self):
        print('Menu scene activated')

        self.button_batch = pyglet.graphics.Batch()
        self.cursor_batch = pyglet.graphics.Batch()

        self.cur_circle = shapes.Circle(0, 0, 3, color=(
            200, 0, 0), batch=self.cursor_batch)

        self.circle = shapes.Circle(self.manager.window.width/2,
                                    self.manager.window.height/2 + 100,
                                    30,
                                    color=(0, 200, 0),
                                    batch=self.button_batch)

        self.t_but_img = pyglet.resource.image('res/T_ButtonImg.jpg')
        self.c_but_img = pyglet.resource.image('res/C_ButtonImg.jpg')
        self.q_but_img = pyglet.resource.image('res/Q_ButtonImg.jpg')

        self.t_but_sprite = pyglet.sprite.Sprite(img=self.t_but_img,
                                                 x=self.manager.window.width/2 - 100,
                                                 y=self.manager.window.height/2,
                                                 batch=self.button_batch
                                                 )
        self.t_but_sprite.visible = True

        self.c_but_sprite = pyglet.sprite.Sprite(img=self.c_but_img,
                                                 x=self.manager.window.width/2 - 25,
                                                 y=self.manager.window.height/2,
                                                 batch=self.button_batch
                                                 )
        self.c_but_sprite.visible = True

        self.q_but_sprite = pyglet.sprite.Sprite(img=self.q_but_img,
                                                 x=self.manager.window.width/2 + 50,
                                                 y=self.manager.window.height/2,
                                                 batch=self.button_batch
                                                 )
        self.q_but_sprite.visible = True

    def deactivate(self):
        print('Menu scene deactivated')

    # def update_scene(self, dt):
    #     pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.cur_circle.x = x
        self.cur_circle.y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if y > self.manager.window.height/2 - 25 and y < self.manager.window.height/2 + 25:

            if x > self.manager.window.width/2 - 100 and x < self.manager.window.width/2 - 50:
                # toggle
                if self.circle.visible == True:
                    self.circle.visible = False
                else:
                    self.circle.visible = True

            elif x > self.manager.window.width/2 - 25 and x < self.manager.window.width/2 + 25:
                # colour
                if self.circle.color == (0, 200, 0, 255):
                    self.circle.color = (0, 0, 200)
                else:
                    self.circle.color = (0, 200, 0)

            elif x > self.manager.window.width/2 + 50 and x < self.manager.window.width/2 + 100:
                # quit
                pyglet.app.exit()

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def draw(self):
        self.button_batch.draw()
        self.cursor_batch.draw()


class SceneManager:

    def __init__(self, window):
        self.window = window
        self.window.on_draw = self._on_draw

        self._scenes = {}
        self.current_scene = None

    def _on_draw(self):
        self.window.clear()
        self.current_scene.draw()

    def add_scene(self, scene_class, *args, alias=None):
        scene_class.manager = self
        name = alias or scene_class.__name__

        scene_instance = scene_class(*args)

        self._scenes[name] = scene_instance
        # self.current_scene = scene_instance
        self.window.clear()

    def set_scene(self, scene):
        assert scene in self._scenes, "Scene not found! Did you add it?"

        if self.current_scene:
            self.current_scene.deactivate()
            self.window.remove_handlers(self.current_scene)

        self.current_scene = self._scenes[scene]
        self.current_scene.activate()
        self.window.push_handlers(self.current_scene)

    def update(self, dt):
        self.current_scene.update_scene(dt)

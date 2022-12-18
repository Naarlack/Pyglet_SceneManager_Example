import pyglet
# from pyglet import clock
from pyglet import shapes
from scenemanager import SceneManager, SplashScene, MenuScene


window = pyglet.window.Window(
    1280, 1024, "SciFi Campaign Ops", resizable=True, vsync=False)

window.set_mouse_visible(False)

ui_batch = pyglet.graphics.Batch()
ui = pyglet.graphics.Group(5)

cur_circle = shapes.Circle(0, 0, 3, color=(
    200, 0, 0), batch=ui_batch, group=ui)

scene_manager = SceneManager(window=window)

scene_manager.add_scene(SplashScene, cur_circle, ui_batch)
scene_manager.add_scene(MenuScene)

scene_manager.set_scene("SplashScene")

# pyglet.clock.schedule_interval(scene_manager.update, 1/60)
pyglet.app.run(interval=1/60)

# if __name__ == "__main__":
#     pyglet.clock.schedule_interval(scene_manager.update, 1/60)
#     pyglet.app.run()

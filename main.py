from pyexpat import model
from tkinter import Scale
from turtle import position, window_height, window_width
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from main_menu import MainMenu

window.title = "Shooter My Game Radnoylar"

window.fullscreen = True

app = Ursina(borderless=False)

normalJump = 90


player = FirstPersonController(
    model="cube",
    color=color.orange,
    origin_y=-0.5,
    speed=90,
)
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))

player.cursor.color = color.green

player.jump_height = normalJump

player.disable()

m = MainMenu()
m.player = player


random.seed(0)
Entity.default_shader = lit_with_shadows_shader


ground = Entity(
    model="assets/ny_clean_up2/ny_clean_up2.obj",
    texture="assets/textures/tex.jpg",
    scale=100,
    position = (0 , 100, 0),
    collider="box",
)
font = Audio(
    "assets\jeliever.mp3",
)
editor_camera = EditorCamera(enabled=False, ignore_paused=True)


# BOX = Entity(
#     z = -70,
#     color = color.orange,
#     scale = 1,
#     model = "box",
# )

# stol = Entity(
#     z = -80,
#     scale = 1,
#     model = "assets/projeto_estrutural_de_um_sobrado.glb",
#     texture = "projeto_estrutural_de_um_sobrado.glb",
# )



gun = Entity(
    model="assets/ak-47s.glb",
    texture="ak-47s",
    parent=camera.ui,
    scale=0.40,
    position=(
        0.2,
        -0.6,
    ),
    rotation=(190),
    on_cooldown=False,
    
)
gun.muzzle_flash = Entity(
    parent=gun, z=2, world_scale=0.5, model="quad", color=color.yellow, enabled=False
)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent


# for i in range(160):
#     Entity(
#         model="cube",
#         origin_y=-.4,
#         scale=(2, 22, 10),
#         texture="brick",
#         texture_scale=(2, 2),
#         x=random.uniform(70, -70),
#         z=random.uniform(-70, 70),
#         collider="box",
#         scale_y=random.uniform(7, 7),
#         color=color.hsv(56,84, random.uniform(0.2, 1)),
#     )

def camera_zoom():
    camera.z += held_keys["o"] * 10 * time.dt

def update():
    if held_keys["left mouse"]:
        shoot()
    if held_keys["right mouse"]:
        gun.position = (0.0, -0.65)
        gun.rotation = 180
        
    if held_keys["r"]:
        gun.position = (
            0.2,
            -0.6,
        )
        gun.rotation = 190
    if held_keys["4"]:
        player.speed = 900.99
    camera_zoom()
    
    


def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled = True
        from ursina.prefabs.ursfx import ursfx

        ursfx(
            [(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)],
            volume=0.5,
            wave="noise",
            pitch=random.uniform(-13, -12),
            pitch_change=-12,
            speed=9.0,
        )
        invoke(gun.muzzle_flash.disable, delay=0.05)
        invoke(setattr, gun, "on_cooldown", False, delay=0.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, "hp"):
            mouse.hovered_entity.hp -= 15
            mouse.hovered_entity.blink(color.red)


from ursina.prefabs.health_bar import HealthBar




class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=shootables_parent,
            model="assets/OBJ.obj",
            scale = 3,
            origin_y=-0.5,
            color=color.black33,
            collider="box",
            **kwargs
        )
        self.health_bar = Entity(
            parent=self,
            y=1.2,
            model="cube",
            color=color.red,
            world_scale=(1.5, 0.1, 0.1),
        )
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 0:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(player.position, "y")
        hit_info = raycast(
            self.world_position + Vec3(0, 1, 0), self.forward, 30, ignore=(self,)
        )
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


enemies = [Enemy(x=x * 4) for x in range(14)]

hello = Enemy()

hello.add_script(SmoothFollow(target=player, offset=[0,1,0], speed=1))


def pause_input(key):
    if key == "tab":
        editor_camera.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled


pause_handler = Entity(ignore_paused=True, input=pause_input)


sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
Sky(texture = "assets/sky.jpg")


# wall1 = Entity(
#     model="cube",
#     texture="white_cube",
#     collider="box",
#     scale=(220, 12, 12),
#     opacity=(0),
#     position=(0, 5, 80),
#     color=color.hsv(225, 88, 0.9, random.uniform(0.2, 1)),
# )
# wall2 = duplicate(wall1, z=-110)
# wall3 = duplicate(wall1, rotation_y=90, x=-110, z=0)
# wall4 = duplicate(wall3, x=110)

# New World qusheppan koroche new york buladi :)

# world = Entity(
#     model = "assets/ny_clean_up2/ny_clean_up2.obj",
#     texture = "assets/textures/tex.jpg",
#     scale = 400,
#     collider = "box",
# )

app.run()

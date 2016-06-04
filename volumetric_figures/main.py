import glfw
import math
from OpenGL.GL import *
from figures import Cube
from figures import SurfaceOfRevolution


def key_callback(window, key, scancode, action, mods):
    global fill
    global rotate_x
    global rotate_y
    global rotate_z
    global scale
    global shift
    global segmentsCount
    global draw_cube
    global isometric

    drotate = 5
    dscale = 0.05
    dshift = 0.03
    dsegments = 1

    if key == glfw.KEY_F and action == glfw.PRESS:
        fill = not fill
    elif key == glfw.KEY_UP:
        rotate_x -= drotate
    elif key == glfw.KEY_DOWN:
        rotate_x += drotate
    elif key == glfw.KEY_RIGHT:
        rotate_y += drotate
    elif key == glfw.KEY_LEFT:
        rotate_y -= drotate
    elif key == glfw.KEY_Z:
        rotate_z += drotate
    elif key == glfw.KEY_X:
        rotate_z -= drotate
    elif key == glfw.KEY_I and scale < 1.9:
        scale += dscale
    elif key == glfw.KEY_R and scale > 0.1:
        scale -= dscale
    elif key == glfw.KEY_W:
        shift[1] += dshift
    elif key == glfw.KEY_S:
        shift[1] -= dshift
    elif key == glfw.KEY_D:
        shift[0] += dshift
    elif key == glfw.KEY_A:
        shift[0] -= dshift
    elif key == glfw.KEY_L and segmentsCount > 5:
        segmentsCount -= dsegments
    elif key == glfw.KEY_M and segmentsCount < 100:
        segmentsCount += dsegments
    elif key == glfw.KEY_C and action == glfw.PRESS:
        draw_cube = not draw_cube
    elif key == glfw.KEY_P and action == glfw.PRESS:
        isometric = not isometric


def resize_callback(window, width, height):
    if width < height:
        glViewport(0, 0, width, width)
    else:
        glViewport(0, 0, height, height)


def make_projection(is_isometric):
    a = 0.61
    l = 1
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if is_isometric:
        glMultTransposeMatrixf([1, 0, 0, 0,
                                0, 1, 0, 0,
                                0, 0, -1, 0,
                                0, 0, 0, 1])
        glMultTransposeMatrixf([1, 0, -l * math.cos(a), 0,
                                0, 1, -l * math.sin(a), 0,
                                0, 0, 1, 0,
                                0, 0, 0, 1])
    glMatrixMode(GL_MODELVIEW)


def paint_material(color):
    glColor3f(*color)


def main():
    global fill
    global rotate_x
    global rotate_y
    global rotate_z
    global scale
    global shift
    global segmentsCount
    global draw_cube
    global isometric
    fill = True
    rotate_x = 0
    rotate_y = 0
    rotate_z = 0
    scale = 1.0
    shift = [0.0, 0.0]
    segmentsCount = 40
    draw_cube = True
    isometric = False

    if not glfw.init():
        print("GLFW not initialized")
        return

    window = glfw.create_window(640, 640, "Cubes", None, None)
    if not window:
        print("Window not created")
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glfw.set_key_callback(window, key_callback)
    glfw.set_framebuffer_size_callback(window, resize_callback)

    big_cube = Cube([0.0, 0.0, 0.0], 0.6)
    small_cube = Cube([0.8, 0.8, 0.0], 0.1)

    line = (
        (0.0, 0.65, 0.0),
        (0.2, 0.4, 0.0),
        (0.05, 0.4, 0.0),
        (0.35, 0.0, 0.0),
        (0.08, 0.0, 0.0),
        (0.08, -0.15, 0.0),
        (0.0, -0.15, 0.0)
    )
    color = (0.0, 0.6, 0.1)
    surface = SurfaceOfRevolution(line, [0.0, 0.0, 0.0])

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        make_projection(isometric)

        if draw_cube:
            big_cube.draw(shift, fill, paint_material, scale, rotate_x, rotate_y, rotate_z)
            small_cube.draw([0.0, 0.0], fill, paint_material)
        else:
            paint_material(color)
            surface.change_segments_count(segmentsCount)
            surface.draw(shift, fill, scale, rotate_x, rotate_y, rotate_z)

        # после каждой итерации сдвиг снова становится нулевым до тех пор,
        # пока пользователь не нажмёт кнопку
        shift = [0.0, 0.0]

        glfw.swap_buffers(window)
        glfw.poll_events()

    print("Terminate...")
    glfw.terminate()


if __name__ == "__main__":
    main()

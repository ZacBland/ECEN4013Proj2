import numpy as np
from vispy import app, gloo
from vispy.util.transforms import perspective, translate, rotate
from threading import Thread

vert = """
// Uniforms
// ------------------------------------
uniform   mat4 u_model;
uniform   mat4 u_view;
uniform   mat4 u_projection;
uniform   vec4 u_color;

// Attributes
// ------------------------------------
attribute vec3 a_position;
attribute vec4 a_color;
attribute vec3 a_normal;

// Varying
// ------------------------------------
varying vec4 v_color;

void main()
{
    v_color = a_color * u_color;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
}
"""


frag = """
// Varying
// ------------------------------------
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
"""


# -----------------------------------------------------------------------------
def cube():
    """
    Build vertices for a colored cube.

    V  is the vertices
    I1 is the indices for a filled cube (use with GL_TRIANGLES)
    I2 is the indices for an outline cube (use with GL_LINES)
    """
    vtype = [('a_position', np.float32, 3),
             ('a_normal', np.float32, 3),
             ('a_color', np.float32, 4)]
    # Vertices positions
    v = [[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
         [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]]
    # Face Normals
    n = [[0, 0, 1], [1, 0, 0], [0, 1, 0],
         [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    # Vertice colors
    c = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
         [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]]

    V = np.array([(v[0], n[0], c[0]), (v[1], n[0], c[1]),
                  (v[2], n[0], c[2]), (v[3], n[0], c[3]),
                  (v[0], n[1], c[0]), (v[3], n[1], c[3]),
                  (v[4], n[1], c[4]), (v[5], n[1], c[5]),
                  (v[0], n[2], c[0]), (v[5], n[2], c[5]),
                  (v[6], n[2], c[6]), (v[1], n[2], c[1]),
                  (v[1], n[3], c[1]), (v[6], n[3], c[6]),
                  (v[7], n[3], c[7]), (v[2], n[3], c[2]),
                  (v[7], n[4], c[7]), (v[4], n[4], c[4]),
                  (v[3], n[4], c[3]), (v[2], n[4], c[2]),
                  (v[4], n[5], c[4]), (v[7], n[5], c[7]),
                  (v[6], n[5], c[6]), (v[5], n[5], c[5])],
                 dtype=vtype)
    I1 = np.resize(np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32), 6 * (2 * 3))
    I1 += np.repeat(4 * np.arange(2 * 3, dtype=np.uint32), 6)

    I2 = np.resize(
        np.array([0, 1, 1, 2, 2, 3, 3, 0], dtype=np.uint32), 6 * (2 * 4))
    I2 += np.repeat(4 * np.arange(6, dtype=np.uint32), 8)

    return V, I1, I2


# -----------------------------------------------------------------------------
class Canvas(app.Canvas):

    def __init__(self, parent):
        self.parent = parent
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))

        self.vertices, self.filled, self.outline = cube()
        self.filled_buf = gloo.IndexBuffer(self.filled)
        self.outline_buf = gloo.IndexBuffer(self.outline)

        self.program = gloo.Program(vert, frag)
        self.program.bind(gloo.VertexBuffer(self.vertices))

        self.view = translate((0, 0, -5))
        self.model = np.eye(4, dtype=np.float32)

        gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
        self.projection = perspective(45.0, self.size[0] /
                                      float(self.size[1]), 2.0, 10.0)

        self.program['u_projection'] = self.projection

        self.program['u_model'] = self.model
        self.program['u_view'] = self.view

        self.theta = 0
        self.phi = 0
        self.e = 0

        gloo.set_clear_color('white')
        gloo.set_state('opaque')
        gloo.set_polygon_offset(1, 1)

        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.show()

    # ---------------------------------
    def on_timer(self, event):
        self.theta = self.parent.theta
        self.phi = self.parent.phi
        self.e = self.parent.e
        self.model = np.dot(rotate(self.theta, (0, 1, 0)),
                            rotate(self.phi, (0, 0, 1)))
        self.model = np.dot(rotate(self.e, (1, 0, 0)),
                            self.model)
        self.program['u_model'] = self.model
        self.update()

    # ---------------------------------
    def on_resize(self, event):
        gloo.set_viewport(0, 0, event.physical_size[0], event.physical_size[1])
        self.projection = perspective(45.0, event.size[0] /
                                      float(event.size[1]), 2.0, 10.0)
        self.program['u_projection'] = self.projection

    # ---------------------------------
    def on_draw(self, event):
        gloo.clear()

        # Filled cube

        gloo.set_state(blend=False, depth_test=True, polygon_offset_fill=True)
        self.program['u_color'] = 1, 1, 1, 1
        self.program.draw('triangles', self.filled_buf)

        # Outline
        gloo.set_state(blend=True, depth_test=True, polygon_offset_fill=False)
        gloo.set_depth_mask(False)
        self.program['u_color'] = 0, 0, 0, 1
        self.program.draw('lines', self.outline_buf)
        gloo.set_depth_mask(True)


import sys, serial, time, glob

class read_thread():
    def __init__(self, parent):
        self.parent = parent
        print("Connecting...")
        print(get_port()[0])
        self.ser = None
        while self.ser is None:
            try:
                self.ser = serial.Serial(get_port()[0], timeout=5)
            except Exception as e:
                print("Failed Connection, trying again...")
                time.sleep(1)
        print("Connected to Pi.")

    def loop(self):
        time.sleep(1)
        while True:
            try:
                received_data = self.ser.read()
                time.sleep(0.03)
                data_left = self.ser.inWaiting() 
                received_data += self.ser.read(data_left)
                received_data = received_data.decode("utf-8")

                info = received_data.split(',')
                if info[0] == "ori":
                    if(info[1] != 'None'):
                        setattr(self.parent, "theta", -float(info[1]))
                        setattr(self.parent, "phi", float(info[3]))
                        setattr(self.parent, "e", float(info[2]))

            except Exception as e:
                print("Error:",e)

        
def get_port():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class Main:
    def __init__(self) -> None:
        self.theta = 0.0
        self.phi = 0.0
        self.e = 0.0
        th = read_thread(self)
        thread = Thread(target=th.loop, args=())
        thread.daemon = True
        thread.start()
        canvas = Canvas(self)
        app.run()
        while True:
            time.sleep(1)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    m = Main()
    

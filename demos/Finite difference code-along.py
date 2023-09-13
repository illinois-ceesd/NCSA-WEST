import numpy as np
import pytato as pt
import matplotlib.pyplot as plt
import arraycontext
import pyopencl as cl
import pytato as pt
from pytools.obj_array import make_obj_array

# ----------

cl_ctx = cl.create_some_context(interactive=True)
queue = cl.CommandQueue(cl_ctx)

# ----------

class MyArrayContext(arraycontext.PytatoPyOpenCLArrayContext):
    def transform_dag(self, dag):
        pt.show_dot_graph(dag)
        return dag

    def transform_loopy_program(self, t_unit):
        if t_unit.default_entrypoint.name == "tstep":
            import loopy as lp
            print(lp.generate_code_v2(t_unit).device_code())
        return t_unit

actx = MyArrayContext(queue)

# ----------

class Mesh:
    def __init__(self, size_x, size_y, resolution):
        self.size_x = size_x
        self.size_y = size_y
        self.resolution = resolution
        self.nx, self.ny = int(size_x*resolution), int(size_y*resolution)

        self.x = actx.np.linspace(
                0, size_x, self.nx, endpoint=False).reshape(self.nx, 1)
        self.y = actx.np.linspace(
                0, size_y, self.ny, endpoint=False).reshape(1, self.ny)
        self.hx = actx.to_numpy(self.x[1, 0] - self.x[0, 0])
        self.hy = actx.to_numpy(self.y[0, 1] - self.y[0, 0])

    def plot(self, f, **kwargs):
        if not isinstance(f, np.ndarray):
            f = actx.to_numpy(f)
        return plt.imshow(f.T[::-1], extent=(0, self.size_x, 0, self.size_y),
                          **kwargs)

    def set_plot_data(self, img, f):
        if not isinstance(f, np.ndarray):
            f = actx.to_numpy(f)
        img.set_data(f.T[::-1])

    def zeros(self):
        return actx.zeros((self.nx, self.ny), dtype=np.float64)

    def norm(self, u):
        return actx.np.sqrt(actx.np.sum(abs(u)**2)) * (
                self.size_x * self.size_y / (self.nx - 1) / (self.ny -1))


mesh = Mesh(size_x=6, size_y=4, resolution=64)

# ----------

f = (mesh.x - mesh.size_x/2)**2 + (mesh.y - mesh.size_y/2)**2
#mesh.plot(f)
#plt.show()

# ----------

def d_dx(mesh, u):
    padded = actx.np.concatenate((
        u[0:1, :],
        u,
        u[-2:-1, :],
        ), axis=0)
    return (padded[2:] - padded[:-2])/(2*mesh.hx)

df_dx = 2*(mesh.x - mesh.size_x/2)
df_dx_num = d_dx(mesh, f)
assert df_dx_num.shape == f.shape

err = df_dx - df_dx_num
print(actx.to_numpy(mesh.norm(err)))
#plt.show()

# ----------

def rk4_step(y, t, h, f):
    k1 = f(t, y)
    k2 = f(t+h/2, y + h/2*k1)
    k3 = f(t+h/2, y + h/2*k2)
    k4 = f(t+h, y + h*k3)
    return y + h/6*(k1 + 2*k2 + 2*k3 + k4)


# ----------

bump = actx.np.exp(-80*((mesh.x - mesh.size_x/2)**2 + (mesh.y - mesh.size_y/2)**2))
#mesh.plot(bump)
#plt.show()


# ----------

def laplace(mesh, u, boundary_val):
    padded_x = actx.np.concatenate((
        actx.np.full((1, mesh.ny), boundary_val),
        u,
        actx.np.full((1, mesh.ny), boundary_val),
        ), axis=0)
    padded_y = actx.np.concatenate((
        actx.np.full((mesh.nx, 1), boundary_val),
        u,
        actx.np.full((mesh.nx, 1), boundary_val),
        ), axis=1)
    return (
            (padded_x[2:] - 2*u + padded_x[:-2])/mesh.hx**2
            +
            (padded_y[:, 2:] - 2*u + padded_y[:, :-2])/mesh.hy**2
            )


# TODO: Remember to show that rhs is only called *once*
def rhs(t, s):
    u, du_dt = s

    return make_obj_array([
        du_dt + actx.np.sin(30*t) * bump,
        laplace(mesh, u, 0)
        ])

# FIXME: Why does 'step' get renamed to _cl_step?
def tstep(t, s):
    return rk4_step(s, t, dt, rhs)

# TODO: demo repeated freezing
tstep_compiled = actx.compile(tstep)


dt = min(mesh.hx, mesh.hy)

# --------------------------

state = make_obj_array([
    mesh.zeros(),
    mesh.zeros()
    ])


if 0:
    t = 0.
    for i in range(1000):
        if i % 10 == 0:
            print(i)

        state = tstep_compiled(actx.from_numpy(t), state)
        t += dt

#mesh.plot(state[0])

# --------------------------

t = 0.
state = make_obj_array([
    mesh.zeros(),
    mesh.zeros()
    ])

fig = plt.figure()
img = mesh.plot(state[0], vmin=-0.02, vmax=0.02)

def update(frame):
    global t, state
    for i in range(10):
        state = tstep_compiled(actx.from_numpy(t), state)
        t += dt
    mesh.set_plot_data(img, state[0])

import matplotlib.animation as animation
ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)
plt.show()

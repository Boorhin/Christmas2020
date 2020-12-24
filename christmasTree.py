import pyvista as pv
#from pyvistaqt import BackgroundPlotter
import numpy as np
from tqdm import tqdm

def mkpoints():
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(3, 18, 100)
    r = np.linspace(10, 1, 100)
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    return np.column_stack((x, y, z))

def lines_from_points(points):
    """Given an array of points, make a line set"""
    poly = pv.PolyData()
    poly.points = points
    cells = np.full((len(points)-1, 3), 2, dtype=np.int_)
    cells[:, 1] = np.arange(0, len(points)-1, dtype=np.int_)
    cells[:, 2] = np.arange(1, len(points), dtype=np.int_)
    poly.lines = cells
    return poly

def mkflakes(rg):
    pts= rg.random((500,3))
    pts[:,0] = (pts[:,0]*2*Rad -Rad)*2
    pts[:,1] = (pts[:,1]*2*Rad -Rad)*2
    pts[:,2] *= 30
    return pts

c = [5.5, 9, 13,15]
d = (0,0,1)
h = [7,5,6, 6]
r = [10,7,4, 4]
Res = 50
Rad= 65
rg = np.random.default_rng()

points= mkpoints()
line = lines_from_points(points)
tube = line.tube(radius=0.1)
tube["lights"] = rg.random(tube.n_cells)

S = pv.Sphere(radius=0.1,theta_resolution =8, phi_resolution =8)

flakes = pv.PolyData(mkflakes(rg)).glyph(geom=S)


plotter = pv.Plotter(off_screen=True, notebook=False)
plotter.enable_eye_dome_lighting()


#plotter = BackgroundPlotter(show = True)
for i in range(4):
    plotter.add_mesh(pv.Cone(center=[0,0,c[i]], direction=d, height=h[i], radius=r[i], capping=True, resolution=Res), color ="g")
plotter.add_mesh(pv.Cylinder(center=[0,0,1],direction=(0,0,1),radius=2,height=3, resolution=30, capping=True), color="brown")
plotter.add_mesh(tube, scalars="lights",opacity=[0, 0.25, 0.5, 0.75, 1], cmap="plasma", show_scalar_bar=False)
plotter.add_mesh(flakes)
plotter.add_mesh(pv.Sphere(center=[15,0,1.5],radius =4,theta_resolution =16, phi_resolution =16), color="w", smooth_shading=True)
plotter.add_mesh(pv.Sphere(center=[15,0,6],radius =3,theta_resolution =16, phi_resolution =16), color="w",smooth_shading=True)
plotter.add_mesh(pv.Sphere(center=[15,0,9],radius =2,theta_resolution =16, phi_resolution =16), color="w",smooth_shading=True)
plotter.add_mesh(pv.Cone(center=[15,2,9.5], direction=(0,1,0), height=4, radius=0.2, capping=False, resolution=20), color ="orange")
plotter.add_mesh(pv.Sphere(center=[14.5,1.6,10],radius =0.2,theta_resolution =16, phi_resolution =16), color="k",smooth_shading=True)
plotter.add_mesh(pv.Sphere(center=[15.5,1.6,10],radius =0.2,theta_resolution =16, phi_resolution =16), color="k",smooth_shading=True)
plotter.add_mesh(pv.Cylinder(center=[12,0,8],direction=(1,0,-1),radius=0.3,height=3, resolution=20, capping=True), color="brown")
plotter.add_mesh(pv.Cylinder(center=[18,0,8],direction=(-1,0,-1),radius=0.3,height=3, resolution=20, capping=True), color="brown")

plotter.add_text("Joyeux Noël et Meilleurs Voeux pour 2021!", font="arial",shadow=True,color="r")
#plotter.add_floor("-z", color="w")
plotter.open_movie('MerryChristmas.mp4', framerate=24)
for t in tqdm(range(200)):
    plotter.update_scalars(rg.random(tube.n_cells), mesh=tube, render=False)
    #plotter.update_coordinates(mkflakes(rg), mesh=flakes, render=False)
    plotter.render()
    omega= np.pi*t/80
    Cpos=[(Rad*np.sin(omega), Rad*np.cos(omega), 13),
 (0.0, 0.2, 10),
 (0.0, 0.0, 1.0)]
    plotter.camera_position=Cpos
    plotter.write_frame()
plotter.close()

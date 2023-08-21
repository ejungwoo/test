import math
import random

num_events = 100000
vertex_x = 0
vertex_y = 0
vertex_z = 0

def caculate_momentum(ke, theta):
    mass = 938.272
    momentum = math.sqrt( (ke + mass)**2 - mass**2 )

    theta = math.radians(theta)
    phi_range = math.radians(6.0)
    phi = random.uniform(-phi_range, phi_range)

    px = momentum * math.sin(theta) * math.cos(phi)
    py = momentum * math.sin(theta) * math.sin(phi)
    pz = momentum * math.cos(theta)

    return px, py, pz

file_input = open("P1_P2_sim.out")
file_g4gen = open("two_proton.gen",'w');
print('p',        file=file_g4gen)
print(num_events, file=file_g4gen)

event_id = 0
for line in file_input:
    if event_id >= num_events:
        break
    energy_theta_array = line.split()
    px1, py1, pz1 = caculate_momentum( float(energy_theta_array[0]), float(energy_theta_array[1]) )
    px2, py2, pz2 = caculate_momentum( float(energy_theta_array[2]), float(energy_theta_array[3]) )

    num_particles = 2

    print(f"{event_id:<6} {num_particles:2} {vertex_x:8}  {vertex_y:8}  {vertex_z:8}", file=file_g4gen)
    print(f"{2212:<9} {px1:8,.2f}  {py1:8,.2f}  {pz1:8,.2f}",           file=file_g4gen)
    print(f"{2212:<9} {px2:8,.2f}  {py2:8,.2f}  {pz2:8,.2f}",           file=file_g4gen)
    event_id = event_id + 1

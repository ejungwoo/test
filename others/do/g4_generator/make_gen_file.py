import math

num_events = 1000
vertex_x = 0
vertex_y = 0
vertex_z = 0

def caculate_momentum(ke, phi):
    mass = 938.272
    momentum = math.sqrt( (ke + mass)**2 - mass**2 )
    phi_rad = phi * math.pi / 360
    px = momentum * math.sin(phi_rad)
    py = 0
    pz = momentum * math.cos(phi_rad)
    return px, py, pz

file_input = open("P1_P2_sim.out")
file_g4gen = open("two_proton.gen",'w');
print('p',        file=file_g4gen)
print(num_events, file=file_g4gen)

event_id = 0
for line in file_input:
    if event_id >= num_events:
        break
    energy_phi_array = line.split()
    px1, py1, pz1 = caculate_momentum( float(energy_phi_array[0]), float(energy_phi_array[1]) )
    px2, py2, pz2 = caculate_momentum( float(energy_phi_array[2]), float(energy_phi_array[3]) )

    print(f"{event_id:<6} 2 {vertex_x:8}  {vertex_y:8}  {vertex_z:8}", file=file_g4gen)
    print(f"{0:<6}   {px1:8,.2f}  {py1:8,.2f}  {pz1:8,.2f}",           file=file_g4gen)
    print(f"{1:<6}   {px2:8,.2f}  {py2:8,.2f}  {pz2:8,.2f}",           file=file_g4gen)
    event_id = event_id + 1

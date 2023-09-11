import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import time
import csv
import datetime
import serial.tools
import serial.tools.list_ports

#find the port radio module is connected to
ports = serial.tools.list_ports.comports()
# serialInst = serial.Serial()

for port in ports:
    print(str(port))


nrows = 3
ncols = 4
fig, ax = plt.subplots(nrows, ncols)
mng = plt.get_current_fig_manager()
mng.resize(1300, 600)
fig.set_facecolor('#000')
fig.subplots_adjust(
top=0.921,
bottom=0.073,
left=0.043,
right=0.953,
hspace=0.437,
wspace=0.524
)



(id_plot, phase_plot ,runT_plot, npacket_plot), (gps_plot, alt_plot, spd_plot, sepT_plot), (batV_plot, temp_plot, pres_plot, vidT_plot) = ax
plot_titles = [['Team ID', '    Phase', 'Running time', 'Number of packets received'], ['GPS', 'Altitude', 'Speed', 'Seperation time'], ['Battery voltage', 'Temperature', 'Presuure', 'Video recording time']]

running_time = 0
running_time_list= []
packet_count = 0
altitude = []
speed = []
temperature = []
pressure = []
voltage = 0
spd_ylim = 5
start_time = time.time()
for _ in ax:
    for plot in _:
        plot.axis('off')


    

    
gps_values = (42.0994, 43.9984)
graphP = (alt_plot, spd_plot, temp_plot, pres_plot)

for plot in graphP:
    plot.axis('on')
    plot.set_facecolor('#000')
    plot.tick_params(color='#c2d2f5', labelcolor='#c2d2f5')
    for spine in plot.spines.values():
        spine.set_edgecolor('#c2d2f5')



[ax[i][j].set_title(plot_titles[i][j], color='#c2d2f5') for i in range(nrows) for j in range(ncols)]


# id_plot.tick_params(color='#000', labelcolor='#000')
# for spine in id_plot.spines.values():
#         spine.set_edgecolor('#fff')
 
serialInst = serial.Serial("COM7", 9600)
f = open('telemetry.csv', 'w', encoding="UTF8")
writer = csv.writer(f)
#id,phase, runtime, npacket,V, Alt, Spd, temp, pres, lat, long, septime, videotime
writer.writerow(['Team ID', 'Phase', 'Running time', 'Number of packets received', 'Battery voltage', 'Altitude', 'Speed', 'Temperature', 'Pressure', 'Latitude', 'Longtitude', 'Seperation time', 'Video recording time'])

def request_start(val):
    data = "s"
    serialInst.write(data.encode())
    print("requested start")
resetPlot = False 
def request_reset(val):
    global resetPlot
    data = "r"
    serialInst.write(data.encode())
    print("requested reset")
    resetPlot = True
    
str_btn_axes = plt.axes([0.88, 0.05, 0.08, 0.075])
start_button = Button(str_btn_axes, "Start", color="#fff")
start_button.on_clicked(request_start)

rst_btn_axes = plt.axes([0.78, 0.05, 0.08, 0.075])
reset_button = Button(rst_btn_axes, "Reset", color="#fff")
reset_button.on_clicked(request_reset)

sepTime = datetime.datetime.now()

x = 0
def updater(i):
    global running_time, packet_count, x, spd_ylim, resetPlot, altitude, speed, temperature, pressure, running_time_list
    if resetPlot:
        # alt_plot, spd_plot, temp_plot, pres_plot = []*4
        # graph_values = [altitude, speed, temperature, pressure]
        altitude = []
        speed = []
        temperature = []
        pressure = []
        running_time_list = []
        resetPlot = False
    try:
        if serialInst.in_waiting > 0:
            x+=1
            packet = serialInst.readline().decode().strip()
            packet = packet.split("|")[:-1]
            writer.writerow(packet)
            print(packet) #id,phase, runtime, npacket,V, Alt, Spd, temp, pres, lat, long, septime, videotime
            running_time_list.append(int(float(packet[2])))
            packet_count = int(float(packet[3]))
            altitude.append(float(packet[5]))
            speed.append(abs(float(packet[6])))
            team_id = int(float(packet[0]))
            temperature.append(float(packet[7]))
            pressure.append(float(packet[8])/1000)
            phase = int(float(packet[1]))
            sepTime = packet[11]
            voltage = float(packet[4])
            gps_values = (float(packet[9]), float(packet[10]))
            video_time = int(float(packet[-1]))
            
            id_plot.cla()
            alt_plot.cla()
            gps_plot.cla()
            runT_plot.cla()
            npacket_plot.cla()
            vidT_plot.cla()
            sepT_plot.cla()
            batV_plot.cla()
            spd_plot.cla()
            phase_plot.cla()
            temp_plot.cla()
            pres_plot.cla()
            
            [ax[i][j].set_title(plot_titles[i][j], color='#c2d2f5') for i in range(nrows) for j in range(ncols)]
            
            time_step = running_time_list[-1]
            id_plot.text(0.33, 0.5, team_id, fontsize=20, color='#c2d2f5')
            id_plot.set_facecolor("#000")
            
            phase_plot.text(0.5, 0.5, phase, fontsize=20, color="#c2d2f5")
            phase_plot.set_facecolor("#000")
            
            gps_plot.text(0.06, 0.5, f"Lattiude   | Longtitude\n{round(gps_values[0],4)} | {round(gps_values[1],4)}", fontsize=15, color="#c2d2f5")
            gps_plot.set_facecolor('#000')
            
            runT_plot.text(0.4, 0.5, str(time_step), fontsize=20, color="#c2d2f5")
            runT_plot.set_facecolor("#000")
            
            npacket_plot.text(0.4, 0.5, packet_count, fontsize=20, color="#c2d2f5")
            npacket_plot.set_facecolor("#000")
            
            sepT_plot.text(0.1, 0.5, sepTime, fontsize=15, color="#c2d2f5")
            sepT_plot.set_facecolor("#000")
            
            vidT_plot.text(0.4, 0.5, video_time, fontsize=20, color="#c2d2f5")
            vidT_plot.set_facecolor("#000")
            
            batV_plot.text(0.35, 0.5, voltage, fontsize=20, color="#c2d2f5")
            batV_plot.set_facecolor("#000")
            
            alt_plot.grid()
            alt_plot.plot(running_time_list, altitude, color="#FFA500")
            alt_plot.scatter(time_step, altitude[-1], color="#FFA500")
            alt_plot.text(time_step-0.2, altitude[-1]+20, altitude[-1], color='#c2d2f5')
            alt_plot.set_xlim(time_step-5, time_step+5)            
            alt_plot.set_ylim(-50,200)
            alt_plot.text(time_step+5.5,-50, 'S', color='#c2d2f5')
            
            spd_plot.plot(running_time_list, speed, color="#FFA500")
            spd_plot.scatter(time_step, speed[-1], color="#FFA500")
            spd_plot.text(time_step-0.2, speed[-1]+1, speed[-1], color='#c2d2f5')
            spd_plot.set_xlim(time_step-5, time_step+5)
            if speed[-1] >= spd_ylim:
                spd_ylim = speed[-1]*1.4
            spd_plot.set_ylim(-2, spd_ylim)
            spd_plot.text(time_step-5, spd_ylim+spd_ylim*0.05, 'm/s', color='#c2d2f5')
            spd_plot.text(time_step+5.5,-2, 'S', color='#c2d2f5')
            
            temp_plot.plot(running_time_list, temperature, color="#FFA500")
            temp_plot.scatter(time_step, temperature[-1], color="#FFA500")
            temp_plot.text(time_step-0.2, temperature[-1]+4, temperature[-1], color='#c2d2f5')
            temp_plot.set_xlim(time_step-5, time_step+5)
            temp_plot.set_ylim(0,40) 
            temp_plot.text(time_step+5.5, 0, 'S', color='#c2d2f5')
            temp_plot.text(time_step-5, 40+40*0.05, 'C', color='#c2d2f5')
            
            pres_plot.plot(running_time_list, pressure, color="#FFA500")
            pres_plot.scatter(time_step, pressure[-1], color="#FFA500")
            pres_plot.text(time_step-0.2, pressure[-1]+20, pressure[-1], color='#c2d2f5')
            pres_plot.set_xlim(time_step-5, time_step+5)
            pres_plot.set_ylim(0,200)
            pres_plot.text(time_step+5.5, 0, 'S', color='#c2d2f5')
        # else:
        #     print('not available')
    except Exception as e:
        print(e)
        

ani = FuncAnimation(fig, updater, interval=0)

plt.show()

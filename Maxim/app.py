from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
from threading import Thread
import io
import csv
from helper import *

update_timing = []
started = False
start_tracking_timing = ""
end_tracking_timing = ""

def wait_for_logging():
    global started
    global start_tracking_timing
    global end_tracking_timing
    
    target_window = "Maxim DeviceStudio - [PPG EV Kit]"
    state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128
    socketio.emit('status_update', {'started': started})

    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0 and get_active_window(target_window) and not started:
                print(f"Window '{target_window}' gained focus at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                start_tracking_timing = listen_loading()
                print(f"Started Logging at {start_tracking_timing}")
                socketio.emit('status_update', {'started': True})
                started = True

            # Assume that if already focused and already started, means you are stopping (AND NOT CLICKING ANYTHING ELSE)
            elif a < 0 and get_active_window(target_window) and started:
                end_tracking_timing = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format with milliseconds
                print(f"Stopped Logging at {end_tracking_timing}")
                started = False
                socketio.emit('status_update', {'started': False})
                break

        socketio.emit('status_update', {'started': started})
        time.sleep(0.001)
    
app = Flask(__name__)
socketio = SocketIO(app)

with app.app_context():
    thread = Thread(target=wait_for_logging)
    thread.daemon = True
    thread.start()


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/waiting")
def waiting():
    return render_template('waiting.html')

@app.route("/track")
def track():
    return render_template('track.html')

@app.route('/download', methods=['POST'])
def download():
    global start_tracking_timing
    global end_tracking_timing

    request_data = request.json
    data = request_data.get('dataContainer', [])
    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Click Time', 'Unclick Time'])
    writer.writerow([start_tracking_timing, end_tracking_timing])
    for row in data:
        print(row)
        writer.writerow([row.get('clickTime'), row.get('unclickTime')])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                     as_attachment=True,
                     mimetype='text/csv',
                     download_name = "data.csv")


if __name__ == "__main__":
    socketio.run(app)
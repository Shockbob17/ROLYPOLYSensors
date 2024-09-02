import pygetwindow as gw
import ctypes
import time
import datetime
import win32api


def get_active_window(target_window):
    active_window = gw.getActiveWindow()
    return (active_window and target_window == active_window.title)


def listen_loading():
    # Define necessary structures and constants
    class CURSORINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint),
                    ("flags", ctypes.c_uint),
                    ("hCursor", ctypes.c_void_p),
                    ("ptScreenPos", ctypes.wintypes.POINT)]

    # Cursor types for default and loading (hourglass/spinning wheel)
    IDC_ARROW = 32512
    IDC_WAIT = 32514

    # Load default and loading cursors
    user32 = ctypes.WinDLL('user32')
    LoadCursor = user32.LoadCursorW
    GetCursorInfo = user32.GetCursorInfo

    # Function to load specific cursors
    def load_cursor(cursor_id):
        return LoadCursor(None, cursor_id)

    # Default and loading cursor handles
    default_cursor = load_cursor(IDC_ARROW)
    loading_cursor = load_cursor(IDC_WAIT)

    def check_cursor():
        cursor_info = CURSORINFO()
        cursor_info.cbSize = ctypes.sizeof(CURSORINFO)
        
        if GetCursorInfo(ctypes.byref(cursor_info)):
            return cursor_info.hCursor
        

    previous_cursor = None

    while True:
        current_cursor = check_cursor()

        if current_cursor == default_cursor and previous_cursor == "Loading":
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format with milliseconds
            return timestamp
        
        elif current_cursor == loading_cursor:
            previous_cursor = "Loading"

        time.sleep(0.1)  # Adjust the interval to 0.1 seconds



def intialise_on_click(target_window): 
    global started
    state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128

    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0 and get_active_window(target_window) and not started:
                print(f"Window '{target_window}' gained focus at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                monitoring_time = listen_loading()
                print(f"Started Logging at {monitoring_time}")
                started = True
            
            # Assume that if already focused and already started, means you are stopping (AND NOT CLICKING ANYTHING ELSE)
            elif a < 0 and get_active_window(target_window) and started:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format with milliseconds
                print(f"Stopped Logging at {timestamp}")
                started = False
                break
                
        time.sleep(0.001)

    
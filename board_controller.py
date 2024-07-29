import serial
import numpy as np
import time
import threading

class DisplayBoard:
    def __init__(self, port, baudrate):
        self.axes = np.array(["X", "Y", "Z", "A", "B", "C", "U", "V"])
        self.serial = serial.Serial(port=port, baudrate=baudrate)

    def write_serial(self, command):
        self.serial.write(str(command+"\n").encode())
        # Wait for confirmation
        self.serial.read_until(expected="ok\n".encode(), size=3)

    def home_motors(self):
        """
        Sets home position of all motors to all the way retracted
        """
        # Run motors all the way up and back down in relative positioning mode
        self.move([20]*8, absolute=False)
        self.move([-15]*8, absolute=False)

        self.move([630]*8, absolute=False)
        self.move([-630]*8, absolute=False)

        # Back off
        self.move([30]*8, absolute=False)

        # Reapproach
        self.move([-25]*8, absolute=False)

        # Set home offset here
        self.write_serial("G90")
        self.write_serial("M428")
    
    def move(self, positions, absolute=True):
        move_type_str = "absolute"
        if absolute:
            self.write_serial("G90")
        else:
            self.write_serial("G91")
            move_type_str = "relative"

        move = "G0"

        for i, axis in enumerate(self.axes):
            if positions[i] is not None:
                move += f" {axis}{positions[i]}"
        
        print(f"Executing {move_type_str} move: {move}")
        self.write_serial(move)

class KineticDisplay:
    def __init__(self, ports, baudrate):
        self.boards = [DisplayBoard(port, baudrate) for port in ports]
        self.current_state = []

    def home_display(self):
        homing_threads = []
        for board in self.boards:
            home_thread = threading.Thread(target=board.home_motors)
            homing_threads.append(home_thread)
            home_thread.start()

        for thread in homing_threads:
            thread.join()

    def move_all(self, positions, absolute=True):
        for i, row in enumerate(positions):
            self.boards[i % len(self.boards)].move(row, absolute=absolute)

    def show_pattern(self, file_name):
        with open(file_name, "r") as pattern_file:
            rows = pattern_file.readlines()
            for i in range(len(rows)):
                state_row = rows[i].split(',')
                move_positions = [int(pos) for pos in state_row]
                self.boards[i % len(self.boards)].move(move_positions, absolute=True)

if __name__ == "__main__":
    PORT = "/dev/ttyACM0"
    BAUD_RATE = 250000

    board = DisplayBoard(PORT, BAUD_RATE)

    # Pause to establish connection or motors do weird things
    time.sleep(3)

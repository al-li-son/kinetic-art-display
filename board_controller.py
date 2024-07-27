import serial
import numpy as np
import time

class DisplayBoard:
    def __init__(self, port, baudrate):
        self.axes = np.array(["X", "Y", "Z", "A", "B", "C", "U", "V"])
        self.serial = serial.Serial(port=port, baudrate=baudrate)

    def write_serial(self, command):
        self.serial.write(str(command+"\n").encode())

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
        for board in self.boards:
            board.home_motors()
        time.sleep(60)

    def show_pattern(self, file_name):
        with open(file_name, "r") as pattern_file:
            rows = pattern_file.readlines()
            for i in range(len(rows)):
                state_row = rows[i].split(',')
                move_positions = [int(pos) for pos in state_row]
                self.boards[i % len(self.boards)].move(move_positions, absolute=True)

                # TODO: Sending Serial commands too fast is causing G-Code commands to be skipped... make this better
                if (i+1) % len(self.boards) == 0:
                    time.sleep(1)


if __name__ == "__main__":
    PORT = "/dev/ttyACM1"
    BAUD_RATE = 250000

    board = DisplayBoard(PORT, BAUD_RATE)

    # Pause to establish connection or motors do weird things
    time.sleep(3)
    
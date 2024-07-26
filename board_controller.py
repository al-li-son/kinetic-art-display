import serial
import numpy as np

class DisplayBoard:
    def __init__(self, port, baudrate):
        self.axes = np.array(["X", "Y", "Z", "A", "B", "C", "U", "V"])
        self.serial = serial.Serial(port=port, baudrate=baudrate)

    def write_serial(self, command):
        self.serial.write(str(command+"\n").encode())

    def set_home(self):
        """
        Sets home position of all motors to all the way retracted
        """
        # Run motors all the way up and back down in relative positioning mode
        self.move([630,630,630,630,630,630,630,630], absolute=False)
        self.move([-630,-630,-630,-630,-630,-630,-630,-630], absolute=False)
        # Set home offset here
        self.write_serial("G90")
        self.write_serial("M428")

        # Back off
        self.move([30,30,30,30,30,30,30,30], absolute=False)

        # Reapproach
        self.move([0,0,0,0,0,0,0,0,0], absolute=True)
    
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
            

if __name__ == "__main__":
    PORT = "/dev/ttyACM0"
    BAUD_RATE = 250000

    board_0 = DisplayBoard(PORT, BAUD_RATE)

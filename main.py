from board_controller import *

def write_state(file_name, state_matrix):
    with open(file_name, "a") as pattern_file:
        for row in state_matrix:
            pattern_file.write(",".join(map(str, row)) + "\n")

def write_horizontal_wave(file_name, num_rows=5):
    row = [10]*8
    dir = [1]*8
    for i in range(8):
        for j in range(i):
            row[j] += 80
        write_state(file_name, [row for _ in range(num_rows)])

    for i in range(14):
        for j in range(8):
            if dir[j] > 0 and row[j] >= 570:
                dir[j] = -1
            elif dir[j] < 0 and row[j] <=10:
                continue
            row[j] += 80 * dir[j]
        write_state(file_name, [row for _ in range(num_rows)])        

if __name__ == "__main__":
    PORTS = ["/dev/ttyACM1"]
    BAUD_RATE = 250000

    write_horizontal_wave("patterns/1_row_wave.txt", num_rows=len(PORTS))

    # display = KineticDisplay(ports=PORTS, baudrate=BAUD_RATE)
    # time.sleep(3)

    # display.home_display()

    # for _ in range(1):
    #     display.show_pattern(file_name="1_row_wave.txt")


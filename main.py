from board_controller import *

def write_state(file_name, state_matrix):
    with open(file_name, "a") as pattern_file:
        for row in state_matrix:
            pattern_file.write(",".join(map(str, row)) + "\n")

def write_horizontal_wave(file_name, num_rows=5):
    """
    Moving wave along horizontal axis
    """
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

def write_horizontal_diag(file_name, num_rows=5):
    """
    Back and forth diagonal along horizontal axis
    """
    row = [280]*8
    write_state(file_name, [row for _ in range(num_rows)])
    row = [10, 90, 170, 250, 330, 410, 490, 570]
    write_state(file_name, [row for _ in range(num_rows)])
    row = [280]*8
    write_state(file_name, [row for _ in range(num_rows)])
    row = [570, 490, 410, 330, 250, 170, 90, 10]
    write_state(file_name, [row for _ in range(num_rows)])
    row = [280]*8
    write_state(file_name, [row for _ in range(num_rows)])

if __name__ == "__main__":
    PORTS = [f"/dev/ttyACM{i}" for i in range(5)]
    BAUD_RATE = 250000

    display = KineticDisplay(ports=PORTS, baudrate=BAUD_RATE)
    time.sleep(3)

    display.home_display()

    for _ in range(1):
        display.show_pattern(file_name="patterns/2_row_wave.txt")


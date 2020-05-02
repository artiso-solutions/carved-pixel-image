import os

def main():
    import argparse

    parser = argparse.ArgumentParser(description='print stick length for stick variant of pixel art.')
    parser.add_argument('input_files', metavar='stick-length', nargs='+', help='input images for processing')
    parser.add_argument('--current_line', help='start line beginning with 0', type=int, default=-1)

    args = parser.parse_args()

    for input_file in args.input_files:
        current_line_input_file = f'{os.path.splitext(input_file)[0]}_line.txt'

        

        with open(input_file, 'r') as file:
            starting_line = read_current_line(current_line_input_file, args.current_line)
            current_index = 0
            for line in file:
                if current_index < starting_line:
                    current_index += 1
                    continue

                print(line)
                input()

                current_index += 1
                update_current_line(current_line_input_file, current_index)

       


        

def read_current_line(current_line_input_file, override_line_number):
    print(f'reading current line from file {current_line_input_file} with override line number {override_line_number}')
    if override_line_number >= 0:
        return override_line_number
    
    if os.path.isfile(current_line_input_file):
            with open(current_line_input_file, 'r') as file: 
                for line in file:
                    print(f' - current read line is {line}')
                    print(f' - current read line is {int(line)}')
                    return int(line)
    
    return 0

    
def update_current_line(current_line_input_file, current_line_number):
    with open(current_line_input_file, 'w+') as file: 
        file.write(f'{current_line_number}\n')

if __name__ == "__main__":
    main()
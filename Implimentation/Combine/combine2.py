def read_lines_with_header(file_path, num_lines):
    """
    Read a specified number of lines from a file including the header.
    """
    lines = []
    with open(file_path, 'r') as file:
        header = file.readline()  # Read the header
        lines.append(header)
        for _ in range(num_lines - 1):  # Subtract 1 to account for the header
            line = file.readline()
            if not line:
                break
            lines.append(line)
    return lines

def main():
    # Count the number of lines in labeled_ddostrace.to-victim.20070804false.csv
    with open('labeled_ddostrace.to-victim.20070804false.csv', 'r') as file:
        num_lines = sum(1 for line in file)

    # Read the same number of lines from labeled_ddostrace.to-victim.20070804_143936.csv
    data_from_false = read_lines_with_header('labeled_ddostrace.to-victim.20070804false.csv', num_lines)
    data_from_large_file = read_lines_with_header('labeled_ddostrace.to-victim.20070804_143936.csv', num_lines)

    # Write the data to labeled_ddostrace.to-victim.20070804.csv
    with open('labeled_ddostrace.to-victim.20070804.csv', 'w') as file:
        for line_false, line_large_file in zip(data_from_false, data_from_large_file):
            file.write(line_false)
            file.write(line_large_file)

if __name__ == "__main__":
    main()

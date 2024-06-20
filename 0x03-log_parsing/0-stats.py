#!/usr/bin/python3
import sys
import signal

def print_msg(codes, file_size):
    print("File size: {}".format(file_size))
    for key in sorted(codes.keys()):
        if codes[key] > 0:
            print("{}: {}".format(key, codes[key]))

def signal_handler(sig, frame):
    print_msg(codes, file_size)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

file_size = 0
count_lines = 0
codes = {
    "200": 0,
    "301": 0,
    "400": 0,
    "401": 0,
    "403": 0,
    "404": 0,
    "405": 0,
    "500": 0
}

try:
    for line in sys.stdin:
        try:
            parts = line.split()
            if len(parts) < 9:
                continue
            
            # Extract status code and file size
            status_code = parts[-2]
            file_size_part = parts[-1]
            
            if status_code in codes:
                codes[status_code] += 1
            
            file_size += int(file_size_part)
            count_lines += 1

            if count_lines == 10:
                print_msg(codes, file_size)
                count_lines = 0
        
        except (ValueError, IndexError):
            # Skip the line if it doesn't match the expected format
            continue

except KeyboardInterrupt:
    print_msg(codes, file_size)
    sys.exit(0)

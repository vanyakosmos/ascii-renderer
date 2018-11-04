import glob
import os
import subprocess
import sys
import time


def file_times(path):
    for python_file in glob.glob(os.path.join(path, '**', '*.py'), recursive=True):
        yield os.stat(python_file).st_mtime


def print_stdout(process):
    stdout = process.stdout
    if stdout is not None:
        print(stdout)


def main():
    command = ' '.join(sys.argv[1:])
    path = '.'
    sleep_time = 1
    process = subprocess.Popen(command, shell=True)

    last_mtime = max(file_times(path))
    try:
        while True:
            max_mtime = max(file_times(path))
            print_stdout(process)
            if max_mtime > last_mtime:
                last_mtime = max_mtime
                print('Restarting process...')
                process.kill()
                process = subprocess.Popen(command, shell=True)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        process.kill()


if __name__ == '__main__':
    main()

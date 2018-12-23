#!/usr/bin/env python
import argparse

from renderer import test_3d, test_shaders


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')

    args = parser.parse_args()
    cmd = args.command
    if cmd == 'shader':
        test_shaders.main()
    elif cmd == '3d':
        test_3d.main()
    else:
        print(f"unknown command: {cmd!r}")


if __name__ == '__main__':
    main()

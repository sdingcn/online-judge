import subprocess
import time

def run_and_get_output(command, stdin = None):
    return subprocess.run(command, input = stdin, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True).stdout

def check(code):
    name = str(time.time()) + 'src'
    with open(f'{name}.cpp', 'w') as f:
        f.write(code)
    run_and_get_output(['clang++', f'{name}.cpp', '-o', f'{name}'])
    def check_io(stdin, stdout):
        if run_and_get_output([f'./{name}'], stdin).strip() == stdout.strip():
            return True
        else:
            return False
    if not check_io('0', '0'):
        return 'Wrong answer on test 1'
    if not check_io('3 2 1', '1 2 3'):
        return 'Wrong answer on test 2'
    if not check_io('1 2 3 4 5', '1 2 3 4 5'):
        return 'Wrong answer on test 3'
    return 'Accepted'

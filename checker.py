import subprocess
import time
import os
import os.path

def run_and_get_output(command, stdin = None):
    return subprocess.run(command, input = stdin, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True).stdout

def check(code):
    try:
        name = str(time.time())
        with open(f'{name}.cpp', 'w') as f:
            f.write(code)
        output = run_and_get_output(['clang++', f'{name}.cpp', '-o', f'{name}.executable']).strip()
        if output != '':
            return ('CE', output[:100])
        def check_io(stdin, stdout):
            if run_and_get_output([f'./{name}.executable'], stdin).strip() == stdout.strip():
                return True
            else:
                return False
        if not check_io('0', '0'):
            return ('WA', 'Wrong answer on test 1')
        if not check_io('3 2 1', '1 2 3'):
            return ('WA', 'Wrong answer on test 2')
        if not check_io('1 2 3 4 5', '1 2 3 4 5'):
            return ('WA', 'Wrong answer on test 3')
        return ('AC', 'Accepted')
    finally:
        if os.path.exists(f'{name}.cpp'):
            os.remove(f'{name}.cpp')
        if os.path.exists(f'{name}.executable'):
            os.remove(f'{name}.executable')

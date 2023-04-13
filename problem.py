import subprocess
import os
import os.path
import time
import hashlib

# returns the problem description
def describe() -> str:
    return '''\
Use C++11 to implement sorting.
Input: Integers a[1] a[2] ... a[n] separated by whitespaces (n >= 1, -100 <= a[i] <= 100).
Output: Sorted integers separated by whitespaces.
'''

# returns (score, details)
def judge(code: str) -> (str, str):
    try:
        def run_and_get_output(command, stdin = None):
            return subprocess.run(command, input = stdin, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True).stdout
        m = hashlib.sha256()
        m.update(code.encode())
        name = str(time.time()) + '-' + m.hexdigest()[:7]
        with open(f'{name}.cpp', 'w') as f:
            f.write(code)
        output = run_and_get_output(['clang++', '-std=c++11', '-o', f'{name}.executable', f'{name}.cpp']).strip()
        if output != '':
            return ('0', output[:100])
        def check_io(stdin, stdout):
            if run_and_get_output([f'./{name}.executable'], stdin).strip() == stdout.strip():
                return True
            else:
                return False
        if not check_io('0', '0'):
            return ('0', 'Wrong answer on test 1')
        if not check_io('3 -2 1', '-2 1 3'):
            return ('33', 'Wrong answer on test 2')
        if not check_io('1 2 3 4 5', '1 2 3 4 5'):
            return ('66', 'Wrong answer on test 3')
        return ('100', 'Accepted')
    finally:
        if os.path.exists(f'{name}.cpp'):
            os.remove(f'{name}.cpp')
        if os.path.exists(f'{name}.executable'):
            os.remove(f'{name}.executable')

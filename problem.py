import subprocess
import os
import os.path
import time
import hashlib
import re

def describe() -> str:
    return '''\
Use C++11 to implement sorting.
Input: Integers a[1] a[2] ... a[n] separated by whitespaces (1 <= n <= 100, -100 <= a[i] <= 100).
Output: Sorted integers separated by whitespaces.
Time limit: 1 second.
Space limit: no limit.
'''

def security_check(code: str) -> bool:
    condensed = re.sub(r'\s+', '', code)
    if '#include"' in condensed:
        return False
    headers = re.findall(r'#include<(.*?)>', condensed)
    for header in headers:
        if header not in ['iostream', 'iomanip', 'vector', 'deque', 'list', 'map', 'set', 'algorithm', 'utility', 'tuple', 'cmath']:
            return False
    return True

def execute(cmd: list, tout = None, ipt = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        timeout = tout,
        input = ipt,
        capture_output = True,
        universal_newlines = True
    )

T = [
    ('0', '0'),
    ('3 -2 1', '-2 1 3'),
    ('1 2 3 4 5', '1 2 3 4 5'),
    ('10 9 8 7 6 5 4 3 2 1', '1 2 3 4 5 6 7 8 9 10'),
    ('-1 -1 -1', '-1 -1 -1'),
    ('5 4 9 7 3', '3 4 5 7 9'),
    ('100 99 1', '1 99 100'),
    ('0 0 0 0 -100', '-100 0 0 0 0')
]

def run_test(name: str, stdin: str, stdout: str) -> str:
    try:
        if execute([f'./{name}.executable'], 1, stdin).stdout.strip() == stdout.strip():
            return 'AC'
        else:
            return 'WA/RE/MLE'
    except subprocess.TimeoutExpired:
        return 'TLE'

def judge(code: str) -> (str, str):
    try:
        name = time.time()
        n = len(T)
        if not security_check(code):
            return (f'0/{n}', 'Security check not passed')
        with open(f'{name}.cpp', 'w') as f:
            f.write(code)
        try:
            err = execute(['clang++', '-std=c++11', '-o', f'{name}.executable', f'{name}.cpp']).stderr
        except subprocess.TimeoutExpired:
            return (f'0/{n}', 'Compilation timed out')
        if err != '':
            return (f'0/{n}', 'Compilation Error: ' + err[:100])
        cnt = 0
        score = 0
        for i, o in T:
            cnt += 1
            r = run_test(name, i, o)
            if r == 'AC':
                score += 1
            elif r == 'WA/RE/MLE':
                return (f'{score}/{n}', f'Wrong answer / runtime error / memory limit exceeded on test {cnt}')
            else:
                return (f'{score}/{n}', f'Time limit exceeded on test {cnt}')
        return (f'{score}/{n}', f'Accepted ({n}/{n} tests passed)')
    finally:
        if os.path.exists(f'{name}.cpp'):
            os.remove(f'{name}.cpp')
        if os.path.exists(f'{name}.executable'):
            os.remove(f'{name}.executable')

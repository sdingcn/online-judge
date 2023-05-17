# online-judge

## summary

A simple online judge (not recommend for public use).

## platforms and dependencies

Tested on Python 3.9.6 (macOS 13.2.1).

It should work on other major platforms with Python 3.x.

## usage

### Prepare your problem
Provide two functions in `problem.py`. The original `problem.py` contains an example.

`def describe() -> str:` returns your problem description.

`def judge(code: str) -> (str, str):` takes the submitted code and returns `(score, judging details)`.

**It's your responsibility to ensure your `describe` and `judge` don't interfere with each other when executed concurrently.**

**It's your responsibility to do security checks and/or set sandboxes before executing the code.**

### Start/stop the web server
Run `python3 server.py` to start the server on `localhost:8008`.

Run `python3 server.py [host] [port]` to start the server on `[host]:[port]`.

Hit `Ctrl-C` to stop the server.

### Inspect logs
For each submission, `logs/{timestamp}-{underscored_name}.code` contains the code, and `logs/{timestamp}-{underscored_name}.result` contains the score and judging details.

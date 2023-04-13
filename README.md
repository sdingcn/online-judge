# online-judge

## Introduction
An extremely small online judge template.

## Prepare your problem
Provide two functions in `problem.py`.

`def describe() -> str:` returns your problem description.

`def judge(code: str) -> (str, str):` takes the submitted code and returns `(score, judging details)`.

**It's your responsibility to ensure your `describe` and `judge` functions don't interfere with each other when executed concurrently.**

## Start/stop the web server
Run `python3 server.py` to start the server on `localhost:8008`.

Run `python3 server.py [host] [port]` to start the server on `[host]:[port]`.

Hit `Ctrl-C` to stop the server.

## Inspect logs
For each submission, `logs/{timestamp}-{underscored_name}-{score}.code` contains the code, and `logs/{timestamp}-{underscored_name}-{score}.details` contains the judging details.

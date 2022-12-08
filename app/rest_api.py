from flask import Request


class ExecutionRequest:
    command: str = None
    stdout_file: str = "/dev/null"
    stderr_file: str = "/dev/null"

    def __int__(self, command: str, arguments: str):
        self.command = command

    def __init__(self, json_request: Request):
        json_request = json_request.get_json()
        if 'command' in json_request:
            self.command = json_request['command']
        else:
            raise ValueError("ExecutionRequest don't have required 'command' field")
        if 'stdoutFile' in json_request:
            self.stdout_file = json_request['stdoutFile']
        if 'stderrFile' in json_request:
            self.stderr_file = json_request['stderrFile']

    def __str__(self) -> str:
        return f"ApiRequest(command='{self.command}')"

    def __repr__(self) -> str:
        return self.__str__()




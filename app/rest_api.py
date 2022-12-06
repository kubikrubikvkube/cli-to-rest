from flask import Request


class ExecutionRequest:
    command: str = ''
    arguments: str = ''

    def __int__(self, command: str, arguments: str):
        self.command = command
        self.arguments = arguments

    def __init__(self, json_request: Request):
        json_request = json_request.get_json()
        if 'command' in json_request:
            self.command = json_request['command']
        if 'arguments' in json_request:
            self.arguments = json_request['arguments']

    def __str__(self) -> str:
        return f"ApiRequest(command='{self.command}', arguments='{self.arguments}')"

    def __repr__(self) -> str:
        return self.__str__()




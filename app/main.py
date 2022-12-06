from subprocess import CompletedProcess

from flask import Flask, request, jsonify, Response

import executor
from rest_api import ExecutionRequest

app = Flask(__name__)


@app.route('/pid/<pid>', methods=['GET'])
def get_id(pid):
    completed_process = executor.execute(f"ps aux | grep {pid}")
    return create_api_response(completed_process)


@app.route('/execute', methods=['POST'])
def execute():
    api_request: ExecutionRequest = ExecutionRequest(request)
    completed_process = executor.execute(api_request.command, api_request.arguments)
    return create_api_response(completed_process)


def create_api_response(completed_process: CompletedProcess) -> Response:
    if completed_process is None:
        return jsonify({"error": "Unknown error"})

    std_out = completed_process.stdout
    std_err = completed_process.stderr
    std_out_lines = list(filter(lambda s: s != "", std_out.splitlines()))
    std_err_lines = list(filter(lambda s: s != "", std_err.splitlines()))

    return jsonify(
        {
            "stdout": std_out_lines,
            "stderr": std_err_lines
        }
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0")

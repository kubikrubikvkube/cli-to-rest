from subprocess import CompletedProcess

from flask import Flask, request, jsonify, Response

import executor
from rest_api import ExecutionRequest

app = Flask(__name__)


@app.route('/pid/<pid>', methods=['GET'])
def get_process_info(pid):
    return {
        "isRunning": executor.is_running(pid),
        "processInfo": executor.process_info(pid)
    }


@app.route('/pid/<pid>', methods=['DELETE'])
def kill_process(pid):
    is_running = executor.is_running(pid)
    executor.execute(f"kill -9 {pid}")
    if is_running:
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/execute/sync', methods=['POST'])
def execute_sync():
    ex_request: ExecutionRequest = ExecutionRequest(request)
    completed_process = executor.execute(ex_request.command)
    return create_sync_api_response(completed_process)


@app.route('/execute/async', methods=['POST'])
def execute_async():
    ex_request: ExecutionRequest = ExecutionRequest(request)
    async_command = f"{ex_request.command} >> {ex_request.stdout_file} 2>{ex_request.stderr_file} & echo $!"
    command_result = executor.execute(async_command)
    return create_async_api_response(command_result)


def create_sync_api_response(completed_process: CompletedProcess) -> Response:
    if completed_process is None:
        return jsonify({"error": "Unknown error"})

    stdout = completed_process.stdout
    stderr = completed_process.stderr
    stdout_lines = list(filter(lambda s: s != "", stdout.splitlines()))
    stderr_lines = list(filter(lambda s: s != "", stderr.splitlines()))

    return jsonify(
        {
            "stdout": stdout_lines,
            "stderr": stderr_lines
        }
    )


def create_async_api_response(completed_process: CompletedProcess) -> Response:
    if completed_process is None:
        return jsonify({"error": "Unknown error"})
    process_pid = completed_process.stdout.strip()
    return jsonify(
        {
            "pid": int(process_pid)
        }
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0")

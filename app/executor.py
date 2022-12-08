import logging
import subprocess

error_response = {}


def execute(command: str, timeout: int = None, byte_input: str | bytes = None) -> subprocess.CompletedProcess:
    if command is None or len(command) == 0:
        raise ValueError("At least 1 command should be provided for execution")

    try:
        completed_process: subprocess.CompletedProcess = subprocess.run(command,
                                                                        capture_output=True,
                                                                        check=True,
                                                                        text=True,
                                                                        shell=True,
                                                                        timeout=timeout,
                                                                        input=byte_input)
        logging.info(f"Executed ${str(completed_process)} with code {completed_process.returncode}")
        return completed_process
    except subprocess.SubprocessError as subprocess_error:
        logging.error(f"SubprocessError: {str(subprocess_error)}")
    except Exception as exception:
        logging.error(f"Exception: {str(exception)}")


def is_running(pid: int) -> bool:
    pid_info = execute(f"ps -p {pid}")
    if pid_info is None:
        return False
    stdout = pid_info.stdout
    stdout_lines = list(filter(lambda s: s != "", stdout.splitlines()))
    headers_row = 1
    return True if len(stdout_lines) > headers_row else False


def process_info(pid: int) -> dict[str, str]:
    pid_info = execute(f"ps -Fp {pid}")
    if pid_info is None:
        return error_response
    stdout = pid_info.stdout
    stdout_lines = list(filter(lambda s: s != "", stdout.splitlines()))

    if len(stdout_lines) != 2:
        return error_response
    normalized_info_line = " ".join(stdout_lines[1].split())
    lines = normalized_info_line.split(" ")

    try:
        response = {
            "userIdNumber": lines[0],
            "processId": int(lines[1]),
            "parentProcessId": int(lines[2]),
            "cpuUtilization": int(lines[3]),
            "size": int(lines[4]),
            "residentSetSize": int(lines[5]),
            "assignedProcessor": int(lines[6]),
            "startTime": lines[7],
            "controllingTerminal": lines[8],
            "cumulativeCpuTime": lines[9],
            "command": lines[10]
        }
    except Exception as e:
        logging.error(e)
        return error_response
    return response

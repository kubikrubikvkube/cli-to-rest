import logging
import subprocess


def execute(*command_and_args: str, timeout: int = None, byte_input: str | bytes = None) -> subprocess.CompletedProcess:

    if len(command_and_args) == 0:
        raise ValueError("At least 1 command should be provided for execution")

    try:
        completed_process: subprocess.CompletedProcess = subprocess.run(command_and_args,
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

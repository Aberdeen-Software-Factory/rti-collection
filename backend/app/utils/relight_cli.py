import subprocess


class RelightCliNotFoundError(Exception):
    def __init__(self, message="Relight CLI executable not found"):
        super().__init__(message)


class RelightCliError(Exception):
    def __init__(self, message):
        super().__init__("relight-cli error: " + message)


def call_relight_cli(input_file, output_file):
    try:
        result = subprocess.run(
            ["relight-cli", input_file, output_file],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise RelightCliNotFoundError()
    
    if result.returncode != 0:
        raise RelightCliError(result.stderr)
    return output_file

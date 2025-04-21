import subprocess

class CommandHandler:
    @staticmethod
    def execute(command: str) -> str:
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                text=True
            )
            output = result.stdout.strip()
            error = result.stderr.strip()

            if result.returncode != 0:
                return f"Error: {error}" if error else "Unknown error"
            return output or "(no output)"
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Exception: {str(e)}"

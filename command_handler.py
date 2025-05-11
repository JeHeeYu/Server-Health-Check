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
                print(f"[CommandHandler] Error:\n{error}")
                return f"Error: {error}" if error else "Unknown error"

            print(f"[CommandHandler] Output:\n{output}")
            return output or "(no output)"
        except subprocess.TimeoutExpired:
            print("[CommandHandler] Timeout")
            return "Command timed out"
        except Exception as e:
            print(f"[CommandHandler] Exception: {e}")
            return f"Exception: {str(e)}"

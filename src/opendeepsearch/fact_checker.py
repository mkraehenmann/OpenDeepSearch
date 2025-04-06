from smolagents import Tool
import io
import contextlib
import traceback

class CodeRunnerTool(Tool):
    name = "run_code"
    description = """
    Executes Python code locally and returns the output or any error messages.
    """
    inputs = {
        "code": {
            "type": "string",
            "description": "The Python code to execute.",
        },
    }
    output_type = "string"
    
    def forward(self, code: str) -> str:
        try:
            output_capture = io.StringIO()
            error_capture = io.StringIO()
            with contextlib.redirect_stdout(output_capture), contextlib.redirect_stderr(error_capture):
                exec(compile(code, "<string>", "exec"), {})
            stdout = output_capture.getvalue()
            stderr = error_capture.getvalue()
            if stderr:
                return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
            return stdout if stdout else "No output."
        except Exception as e:
            return f"Error executing code:\n{traceback.format_exc()}"
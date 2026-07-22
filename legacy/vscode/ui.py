import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import subprocess
import threading

class ScriptRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Script Runner")
        self.root.geometry("600x500")

        # Create a button to load a script
        self.load_button = tk.Button(root, text="Load Python Script", command=self.load_script)
        self.load_button.pack(pady=10)

        # Create an input field for script parameters
        self.param_label = tk.Label(root, text="Script Parameters (comma-separated):")
        self.param_label.pack(pady=5)
        self.param_entry = tk.Entry(root, width=70)
        self.param_entry.pack(pady=5)

        # Create a text area to display the output
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.output_area.pack(pady=10)

        # Create a button to run the script
        self.run_button = tk.Button(root, text="Run Script", command=self.run_script)
        self.run_button.pack(pady=10)

        self.script_path = None

    def load_script(self):
        self.script_path = filedialog.askopenfilename(
            title="Select a Python Script",
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*"))
        )
        if self.script_path:
            self.output_area.insert(tk.END, f"Loaded script: {self.script_path}\n")

    def run_script(self):
        if not self.script_path:
            self.output_area.insert(tk.END, "No script loaded. Please load a script first.\n")
            return

        # Clear the output area
        self.output_area.delete(1.0, tk.END)

        # Get parameters from the input field
        params = self.param_entry.get().split(',')
        params = [param.strip() for param in params if param.strip()]  # Clean up empty strings

        # Start a new thread to run the script
        threading.Thread(target=self.execute_script, args=(params,)).start()

    def execute_script(self, params):
        try:
            # Run the script and capture the output
            result = subprocess.run(['python', self.script_path] + params, capture_output=True, text=True, check=True)
            output = result.stdout
            error = result.stderr

            if output:
                self.output_area.insert(tk.END, output)
            if error:
                self.output_area.insert(tk.END, f"Error: {error}\n", 'error')

        except subprocess.CalledProcessError as e:
            self.output_area.insert(tk.END, f"Error: {e.stderr}\n", 'error')
        except Exception as e:
            self.output_area.insert(tk.END, f"Unexpected error: {str(e)}\n", 'error')

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptRunnerApp(root)
    root.mainloop()

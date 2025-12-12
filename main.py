import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from recorder import Recorder
from document_generator import DocumentGenerator
import os

class QARecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QA Recorder App")
        self.root.geometry("400x300")

        self.recorder = Recorder()
        self.doc_generator = DocumentGenerator()
        self.is_recording = False

        self._build_ui()
        self._update_status()

    def _build_ui(self):
        # Title
        title_label = ttk.Label(self.root, text="QA Test Recorder", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Output Format Selection
        format_frame = ttk.Frame(self.root)
        format_frame.pack(pady=5)
        ttk.Label(format_frame, text="Output Format:").pack(side=tk.LEFT, padx=5)
        self.output_format = tk.StringVar(value="docx")
        format_combo = ttk.Combobox(format_frame, textvariable=self.output_format, values=["docx", "pdf"], state="readonly", width=10)
        format_combo.pack(side=tk.LEFT)

        # Buttons
        self.start_btn = ttk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_btn.pack(pady=10)

        self.stop_btn = ttk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_btn.pack(pady=10)

        # Status
        self.status_label = ttk.Label(self.root, text="Ready", foreground="green")
        self.status_label.pack(pady=20)
        
        # Info
        info_label = ttk.Label(self.root, text="Captures screen on change (min 10s interval)", font=("Helvetica", 8))
        info_label.pack(side=tk.BOTTOM, pady=5)

    def start_recording(self):
        self.recorder.start()
        self.is_recording = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Recording...", foreground="red")

    def stop_recording(self):
        if not self.is_recording:
            return

        self.recorder.stop()
        self.is_recording = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processing report...", foreground="blue")
        
        # Process data in a separate thread to avoid freezing UI
        threading.Thread(target=self._save_report).start()

    def _save_report(self):
        data = self.recorder.get_data()
        if not data:
            self.root.after(0, lambda: messagebox.showinfo("Info", "No changes detected during recording."))
            self.root.after(0, lambda: self.status_label.config(text="Ready", foreground="green"))
            return

        fmt = self.output_format.get()
        default_ext = f".{fmt}"
        
        # Ask user where to save
        # Note: filedialog must be called from main thread usually, but let's try or use a default
        # To be safe with threading, we'll save to a default name first or ask before stopping?
        # Simpler: Save to default and rename, or just save to default.
        # Let's use a default name with timestamp
        timestamp = int(time.time())
        filename = f"QA_Report_{timestamp}{default_ext}"
        
        try:
            if fmt == "docx":
                saved_file = self.doc_generator.generate_docx(data, filename)
            else:
                saved_file = self.doc_generator.generate_pdf(data, filename)
            
            self.recorder.clear_temp_files()
            
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Report saved as {saved_file}"))
            self.root.after(0, lambda: self.status_label.config(text="Ready", foreground="green"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to save report: {e}"))
            self.root.after(0, lambda: self.status_label.config(text="Error", foreground="red"))

    def _update_status(self):
        # Optional: Update status with capture count if needed
        if self.is_recording:
            count = len(self.recorder.captured_data)
            self.status_label.config(text=f"Recording... ({count} captures)")
        self.root.after(1000, self._update_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = QARecorderApp(root)
    root.mainloop()

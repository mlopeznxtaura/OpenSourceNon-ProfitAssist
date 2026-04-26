"""Modular Engine GUI Application."""
import logging
from typing import Any, Dict, Optional

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    TK_AVAILABLE = True
except ImportError:
    TK_AVAILABLE = False

from modular_engine.core.engine import Engine


logger = logging.getLogger(__name__)


class ModularEngineGUI:
    """Graphical User Interface for Modular Engine.
    
    Provides a visual interface for:
    - Monitoring engine status
    - Managing modules
    - Processing data
    - Viewing logs and results
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        """Initialize the GUI.
        
        Args:
            engine: Optional engine instance to control
        """
        if not TK_AVAILABLE:
            raise ImportError("tkinter is not available. Install with: pip install tk")
        
        self.engine = engine or Engine()
        self._root = None
        self._status_var = None
        self._log_text = None
        self._module_listbox = None
        self._input_text = None
        self._output_text = None
        
        logger.info("GUI initialized")
    
    def launch(self) -> None:
        """Launch the GUI application."""
        self._root = tk.Tk()
        self._root.title("Modular Engine Control Panel")
        self._root.geometry("1000x700")
        
        self._setup_ui()
        self._update_status()
        
        logger.info("GUI launched")
        self._root.mainloop()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self._root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Modular Engine Control Panel",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Engine Status", padding="5")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        status_frame.columnconfigure(1, weight=1)
        
        self._status_var = tk.StringVar(value="Not Initialized")
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self._status_var).grid(row=0, column=1, sticky=tk.W)
        
        # Control buttons
        btn_frame = ttk.Frame(status_frame)
        btn_frame.grid(row=0, column=2, padx=10)
        
        ttk.Button(btn_frame, text="Initialize", command=self._initialize_engine).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Shutdown", command=self._shutdown_engine).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Refresh", command=self._update_status).pack(side=tk.LEFT, padx=2)
        
        # Modules frame
        module_frame = ttk.LabelFrame(main_frame, text="Modules", padding="5")
        module_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        module_frame.columnconfigure(0, weight=1)
        
        self._module_listbox = tk.Listbox(module_frame, height=5)
        self._module_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        module_btn_frame = ttk.Frame(module_frame)
        module_btn_frame.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        ttk.Button(module_btn_frame, text="Refresh Modules", command=self._refresh_modules).pack(side=tk.LEFT, padx=2)
        
        # Input/Output frame
        io_frame = ttk.Frame(main_frame)
        io_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        io_frame.columnconfigure(0, weight=1)
        io_frame.columnconfigure(1, weight=1)
        io_frame.rowconfigure(1, weight=1)
        
        # Input
        input_label = ttk.Label(io_frame, text="Input Data (JSON):")
        input_label.grid(row=0, column=0, sticky=tk.W)
        
        self._input_text = scrolledtext.ScrolledText(io_frame, width=40, height=8)
        self._input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Output
        output_label = ttk.Label(io_frame, text="Output:")
        output_label.grid(row=0, column=1, sticky=tk.W)
        
        self._output_text = scrolledtext.ScrolledText(io_frame, width=40, height=8)
        self._output_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Process button
        process_btn = ttk.Button(io_frame, text="Process", command=self._process_data)
        process_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="5")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self._log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self._log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        ttk.Button(log_frame, text="Clear Logs", command=self._clear_logs).grid(row=1, column=0, sticky=tk.W, pady=2)
    
    def _initialize_engine(self) -> None:
        """Initialize the engine."""
        try:
            success = self.engine.initialize()
            if success:
                self._log_message("Engine initialized successfully")
                self._update_status()
            else:
                self._log_message("Engine initialized with errors", level="warning")
                self._update_status()
        except Exception as e:
            self._log_message(f"Error initializing engine: {str(e)}", level="error")
            messagebox.showerror("Initialization Error", str(e))
    
    def _shutdown_engine(self) -> None:
        """Shutdown the engine."""
        try:
            self.engine.shutdown()
            self._log_message("Engine shutdown complete")
            self._update_status()
        except Exception as e:
            self._log_message(f"Error shutting down engine: {str(e)}", level="error")
            messagebox.showerror("Shutdown Error", str(e))
    
    def _update_status(self) -> None:
        """Update the status display."""
        try:
            status = self.engine.get_status()
            status_text = f"Initialized: {status['initialized']} | Running: {status['running']} | Modules: {status['module_count']}"
            self._status_var.set(status_text)
            self._refresh_modules()
        except Exception as e:
            self._log_message(f"Error updating status: {str(e)}", level="error")
    
    def _refresh_modules(self) -> None:
        """Refresh the module list."""
        try:
            self._module_listbox.delete(0, tk.END)
            modules = self.engine.list_modules()
            
            if not modules:
                self._module_listbox.insert(tk.END, "No modules loaded")
            else:
                for module in modules:
                    display = f"{module['name']} ({module['layer']}) v{module['version']}"
                    self._module_listbox.insert(tk.END, display)
        except Exception as e:
            self._log_message(f"Error refreshing modules: {str(e)}", level="error")
    
    def _process_data(self) -> None:
        """Process input data through the engine."""
        try:
            import json
            
            input_str = self._input_text.get("1.0", tk.END).strip()
            
            if not input_str:
                messagebox.showwarning("No Input", "Please enter input data")
                return
            
            input_data = json.loads(input_str)
            result = self.engine.process(input_data)
            
            output_str = json.dumps(result, indent=2)
            self._output_text.delete("1.0", tk.END)
            self._output_text.insert("1.0", output_str)
            
            self._log_message("Data processed successfully")
        except json.JSONDecodeError as e:
            self._log_message(f"Invalid JSON input: {str(e)}", level="error")
            messagebox.showerror("JSON Error", f"Invalid JSON format: {str(e)}")
        except Exception as e:
            self._log_message(f"Error processing data: {str(e)}", level="error")
            messagebox.showerror("Processing Error", str(e))
    
    def _log_message(self, message: str, level: str = "info") -> None:
        """Add a message to the log display.
        
        Args:
            message: Message to log
            level: Log level (info, warning, error)
        """
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
        
        self._log_text.configure(state='normal')
        self._log_text.insert(tk.END, log_entry)
        self._log_text.see(tk.END)
        self._log_text.configure(state='disabled')
        
        # Also log using standard logging
        log_func = getattr(logger, level, logger.info)
        log_func(message)
    
    def _clear_logs(self) -> None:
        """Clear the log display."""
        self._log_text.configure(state='normal')
        self._log_text.delete("1.0", tk.END)
        self._log_text.configure(state='disabled')
        self._log_message("Logs cleared")


def launch_gui(engine: Optional[Engine] = None) -> None:
    """Convenience function to launch the GUI.
    
    Args:
        engine: Optional engine instance to control
    """
    gui = ModularEngineGUI(engine)
    gui.launch()

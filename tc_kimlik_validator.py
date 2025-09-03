import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import re
import os
from datetime import datetime

class TCKimlikValidatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TC Kimlik No Validator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def validate_tc_kimlik(self, tc_no):
        """Validates Turkish TC Kimlik No"""
        tc_str = str(tc_no).replace(' ', '').replace('-', '')
        
        if not re.match(r'^\d{11}$', tc_str):
            return False
        
        if tc_str[0] == '0':
            return False
        
        digits = [int(d) for d in tc_str]
        
        # Calculate checksum
        odd_sum = sum(digits[i] for i in range(0, 9, 2))
        even_sum = sum(digits[i] for i in range(1, 8, 2))
        
        tenth_digit_check = ((odd_sum * 7) - even_sum) % 10
        if tenth_digit_check != digits[9]:
            return False
        
        first_ten_sum = sum(digits[:10])
        eleventh_digit_check = first_ten_sum % 10
        if eleventh_digit_check != digits[10]:
            return False
        
        return True
    
    def find_tc_numbers_in_text(self, text):
        """Finds TC numbers in text"""
        pattern = r'\b\d{1,2}[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{1,2}\b|\b\d{11}\b'
        potential_tc_numbers = re.findall(pattern, text)
        
        valid_numbers = []
        invalid_numbers = []
        
        for tc in potential_tc_numbers:
            clean_tc = re.sub(r'[\s-]', '', tc)
            if len(clean_tc) == 11 and clean_tc.isdigit():
                if self.validate_tc_kimlik(clean_tc):
                    valid_numbers.append(clean_tc)
                else:
                    invalid_numbers.append(clean_tc)
        
        return valid_numbers, invalid_numbers
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="TC Kimlik No Validator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Single TC Number Validation Section
        single_frame = ttk.LabelFrame(main_frame, text="Single TC Number Validation", padding="10")
        single_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        single_frame.columnconfigure(1, weight=1)
        
        ttk.Label(single_frame, text="TC Number:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.single_tc_var = tk.StringVar()
        self.single_tc_entry = ttk.Entry(single_frame, textvariable=self.single_tc_var, width=20)
        self.single_tc_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.single_tc_entry.bind('<KeyRelease>', self.on_single_tc_change)
        
        self.validate_single_btn = ttk.Button(single_frame, text="Validate", 
                                            command=self.validate_single_tc)
        self.validate_single_btn.grid(row=0, column=2, padx=(5, 0))
        
        self.single_result_var = tk.StringVar()
        self.single_result_label = ttk.Label(single_frame, textvariable=self.single_result_var, 
                                           font=('Arial', 10, 'bold'))
        self.single_result_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Bulk Text Analysis Section
        bulk_frame = ttk.LabelFrame(main_frame, text="Bulk Text Analysis", padding="10")
        bulk_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        bulk_frame.columnconfigure(0, weight=1)
        bulk_frame.rowconfigure(1, weight=1)
        
        # Text input area
        text_label = ttk.Label(bulk_frame, text="Enter text or load from file:")
        text_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_area = scrolledtext.ScrolledText(bulk_frame, height=10, width=70)
        self.text_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(bulk_frame)
        buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(buttons_frame, text="Load from File", 
                  command=self.load_file).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(buttons_frame, text="Clear Text", 
                  command=self.clear_text).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(buttons_frame, text="Analyze Text", 
                  command=self.analyze_text).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(buttons_frame, text="Save Results", 
                  command=self.save_results).grid(row=0, column=3)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.results_area = scrolledtext.ScrolledText(results_frame, height=8, width=70)
        self.results_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for main frame
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Initialize results storage
        self.last_analysis_results = None
        
    def on_single_tc_change(self, event=None):
        """Real-time validation as user types"""
        tc_number = self.single_tc_var.get().strip()
        if tc_number:
            if len(tc_number) == 11:
                if self.validate_tc_kimlik(tc_number):
                    self.single_result_var.set("✅ Valid TC Number")
                    self.single_result_label.configure(foreground='green')
                else:
                    self.single_result_var.set("❌ Invalid TC Number")
                    self.single_result_label.configure(foreground='red')
            else:
                self.single_result_var.set(f"Enter 11 digits ({len(tc_number)}/11)")
                self.single_result_label.configure(foreground='blue')
        else:
            self.single_result_var.set("")
    
    def validate_single_tc(self):
        """Validate single TC number"""
        tc_number = self.single_tc_var.get().strip()
        if not tc_number:
            messagebox.showwarning("Warning", "Please enter a TC number")
            return
            
        is_valid = self.validate_tc_kimlik(tc_number)
        if is_valid:
            self.single_result_var.set("✅ Valid TC Number")
            self.single_result_label.configure(foreground='green')
            self.status_var.set(f"TC {tc_number} is valid")
        else:
            self.single_result_var.set("❌ Invalid TC Number")
            self.single_result_label.configure(foreground='red')
            self.status_var.set(f"TC {tc_number} is invalid")
    
    def load_file(self):
        """Load text from file"""
        file_path = filedialog.askopenfilename(
            title="Select file to analyze",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete('1.0', tk.END)
                    self.text_area.insert('1.0', content)
                    self.status_var.set(f"Loaded file: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")
    
    def clear_text(self):
        """Clear text area"""
        self.text_area.delete('1.0', tk.END)
        self.results_area.delete('1.0', tk.END)
        self.status_var.set("Text cleared")
    
    def analyze_text(self):
        """Analyze text for TC numbers"""
        text = self.text_area.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze")
            return
        
        self.status_var.set("Analyzing...")
        self.root.update()
        
        valid_numbers, invalid_numbers = self.find_tc_numbers_in_text(text)
        
        # Prepare results 
        results = []
        results.append(f"=== TC Kimlik Analysis Results ===")
        results.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        results.append(f"Text Length: {len(text)} characters")
        results.append("")
        
        results.append(f"📊 Summary:")
        results.append(f"   Valid TC Numbers Found: {len(valid_numbers)}")
        results.append(f"   Invalid TC Numbers Found: {len(invalid_numbers)}")
        results.append(f"   Total Numbers Analyzed: {len(valid_numbers) + len(invalid_numbers)}")
        results.append("")
        
        if valid_numbers:
            results.append("✅ Valid TC Numbers:")
            for i, tc in enumerate(valid_numbers, 1):
                formatted_tc = f"{tc[:3]} {tc[3:6]} {tc[6:8]} {tc[8:]}"
                results.append(f"   {i}. {formatted_tc} ({tc})")
            results.append("")
        
        if invalid_numbers:
            results.append("❌ Invalid TC Numbers:")
            for i, tc in enumerate(invalid_numbers, 1):
                formatted_tc = f"{tc[:3]} {tc[3:6]} {tc[6:8]} {tc[8:]}"
                results.append(f"   {i}. {formatted_tc} ({tc})")
            results.append("")
        
        if not valid_numbers and not invalid_numbers:
            results.append("ℹ️ No TC numbers found in the text.")
        
        # Display results
        self.results_area.delete('1.0', tk.END)
        self.results_area.insert('1.0', '\n'.join(results))
        
        # Store results for saving 
        self.last_analysis_results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'valid_numbers': valid_numbers,
            'invalid_numbers': invalid_numbers,
            'text_length': len(text),
            'results_text': '\n'.join(results)
        }
        
        self.status_var.set(f"Analysis complete: {len(valid_numbers)} valid, {len(invalid_numbers)} invalid TC numbers found")
    
    def save_results(self):
        """Save analysis results to file"""
        if not self.last_analysis_results:
            messagebox.showwarning("Warning", "No analysis results to save. Please analyze some text first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save results",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.last_analysis_results['results_text'])
                messagebox.showinfo("Success", f"Results saved to {os.path.basename(file_path)}")
                self.status_var.set(f"Results saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")

def main():
    root = tk.Tk()
    app = TCKimlikValidatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

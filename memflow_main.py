"""
MemFlow: Virtual Memory Manager with TLB Simulation
Main Application File
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import random
from collections import OrderedDict
from datetime import datetime

class MemFlow:
    def __init__(self, root):
        self.root = root
        self.root.title("MemFlow - Virtual Memory Manager")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Memory Configuration
        self.PAGE_SIZE = 4096  # 4KB
        self.VIRTUAL_MEMORY_SIZE = 2**32  # 4GB
        self.PHYSICAL_MEMORY_SIZE = 2**24  # 16MB
        self.NUM_PAGES = self.VIRTUAL_MEMORY_SIZE // self.PAGE_SIZE
        self.NUM_FRAMES = self.PHYSICAL_MEMORY_SIZE // self.PAGE_SIZE
        self.TLB_SIZE = 16
        
        # Data Structures
        self.page_table = {}  # {page_number: frame_number}
        self.tlb = OrderedDict()  # {page_number: frame_number}
        self.physical_memory = [None] * self.NUM_FRAMES
        self.free_frames = list(range(self.NUM_FRAMES))
        
        # Statistics
        self.total_accesses = 0
        self.tlb_hits = 0
        self.tlb_misses = 0
        self.page_faults = 0
        self.tlb_policy = "FIFO"  # or "LRU"
        
        # History
        self.access_history = []
        
        self.create_ui()
        
    def create_ui(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='#ffffff')
        style.configure('TButton', background='#2d2d2d', foreground='#ffffff')
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#4CAF50')
        
        # Main Container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_container, text="MemFlow", style='Header.TLabel')
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        subtitle = ttk.Label(main_container, text="Virtual Memory Manager with TLB Simulation")
        subtitle.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Left Panel - Controls
        self.create_control_panel(main_container)
        
        # Middle Panel - Visualization
        self.create_visualization_panel(main_container)
        
        # Right Panel - Statistics
        self.create_statistics_panel(main_container)
        
        # Bottom Panel - History
        self.create_history_panel(main_container)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def create_control_panel(self, parent):
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Address Input
        ttk.Label(control_frame, text="Virtual Address (Decimal):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.address_entry = ttk.Entry(control_frame, width=20)
        self.address_entry.grid(row=0, column=1, pady=5)
        
        ttk.Button(control_frame, text="Translate", command=self.translate_single).grid(row=0, column=2, padx=5)
        
        # Or Hex
        ttk.Label(control_frame, text="Virtual Address (Hex):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.hex_entry = ttk.Entry(control_frame, width=20)
        self.hex_entry.grid(row=1, column=1, pady=5)
        
        ttk.Button(control_frame, text="Translate", command=self.translate_single_hex).grid(row=1, column=2, padx=5)
        
        # Random Generation
        ttk.Label(control_frame, text="Generate Random:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.random_count = ttk.Entry(control_frame, width=20)
        self.random_count.insert(0, "10")
        self.random_count.grid(row=2, column=1, pady=5)
        
        ttk.Button(control_frame, text="Generate & Run", command=self.generate_random).grid(row=2, column=2, padx=5)
        
        # File Input
        ttk.Button(control_frame, text="Load Address File", command=self.load_file).grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # TLB Policy
        ttk.Label(control_frame, text="TLB Replacement:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.policy_var = tk.StringVar(value="FIFO")
        policy_combo = ttk.Combobox(control_frame, textvariable=self.policy_var, values=["FIFO", "LRU"], state="readonly", width=18)
        policy_combo.grid(row=4, column=1, pady=5)
        policy_combo.bind("<<ComboboxSelected>>", self.change_policy)
        
        # Reset Button
        ttk.Button(control_frame, text="Reset All", command=self.reset_all).grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Step-by-step mode
        self.step_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Step-by-Step Mode", variable=self.step_mode).grid(row=6, column=0, columnspan=3, pady=5)
        
    def create_visualization_panel(self, parent):
        viz_frame = ttk.LabelFrame(parent, text="Memory Visualization", padding="10")
        viz_frame.grid(row=2, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # TLB Display
        ttk.Label(viz_frame, text="Translation Lookaside Buffer (TLB)", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        tlb_container = ttk.Frame(viz_frame)
        tlb_container.grid(row=1, column=0, pady=5)
        
        self.tlb_text = scrolledtext.ScrolledText(tlb_container, width=50, height=10, bg='#2d2d2d', fg='#ffffff', font=('Courier', 9))
        self.tlb_text.pack()
        
        # Page Table Display (showing recent entries)
        ttk.Label(viz_frame, text="Page Table (Recent Entries)", font=('Arial', 12, 'bold')).grid(row=2, column=0, pady=5)
        
        pt_container = ttk.Frame(viz_frame)
        pt_container.grid(row=3, column=0, pady=5)
        
        self.pt_text = scrolledtext.ScrolledText(pt_container, width=50, height=10, bg='#2d2d2d', fg='#ffffff', font=('Courier', 9))
        self.pt_text.pack()
        
        # Current Translation Display
        ttk.Label(viz_frame, text="Current Translation", font=('Arial', 12, 'bold')).grid(row=4, column=0, pady=5)
        
        self.translation_text = scrolledtext.ScrolledText(viz_frame, width=50, height=8, bg='#2d2d2d', fg='#00ff00', font=('Courier', 10, 'bold'))
        self.translation_text.grid(row=5, column=0, pady=5)
        
        self.update_visualization()
        
    def create_statistics_panel(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=2, column=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.stats_labels = {}
        
        stats = [
            ("Total Accesses:", "total"),
            ("TLB Hits:", "tlb_hits"),
            ("TLB Misses:", "tlb_misses"),
            ("TLB Hit Rate:", "hit_rate"),
            ("Page Faults:", "page_faults"),
            ("Page Fault Rate:", "pf_rate"),
            ("TLB Size:", "tlb_size"),
            ("Pages in Memory:", "pages_in_mem"),
        ]
        
        for idx, (label, key) in enumerate(stats):
            ttk.Label(stats_frame, text=label, font=('Arial', 10, 'bold')).grid(row=idx, column=0, sticky=tk.W, pady=5)
            value_label = ttk.Label(stats_frame, text="0", font=('Arial', 10), foreground='#4CAF50')
            value_label.grid(row=idx, column=1, sticky=tk.E, pady=5, padx=10)
            self.stats_labels[key] = value_label
            
        # Export button
        ttk.Button(stats_frame, text="Export Statistics", command=self.export_stats).grid(row=len(stats), column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.update_statistics()
        
    def create_history_panel(self, parent):
        history_frame = ttk.LabelFrame(parent, text="Access History", padding="10")
        history_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.history_text = scrolledtext.ScrolledText(history_frame, width=140, height=10, bg='#2d2d2d', fg='#ffffff', font=('Courier', 9))
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        header = f"{'Time':<20} {'Virtual Addr':<15} {'Page':<10} {'Offset':<10} {'Physical Addr':<15} {'Frame':<10} {'TLB':<10} {'Status':<15}\n"
        header += "-" * 140 + "\n"
        self.history_text.insert(tk.END, header)
        
    def translate_address(self, virtual_address):
        """Core translation logic"""
        self.total_accesses += 1
        
        # Extract page number and offset
        page_number = virtual_address >> 12  # Upper 20 bits
        offset = virtual_address & 0xFFF     # Lower 12 bits (4096)
        
        tlb_hit = False
        page_fault = False
        frame_number = None
        
        # Check TLB first
        if page_number in self.tlb:
            frame_number = self.tlb[page_number]
            self.tlb_hits += 1
            tlb_hit = True
            
            # LRU: move to end
            if self.tlb_policy == "LRU":
                self.tlb.move_to_end(page_number)
        else:
            self.tlb_misses += 1
            
            # Check page table
            if page_number in self.page_table:
                frame_number = self.page_table[page_number]
            else:
                # Page fault - allocate new frame
                page_fault = True
                self.page_faults += 1
                
                if self.free_frames:
                    frame_number = self.free_frames.pop(0)
                else:
                    # Simple replacement: use frame 0 (in real system, use page replacement algorithm)
                    frame_number = 0
                
                self.page_table[page_number] = frame_number
                self.physical_memory[frame_number] = page_number
            
            # Update TLB
            if len(self.tlb) >= self.TLB_SIZE:
                self.tlb.popitem(last=False)  # Remove oldest (FIFO) or LRU
            self.tlb[page_number] = frame_number
        
        # Calculate physical address
        physical_address = (frame_number << 12) | offset
        
        # Record history
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        status = "PAGE FAULT" if page_fault else ("TLB HIT" if tlb_hit else "TLB MISS")
        
        history_entry = {
            'time': timestamp,
            'virtual': virtual_address,
            'page': page_number,
            'offset': offset,
            'physical': physical_address,
            'frame': frame_number,
            'tlb': 'HIT' if tlb_hit else 'MISS',
            'status': status
        }
        
        self.access_history.append(history_entry)
        
        # Display in history
        line = f"{timestamp:<20} {virtual_address:<15} {page_number:<10} {offset:<10} {physical_address:<15} {frame_number:<10} {'HIT' if tlb_hit else 'MISS':<10} {status:<15}\n"
        self.history_text.insert(tk.END, line)
        self.history_text.see(tk.END)
        
        # Update displays
        self.display_translation(virtual_address, page_number, offset, physical_address, frame_number, tlb_hit, page_fault)
        self.update_visualization()
        self.update_statistics()
        
        return physical_address
    
    def display_translation(self, virtual, page, offset, physical, frame, tlb_hit, page_fault):
        """Display current translation details"""
        self.translation_text.delete(1.0, tk.END)
        
        output = f"Virtual Address:  {virtual} (0x{virtual:08X})\n"
        output += f"  Page Number:    {page}\n"
        output += f"  Offset:         {offset}\n"
        output += f"\n"
        output += f"TLB:              {'HIT ✓' if tlb_hit else 'MISS ✗'}\n"
        output += f"Page Table:       {'HIT ✓' if not page_fault else 'MISS (Page Fault) ✗'}\n"
        output += f"\n"
        output += f"Frame Number:     {frame}\n"
        output += f"Physical Address: {physical} (0x{physical:08X})\n"
        
        self.translation_text.insert(tk.END, output)
    
    def update_visualization(self):
        """Update TLB and Page Table displays"""
        # TLB
        self.tlb_text.delete(1.0, tk.END)
        self.tlb_text.insert(tk.END, f"TLB Entries ({len(self.tlb)}/{self.TLB_SIZE}) - Policy: {self.tlb_policy}\n")
        self.tlb_text.insert(tk.END, "-" * 40 + "\n")
        self.tlb_text.insert(tk.END, f"{'Page':<15} {'Frame':<15}\n")
        self.tlb_text.insert(tk.END, "-" * 40 + "\n")
        
        for page, frame in self.tlb.items():
            self.tlb_text.insert(tk.END, f"{page:<15} {frame:<15}\n")
        
        # Page Table (show last 20 entries)
        self.pt_text.delete(1.0, tk.END)
        self.pt_text.insert(tk.END, f"Page Table Entries ({len(self.page_table)} total)\n")
        self.pt_text.insert(tk.END, "-" * 40 + "\n")
        self.pt_text.insert(tk.END, f"{'Page':<15} {'Frame':<15}\n")
        self.pt_text.insert(tk.END, "-" * 40 + "\n")
        
        recent_entries = list(self.page_table.items())[-20:]
        for page, frame in recent_entries:
            self.pt_text.insert(tk.END, f"{page:<15} {frame:<15}\n")
    
    def update_statistics(self):
        """Update statistics display"""
        hit_rate = (self.tlb_hits / self.total_accesses * 100) if self.total_accesses > 0 else 0
        pf_rate = (self.page_faults / self.total_accesses * 100) if self.total_accesses > 0 else 0
        
        self.stats_labels['total'].config(text=str(self.total_accesses))
        self.stats_labels['tlb_hits'].config(text=str(self.tlb_hits))
        self.stats_labels['tlb_misses'].config(text=str(self.tlb_misses))
        self.stats_labels['hit_rate'].config(text=f"{hit_rate:.2f}%")
        self.stats_labels['page_faults'].config(text=str(self.page_faults))
        self.stats_labels['pf_rate'].config(text=f"{pf_rate:.2f}%")
        self.stats_labels['tlb_size'].config(text=f"{len(self.tlb)}/{self.TLB_SIZE}")
        self.stats_labels['pages_in_mem'].config(text=str(len(self.page_table)))
    
    def translate_single(self):
        """Translate single address from entry"""
        try:
            addr = int(self.address_entry.get())
            if addr < 0 or addr >= self.VIRTUAL_MEMORY_SIZE:
                messagebox.showerror("Error", f"Address must be between 0 and {self.VIRTUAL_MEMORY_SIZE-1}")
                return
            self.translate_address(addr)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid decimal number")
    
    def translate_single_hex(self):
        """Translate single hex address"""
        try:
            addr = int(self.hex_entry.get(), 16)
            if addr < 0 or addr >= self.VIRTUAL_MEMORY_SIZE:
                messagebox.showerror("Error", f"Address must be between 0 and 0x{self.VIRTUAL_MEMORY_SIZE-1:X}")
                return
            self.translate_address(addr)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid hexadecimal number (e.g., 1A2B3C)")
    
    def generate_random(self):
        """Generate and translate random addresses"""
        try:
            count = int(self.random_count.get())
            if count <= 0 or count > 10000:
                messagebox.showerror("Error", "Count must be between 1 and 10000")
                return
            
            for _ in range(count):
                addr = random.randint(0, self.VIRTUAL_MEMORY_SIZE - 1)
                self.translate_address(addr)
                if self.step_mode.get():
                    self.root.update()
                    self.root.after(100)
                    
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def load_file(self):
        """Load addresses from file"""
        filename = filedialog.askopenfilename(title="Select Address File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            try:
                                addr = int(line)
                                self.translate_address(addr)
                                if self.step_mode.get():
                                    self.root.update()
                                    self.root.after(100)
                            except ValueError:
                                continue
                messagebox.showinfo("Success", f"File loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def change_policy(self, event):
        """Change TLB replacement policy"""
        self.tlb_policy = self.policy_var.get()
        self.update_visualization()
    
    def reset_all(self):
        """Reset all data structures and statistics"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all data?"):
            self.page_table.clear()
            self.tlb.clear()
            self.physical_memory = [None] * self.NUM_FRAMES
            self.free_frames = list(range(self.NUM_FRAMES))
            
            self.total_accesses = 0
            self.tlb_hits = 0
            self.tlb_misses = 0
            self.page_faults = 0
            self.access_history.clear()
            
            self.history_text.delete(1.0, tk.END)
            header = f"{'Time':<20} {'Virtual Addr':<15} {'Page':<10} {'Offset':<10} {'Physical Addr':<15} {'Frame':<10} {'TLB':<10} {'Status':<15}\n"
            header += "-" * 140 + "\n"
            self.history_text.insert(tk.END, header)
            
            self.translation_text.delete(1.0, tk.END)
            
            self.update_visualization()
            self.update_statistics()
    
    def export_stats(self):
        """Export statistics to file"""
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("MemFlow - Virtual Memory Manager Statistics\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Total Memory Accesses: {self.total_accesses}\n")
                    f.write(f"TLB Hits: {self.tlb_hits}\n")
                    f.write(f"TLB Misses: {self.tlb_misses}\n")
                    hit_rate = (self.tlb_hits / self.total_accesses * 100) if self.total_accesses > 0 else 0
                    f.write(f"TLB Hit Rate: {hit_rate:.2f}%\n")
                    f.write(f"Page Faults: {self.page_faults}\n")
                    pf_rate = (self.page_faults / self.total_accesses * 100) if self.total_accesses > 0 else 0
                    f.write(f"Page Fault Rate: {pf_rate:.2f}%\n")
                    f.write(f"TLB Size: {len(self.tlb)}/{self.TLB_SIZE}\n")
                    f.write(f"Pages in Memory: {len(self.page_table)}\n")
                    f.write(f"TLB Replacement Policy: {self.tlb_policy}\n\n")
                    
                    f.write("Access History:\n")
                    f.write("-" * 100 + "\n")
                    for entry in self.access_history:
                        f.write(f"{entry['time']} | Virtual: {entry['virtual']} | Page: {entry['page']} | Frame: {entry['frame']} | {entry['status']}\n")
                
                messagebox.showinfo("Success", "Statistics exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

def main():
    root = tk.Tk()
    app = MemFlow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

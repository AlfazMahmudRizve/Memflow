# MemFlow - Virtual Memory Manager with TLB Simulation

![MemFlow Logo](https://img.shields.io/badge/MemFlow-v1.0-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**MemFlow** is an interactive virtual memory management simulator that demonstrates address translation, TLB (Translation Lookaside Buffer) operations, and page fault handling with real-time visualization.

---

## 🌟 Features

- ✅ **Virtual to Physical Address Translation**
- ✅ **TLB Simulation with Hit/Miss Tracking**
- ✅ **Page Table Management**
- ✅ **Page Fault Handling**
- ✅ **Multiple TLB Replacement Policies** (FIFO, LRU)
- ✅ **Real-time Statistics Display**
- ✅ **Step-by-Step Execution Mode**
- ✅ **Visual Memory State Display**
- ✅ **Export Statistics and History**
- ✅ **Load Address Files**
- ✅ **Random Address Generation**

---

## 📋 System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Dependencies:** tkinter (usually comes with Python)

---

## 🚀 Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/memflow.git
cd memflow
```

### 2. Verify Python Installation

```bash
python --version
# or
python3 --version
```

Should show Python 3.8 or higher.

### 3. Install Dependencies (if needed)

Tkinter usually comes with Python. If not installed:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Tkinter is included with Python installer.

---

## 🎮 How to Run

### Method 1: Run Directly
```bash
python memflow.py
```

### Method 2: Make Executable (Linux/Mac)
```bash
chmod +x memflow.py
./memflow.py
```

---

## 📖 User Guide

### Memory Configuration
- **Virtual Memory:** 4GB (2^32 bytes)
- **Physical Memory:** 16MB (2^24 bytes)
- **Page Size:** 4KB (4096 bytes)
- **TLB Size:** 16 entries
- **Number of Pages:** 1,048,576
- **Number of Frames:** 4,096

### Input Methods

#### 1. Manual Address Input
- **Decimal Input:** Enter address in decimal (e.g., `16916`)
- **Hexadecimal Input:** Enter address in hex (e.g., `4214`)

#### 2. Random Address Generation
- Specify count (1-10,000)
- Click "Generate & Run"
- Optionally enable "Step-by-Step Mode" for visualization

#### 3. Load from File
- Create a text file with one address per line
- Click "Load Address File"
- Addresses can be decimal numbers
- Lines starting with `#` are treated as comments

**Example `addresses.txt`:**
```
# Sample address file for MemFlow
16916
62493
30198
53683
16916
```

### TLB Replacement Policies

#### FIFO (First-In-First-Out)
- Removes the oldest entry when TLB is full
- Simple and predictable
- Good for sequential access patterns

#### LRU (Least Recently Used)
- Removes the least recently accessed entry
- Better performance for locality of reference
- Slightly more complex

---

## 📊 Understanding the Output

### Translation Display

```
Virtual Address:  16916 (0x00004214)
  Page Number:    4
  Offset:         820

TLB:              HIT ✓
Page Table:       HIT ✓

Frame Number:     5
Physical Address: 21300 (0x00005334)
```

**Breakdown:**
1. **Virtual Address:** The input address
2. **Page Number:** Upper 20 bits (virtual_address >> 12)
3. **Offset:** Lower 12 bits (virtual_address & 0xFFF)
4. **TLB Status:** Whether address was found in TLB
5. **Page Table Status:** Whether page was in memory (or page fault)
6. **Frame Number:** Physical frame where page is loaded
7. **Physical Address:** (frame_number << 12) | offset

### Statistics

- **Total Accesses:** Number of address translations performed
- **TLB Hits:** Translations found in TLB cache
- **TLB Misses:** Translations not in TLB (had to check page table)
- **TLB Hit Rate:** (TLB Hits / Total Accesses) × 100%
- **Page Faults:** Pages not in physical memory (had to be loaded)
- **Page Fault Rate:** (Page Faults / Total Accesses) × 100%

**Good Performance:**
- TLB Hit Rate: > 80%
- Page Fault Rate: < 5%

---

## 🧪 Sample Test Cases

### Test Case 1: Sequential Access
```
0
4096
8192
12288
16384
```
**Expected:** High page fault rate initially, then low TLB miss rate

### Test Case 2: Repeated Access
```
16916
16916
16916
16916
```
**Expected:** First access = TLB miss, rest = TLB hits

### Test Case 3: Same Page, Different Offsets
```
4000
4100
4200
4300
```
**Expected:** First access = TLB miss, rest = TLB hits (same page)

### Test Case 4: Random Access
Generate 1000 random addresses
**Expected:** Variable TLB hit rate depending on locality

---

## 🎯 Project Structure

```
memflow/
│
├── memflow.py              # Main application file
├── README.md               # This file
├── addresses.txt           # Sample address file
├── test_addresses.txt      # Test cases
├── documentation.pdf       # Project documentation
└── screenshots/            # Application screenshots
    ├── main_interface.png
    ├── translation.png
    └── statistics.png
```

---

## 🔧 Configuration Options

You can modify memory parameters in `memflow.py`:

```python
self.PAGE_SIZE = 4096              # Change page size
self.PHYSICAL_MEMORY_SIZE = 2**24  # Change physical memory size
self.TLB_SIZE = 16                 # Change TLB size
```

---

## 📝 Exporting Data

### Export Statistics
1. Click "Export Statistics" button
2. Choose save location
3. File includes:
   - All statistics
   - Complete access history
   - TLB configuration

### Export Format
```
MemFlow - Virtual Memory Manager Statistics
==================================================

Total Memory Accesses: 100
TLB Hits: 75
TLB Misses: 25
TLB Hit Rate: 75.00%
Page Faults: 30
Page Fault Rate: 30.00%
...
```

---

## 🐛 Troubleshooting

### Issue: "tkinter not found"
**Solution:** Install python3-tk package (see Installation section)

### Issue: Address out of range
**Solution:** Ensure addresses are between 0 and 4,294,967,295 (2^32 - 1)

### Issue: File won't load
**Solution:** Check file format - one address per line, decimal numbers

### Issue: Application freezes
**Solution:** Disable "Step-by-Step Mode" for large address files

---

## 🎓 Educational Use

This project demonstrates:

1. **Address Translation:** Virtual to physical address mapping
2. **Memory Hierarchy:** TLB → Page Table → Physical Memory
3. **Caching:** TLB as a cache for page table entries
4. **Page Faults:** Handling missing pages
5. **Replacement Policies:** FIFO vs LRU comparison
6. **Performance Metrics:** Hit rates, miss rates, access times

---

## 👥 Team Distribution Guide

### Person 1: Core Translation Logic
- Implement `translate_address()` function
- Page table and TLB data structures
- Address parsing (page number + offset extraction)

### Person 2: TLB Management
- Implement FIFO replacement policy
- Implement LRU replacement policy
- TLB update and lookup functions

### Person 3: GUI Development
- Tkinter interface design
- Visualization panels (TLB, Page Table, Statistics)
- Event handlers for buttons

### Person 4: Testing & Documentation
- Create test cases
- Write documentation
- Prepare presentation slides
- Export functionality

---

## 📚 References

- **Operating System Concepts** by Silberschatz, Galvin, and Gagne
- **Modern Operating Systems** by Andrew S. Tanenbaum
- [Virtual Memory - Wikipedia](https://en.wikipedia.org/wiki/Virtual_memory)
- [Translation Lookaside Buffer - Wikipedia](https://en.wikipedia.org/wiki/Translation_lookaside_buffer)

---

## 📄 License

MIT License - Feel free to use and modify for educational purposes.

---

## 🤝 Contributing

This is an educational project. Suggestions and improvements are welcome!

---

## 📧 Contact

For questions or support, contact: [your-email@example.com]

---

## 🎉 Acknowledgments

- Inspired by classic OS textbook examples
- Built for Operating Systems course project
- Developed using Python and Tkinter

---

**Enjoy learning about virtual memory management with MemFlow!** 🚀

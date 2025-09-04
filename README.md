# TC Kimlik No Validator

A Python GUI application for validating Turkish TC Kimlik numbers (Turkish Identity Numbers) using the official validation algorithm.

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **Single TC Number Validation**: Real-time validation with visual feedback
- **Bulk Text Analysis**: Analyze large texts and files for TC numbers
- **Detailed Results**: Comprehensive analysis with statistics
- **File Operations**: Load from and save results to files
- **User-friendly GUI**: Clean, intuitive interface with Tkinter
- **Real-time Feedback**: Instant validation as you type

## Screenshots

### Main Interface
```
┌─────────────────────────────────────────┐
│           TC Kimlik No Validator        │
├─────────────────────────────────────────┤
│ Single TC Number Validation             │
│ TC Number: [___________] [Validate]     │
│ ✅ Valid TC Number                      │
├─────────────────────────────────────────┤
│ Bulk Text Analysis                      │
│ ┌─────────────────────────────────────┐ │
│ │ Enter your text here...             │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│ [Load File] [Clear] [Analyze] [Save]    │
├─────────────────────────────────────────┤
│ Analysis Results                        │
│ ┌─────────────────────────────────────┐ │
│ │ Results will appear here...         │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.6 or higher
- tkinter (usually comes with Python)

### Clone the Repository

```bash
git clone https://github.com/yourusername/tc-kimlik-validator.git
cd tc-kimlik-validator
```

### Run the Application

```bash
python tc_validator_gui.py
```

## Usage

### Single TC Number Validation

1. Enter a TC Kimlik number in the "Single TC Number Validation" section
2. The application will validate in real-time as you type
3. Green checkmark (✅) indicates a valid TC number
4. Red X (❌) indicates an invalid TC number

### Bulk Text Analysis

1. **Manual Entry**: Type or paste text containing TC numbers into the text area
2. **File Loading**: Click "Load from File" to import text files (TXT, CSV, etc.)
3. **Analysis**: Click "Analyze Text" to find and validate all TC numbers
4. **Save Results**: Click "Save Results" to export the analysis

### Supported File Formats

- Text files (.txt)
- CSV files (.csv)
- All file types (the application will attempt to read as text)

## TC Kimlik Validation Algorithm

The application uses the official Turkish TC Kimlik validation algorithm:

1. **Length Check**: Must be exactly 11 digits
2. **First Digit**: Cannot be 0
3. **10th Digit Validation**: `((sum of odd positions * 7) - sum of even positions) % 10`
4. **11th Digit Validation**: `(sum of first 10 digits) % 10`

### Example Valid TC Numbers

- 10000000146
- 11111111110
- 12345678901 (if it passes the algorithm)

*Note: These are examples for testing. Real TC numbers should not be shared publicly.*

## Code Structure

```
tc-kimlik-validator/
│
├── tc_validator_gui.py          # Main GUI application
├── README.md                    # This file
├── LICENSE                      # MIT License
└── requirements.txt             # Python dependencies (if any)
```

### Main Classes and Functions

- `TCKimlikValidatorGUI`: Main GUI class
- `validate_tc_kimlik()`: Core validation function
- `find_tc_numbers_in_text()`: Text parsing for TC numbers
- `analyze_text()`: Bulk analysis functionality

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## Testing

### Manual Testing

1. Test with known valid TC numbers
2. Test with invalid formats (wrong length, starting with 0, etc.)
3. Test bulk analysis with various text formats
4. Test file loading with different encodings

### Test Cases

```python
# Valid TC numbers for testing
valid_test_cases = [
    "10000000146",
    "11111111110"
]

# Invalid TC numbers for testing
invalid_test_cases = [
    "01234567890",  # Starts with 0
    "1234567890",   # Too short
    "123456789012", # Too long
    "12345678901"   # Fails checksum
]
```

## Known Issues

- Large files (>50MB) may take time to process
- Some special characters in file encoding might cause issues

## Future Enhancements

- [ ] Batch file processing
- [ ] Export to Excel format
- [ ] Command-line interface version
- [ ] Docker containerization
- [ ] API endpoint version
- [ ] Dark theme support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and validation purposes only. Please ensure you comply with data protection laws and regulations when processing personal identification numbers.

## Author

**Bahadir Sahin**
- GitHub: [@yourusername](https://github.com/masaldede)

## Acknowledgments

- Turkish Republic for the TC Kimlik validation algorithm specification
- Python tkinter community for GUI development resources
- Contributors and testers

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/masaldede/tc-kimlik-validator/issues) page
2. Create a new issue with detailed description
3. Provide error messages and steps to reproduce

---

⭐ **Star this repository** if you find it helpful!

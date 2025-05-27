# PDF Crop Tool

A simple Python tool for cropping PDF files by removing unwanted margins.

## Features

- Automatically detect and remove white margins from PDF pages
- Batch processing of multiple PDF files
- Preserve original PDF content and metadata
- Configurable margin settings
- Cross-platform compatibility

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/PDF_CROP.git
   cd PDF_CROP
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python pdf_crop.py
   ```
2. In the application window:
   - Click "Открыть PDF" (Open PDF) to select the PDF file you want to crop.
   - After selecting the file, click "Начать обработку" (Start Processing) to choose the output location and start the cropping process.
   - A message box will inform you once the processing is complete or if an error occurred.

## Building an Executable (Optional)

To create a standalone executable using PyInstaller:

1. Make sure PyInstaller is installed:
   ```bash
   pip install pyinstaller
   ```
2. Run PyInstaller from the project root directory:
   ```bash
   pyinstaller --onefile --windowed pdf_crop.py
   ```
   The executable will be found in the `dist` folder.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. (Note: A LICENSE file is not included in this project, but it's good practice to mention it.)
```

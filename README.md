# OCR-Kaset-Academic-Intellectual-Classification

OCR-Kaset-Academic-Intellectual-Classification is a project developed for the Office of Academic Services and Intellectual Property at Kasetsart University. The purpose of this project is to create a document classification program using Optical Character Recognition (OCR) to extract text from scanned images.

## Project Description

The main goal of the project is to automate the process of extracting text from scanned images and classifying them based on their content. This program can be used to handle permission requests or any other documents related to academic and intellectual property matters.

The program is implemented using the Python programming language and relies on several external libraries and tools, including:

- **Tesseract OCR engine**: An open-source OCR engine that is capable of recognizing text within images.

## Usage

To use this program, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have the required dependencies installed and using vitualenv, including Python and Tesseract OCR. You can download the necessary dependencies from the following link: [pytesseract and poppler installation](https://drive.google.com/file/d/1CeqV1tqzxLldxl8GSy41X3QpYCNA3JvR/view?usp=drive_link).
3. Place the scanned image files that you want to process in the appropriate directory. You can specify the directory in the setup.txt file.
4. Run the program by executing the run.bat file.
5. The program will introduce a 3-second delay before processing and classifying the documents based on the information provided in the agency.txt file. The files will also be renamed according to the classification.

Please ensure that you have correctly set up the required dependencies and provided the necessary input files before running the program.

Please note that the sample work cannot be provided in this repository due to its confidential nature. The files containing sensitive information or credentials are excluded from the repository.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as permitted by the license.

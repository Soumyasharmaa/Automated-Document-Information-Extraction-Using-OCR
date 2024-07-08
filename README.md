


# Automated Document Information Extraction Using OCR
[Main ipynb Notebook ](https://soumyasharmaa.github.io/Automated-Document-Information-Extraction-Using-OCR/) <br>
[Deployed Web app](https://automated-document-information-extraction-using-ocr-d2ekdqxufz.streamlit.app/)

This project involves developing a web application to extract information from user-defined document regions using Optical Character Recognition (OCR). The application leverages Streamlit for the web interface, EasyOCR for text extraction, and OpenCV for image processing tasks.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technology Stack](#technology-stack)
- [Results](#results)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

Document information extraction is a crucial task in many fields, including finance, healthcare, and legal sectors. This project aims to simplify and automate the extraction process using state-of-the-art OCR techniques. The developed web application allows users to upload documents, select regions of interest, and extract textual information from those regions.

## Features

- **User-friendly Interface**: A web application built with Streamlit for easy interaction.
- **Accurate OCR**: Utilizes EasyOCR to accurately extract text from various document types.
- **Flexible Region Selection**: Allows users to define specific regions in the document for text extraction.
- **Structured Output**: Extracted information is converted into a structured CSV format.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Soumyasharmaa/Automated-Document-Information-Extraction-Using-OCR.git
    cd Automated-Document-Information-Extraction-Using-OCR
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Select regions**: Define the regions of interest in the document from which you want to extract text.(Run the Region of interest generator script in you local machine and update the cordinates in the main Web_app.py file

2. **Run the Streamlit application**:
    [Deployed Web app](https://automated-document-information-extraction-using-ocr-d2ekdqxufz.streamlit.app/)

3. **Upload a document**: Use the web interface to upload the document you wish to process.

4. **Extract and download**: Extract the text and download it in a structured CSV format.

## Technology Stack

- **Streamlit**: For building the web application interface.
- **EasyOCR**: For performing Optical Character Recognition.
- **OpenCV**: For image processing and manipulation.

## Results

The application efficiently extracts text from user-defined regions of the document and converts it into a structured CSV format, facilitating easy data manipulation and analysis.




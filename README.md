### README (README.md)


# XXE Injection Automation

This repository contains a Python tool that automates XXE (XML External Entity) payload injection into various file formats, such as `.docx`, `.xlsx`, `.xml`, and more. This utility helps with penetration testing and security analysis by injecting custom XXE payloads into files.

## Features

- Supports multiple file types: `.docx`, `.xlsx`, `.xml`, `.epub`, `.svg`, and more.
- Automatically unpacks the file, injects the payload, and repacks it.
- Simple and easy-to-use command-line interface.

## Supported File Types

The following file formats are supported for XXE injection:

- Microsoft Office formats (`.docx`, `.xlsx`, `.docm`)
- OpenDocument formats (`.odt`, `.ods`, `.odp`)
- Ebook formats (`.epub`)
- Web formats (`.svg`, `.xml`, `.rss`, `.xhtml`)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Elizarfish/xxe_injection.git
```

2. Navigate into the project directory:

```bash
cd xxe_injection
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To inject an XXE payload into a file, use the following command:

```bash
python main.py -i <input_file> -o <output_file> -p "<xxe_payload>"
```

### Arguments:

- `-i`, `--input`: Path to the input file.
- `-o`, `--output`: Path to the output file.
- `-p`, `--payload`: The XXE payload to inject.

### Example:

```bash
python main.py -i example.docx -o output.docx -p "<?xml version='1.0'?><!DOCTYPE doc [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>"
```

## Disclaimer

This tool is intended for educational and legal security testing purposes only. Do not use it on files or systems without permission. The creator is not responsible for any misuse of this tool.

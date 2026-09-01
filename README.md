# HR Document Organizer

A Python CLI tool that organizes HR documents into folders based on document type.

## Problem

HR teams often receive many documents in one folder:

- CVs
- Contracts
- Payroll files
- Leave requests
- Certificates
- Policies
- IDs and passports

Manually sorting these files takes time and can lead to mistakes.

## Solution

This tool automatically classifies HR documents into folders such as:

- CVs
- Contracts
- Payroll
- Leaves
- Certificates
- Policies
- IDs
- Documents
- Images
- Spreadsheets
- Archives
- Other

The tool first checks keywords in the file name.  
If no HR keyword is found, it classifies the file by extension.

## Features

- HR-aware document classification
- Safe dry-run mode by default
- Moves files only when `--execute` is used
- Prevents overwriting files with the same name
- Creates operation logs

## Project Structure

```text
hr-document-organizer/
├── create_sample_files.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Usage

Create sample HR files:

```bash
python create_sample_files.py
```

Preview what will happen without moving files:

```bash
python main.py test_folder
```

Actually move files:

```bash
python main.py test_folder --execute
```

## Example

Input files:

```text
ahmed_cv.pdf
employee_contract.pdf
monthly_payroll.xlsx
leave_request.pdf
training_certificate.pdf
company_policy.pdf
passport_copy.jpg
national_id.png
```

Output folders:

```text
CVs/
Contracts/
Payroll/
Leaves/
Certificates/
Policies/
IDs/
```

## Notes

This project uses sample HR files only.  
Do not use real employee personal data unless you have proper authorization.
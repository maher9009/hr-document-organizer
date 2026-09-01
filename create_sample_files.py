from pathlib import Path


def create_sample_files():
    folder = Path("test_folder")
    folder.mkdir(exist_ok=True)

    sample_files = [
        "ahmed_cv.pdf",
        "sara_resume.docx",
        "employee_contract.pdf",
        "monthly_payroll.xlsx",
        "leave_request.pdf",
        "training_certificate.pdf",
        "company_policy.pdf",
        "passport_copy.jpg",
        "national_id.png",
        "unknown_file.xyz",
    ]

    for file_name in sample_files:
        file_path = folder / file_name
        file_path.write_text(
            f"Sample HR file: {file_name}",
            encoding="utf-8",
        )

    print("Sample HR files created inside test_folder.")


if __name__ == "__main__":
    create_sample_files()
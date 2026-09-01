from pathlib import Path
import argparse
import shutil
import logging


# التصنيف حسب كلمات موجودة في اسم الملف
HR_KEYWORD_MAP = {
    "CVs": [
        "cv",
        "resume",
        "سيرة",
    ],
    "Contracts": [
        "contract",
        "عقد",
    ],
    "Payroll": [
        "payroll",
        "salary",
        "راتب",
        "رواتب",
    ],
    "Leaves": [
        "leave",
        "vacation",
        "إجازة",
        "اجازة",
    ],
    "Certificates": [
        "certificate",
        "training",
        "شهادة",
        "دورة",
    ],
    "Policies": [
        "policy",
        "policies",
        "سياسة",
        "سياسات",
    ],
    "IDs": [
        "passport",
        "national_id",
        "national-id",
        "nationalid",
        "هوية",
        "جواز",
    ],
}


# التصنيف حسب نوع الملف إذا لم نجد كلمة واضحة في الاسم
FILE_EXTENSION_MAP = {
    "Images": {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",
    },
    "Documents": {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".rtf",
        ".odt",
    },
    "Spreadsheets": {
        ".xlsx",
        ".xls",
        ".csv",
        ".ods",
    },
    "Archives": {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
    },
}


def setup_logging(log_file: Path):
    """
    إعداد logging حتى نرى العمليات في الشاشة
    ونحتفظ بها أيضًا داخل ملف سجل.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def get_hr_category(file_path: Path) -> str:
    """
    يحدد تصنيف الملف.

    الأولوية:
    1. البحث عن كلمة تدل على نوع مستند HR في اسم الملف.
    2. إذا لم توجد كلمة واضحة، نصنف حسب امتداد الملف.
    """
    file_name = file_path.stem.lower()

    # أولاً: التصنيف حسب كلمات اسم الملف
    for category, keywords in HR_KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword.lower() in file_name:
                return category

    # ثانيًا: التصنيف حسب الامتداد
    file_extension = file_path.suffix.lower()

    for category, extensions in FILE_EXTENSION_MAP.items():
        if file_extension in extensions:
            return category

    return "Other"


def get_unique_path(target_path: Path) -> Path:
    """
    إذا كان يوجد ملف بنفس الاسم في المجلد الهدف،
    نضيف رقمًا حتى لا نستبدل الملف الموجود.
    """
    if not target_path.exists():
        return target_path

    parent = target_path.parent
    stem = target_path.stem
    suffix = target_path.suffix
    counter = 1

    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def organize_folder(source_folder: Path, execute: bool):
    """
    ينظم الملفات داخل المجلد.

    إذا كانت execute = False:
        البرنامج يعرض فقط ماذا سيفعل.

    إذا كانت execute = True:
        البرنامج ينقل الملفات فعليًا.
    """
    if not source_folder.exists():
        raise FileNotFoundError(f"Folder not found: {source_folder}")

    if not source_folder.is_dir():
        raise NotADirectoryError(f"This is not a folder: {source_folder}")

    try:
        current_script = Path(__file__).resolve()
    except NameError:
        current_script = None

    processed_files = 0

    for item in source_folder.iterdir():
        # نتعامل مع الملفات فقط، وليس المجلدات
        if not item.is_file():
            continue

        # نتجاهل الملفات المخفية التي تبدأ بنقطة
        if item.name.startswith("."):
            continue

        # نتجاهل ملف البرنامج نفسه إذا كان داخل نفس المجلد
        if current_script and item.resolve() == current_script:
            continue

        category = get_hr_category(item)
        target_folder = source_folder / category
        target_path = get_unique_path(target_folder / item.name)

        if execute:
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(target_path))
            logging.info(
                "Moved: %s -> %s/%s",
                item.name,
                category,
                target_path.name,
            )
        else:
            logging.info(
                "[DRY RUN] Would move: %s -> %s/%s",
                item.name,
                category,
                target_path.name,
            )

        processed_files += 1

    logging.info("Total files processed: %s", processed_files)

    if not execute:
        logging.info("Dry run only. No files were moved.")
        logging.info("To actually move files, add: --execute")


def main():
    parser = argparse.ArgumentParser(
        description="Organize HR documents into folders by document type."
    )

    parser.add_argument(
        "source",
        help="The folder you want to organize. Example: test_folder",
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually move files. Without this flag, the program only shows what it would do.",
    )

    args = parser.parse_args()

    source_folder = Path(args.source).expanduser().resolve()

    # ملف سجل مخفي حتى لا يزعج ملفات المشروع
    log_file = Path(".hr_document_organizer.log")

    setup_logging(log_file)

    try:
        organize_folder(source_folder, args.execute)
    except Exception as error:
        logging.error("Error: %s", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
import os
import hashlib
import datetime
import logging

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(filename='tool.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_details(folder):
    """Return a dictionary with file names as keys and their full paths as values."""
    if not os.path.isdir(folder):
        logging.error(f"The folder '{folder}' does not exist or is not a directory.")
        raise FileNotFoundError(f"The folder '{folder}' does not exist or is not a directory.")
    
    file_paths = {}
    for root, _, files in os.walk(folder):
        for file in files:
            file_paths[file] = os.path.join(root, file)
    return file_paths

def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of the given file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_sha256.update(chunk)
    except Exception as e:
        logging.error(f"Error calculating hash for {file_path}: {e}")
        return None
    return hash_sha256.hexdigest()

def generate_report(original_folder, backup_folder):
    files_in_original = get_file_details(original_folder)
    files_in_backup = get_file_details(backup_folder)

    files_present_and_similar_in_both = []
    files_present_in_both_but_different = []
    files_only_in_original = []
    files_only_in_backup = []

    original_files_set = set(files_in_original.keys())
    backup_files_set = set(files_in_backup.keys())

    # Compare files that are present in both folders
    common_files = original_files_set.intersection(backup_files_set)
    for file_name in common_files:
        src_file_path = files_in_original[file_name]
        backup_file_path = files_in_backup[file_name]
        
        if os.path.getsize(src_file_path) == os.path.getsize(backup_file_path):
            # Sizes match, compare hashes
            src_file_hash = calculate_file_hash(src_file_path)
            backup_file_hash = calculate_file_hash(backup_file_path)
            
            if src_file_hash and backup_file_hash:
                if src_file_hash == backup_file_hash:
                    files_present_and_similar_in_both.append(file_name)
                else:
                    files_present_in_both_but_different.append(file_name)
            else:
                files_present_in_both_but_different.append(file_name)
        else:
            files_present_in_both_but_different.append(file_name)

    # Files only in original or backup
    files_only_in_original = list(original_files_set - backup_files_set)
    files_only_in_backup = list(backup_files_set - original_files_set)

    # Determine backup performance
    performance_status = '1' if (len(files_only_in_backup) == 0 and len(files_present_in_both_but_different) == 0 and len(files_only_in_original) == 0) else '0'
    
    # Generate report
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file_name = f"backup_reports/{timestamp}_report.txt"
    os.makedirs(os.path.dirname(report_file_name), exist_ok=True)
    
    with open(report_file_name, 'w') as f:
        # Write the performance status and counts
        report_summary = (
            f"{performance_status}#{len(files_only_in_original)}#"
            f"{len(files_only_in_backup)}#"
            f"{len(files_present_in_both_but_different)}#"
            f"{len(files_present_and_similar_in_both)}\n"
        )
        f.write(report_summary)

        f.write("Similarity percentage between source and backup:\n\n")

        f.write("Files in source but missing in backup:\n")
        f.write(f"Count: {len(files_only_in_original)}\n")
        if files_only_in_original:
            f.write("Names:\n")
            f.write('\n'.join(files_only_in_original) + '\n')
        else:
            f.write("None\n")

        f.write("\nFiles in backup but missing in source:\n")
        f.write(f"Count: {len(files_only_in_backup)}\n")
        if files_only_in_backup:
            f.write("Names:\n")
            f.write('\n'.join(files_only_in_backup) + '\n')
        else:
            f.write("None\n")

        f.write("\nFiles in both source and backup but different sizes or hashes:\n")
        f.write(f"Count: {len(files_present_in_both_but_different)}\n")
        if files_present_in_both_but_different:
            f.write("Names:\n")
            f.write('\n'.join(files_present_in_both_but_different) + '\n')
        else:
            f.write("None\n")

        f.write("\nFiles in both source and backup and similar:\n")
        f.write(f"Count: {len(files_present_and_similar_in_both)}\n")
        if files_present_and_similar_in_both:
            f.write("Names:\n")
            f.write('\n'.join(files_present_and_similar_in_both) + '\n')
        else:
            f.write("None\n")

def main():
    setup_logging()

    try:
        original_folder = input("Enter the path to the original folder: ").strip()
        backup_folder = input("Enter the path to the backup folder: ").strip()

        if not os.path.exists(original_folder):
            raise FileNotFoundError(f"The folder '{original_folder}' does not exist.")
        if not os.path.exists(backup_folder):
            raise FileNotFoundError(f"The folder '{backup_folder}' does not exist.")

        generate_report(original_folder, backup_folder)
        print("Report generated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
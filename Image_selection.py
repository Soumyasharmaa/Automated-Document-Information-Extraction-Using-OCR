import os
import shutil


def extract_and_rename_images(src_dir, dst_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Iterate through the range 1 to 108
    for x in range(1, 109):
        # Construct the source file name
        src_file_name = f"{x}front_scaled_up.jpg"
        src_file_path = os.path.join(src_dir, src_file_name)

        # Check if the file exists in the source directory
        if os.path.exists(src_file_path):
            # Construct the destination file name
            dst_file_name = f"Test Image {x}.jpg"
            dst_file_path = os.path.join(dst_dir, dst_file_name)

            # Copy the file to the destination directory with the new name
            shutil.copy(src_file_path, dst_file_path)
            print(f"Copied {src_file_name} to {dst_file_name}")
        else:
            print(f"File {src_file_name} not found in {src_dir}")


# Define the source and destination directories
source_directory = "new_generated_aadharcard_images"
destination_directory = "Test aadhar"

# Call the function
extract_and_rename_images(source_directory, destination_directory)

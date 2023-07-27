import collections
import tempfile

from class_file_parser import class_file
import zipfile
import os
import pathlib

EXTRACT_DIR = "./build"


def get_class_name(parsed_class_file):
    class_record_index = parsed_class_file.this_class
    class_record = parsed_class_file.constant_pool[class_record_index]
    name_record_index = class_record.info.name_index
    name_record = parsed_class_file.constant_pool[name_record_index]
    return name_record.info.bytes


def main():
    zf = zipfile.ZipFile('logback-core-1.2.3.jar')

    with tempfile.TemporaryDirectory() as tempdir:
        zf.extractall(tempdir)

        for subdir, dirs, files in os.walk(tempdir):
            for file in files:
                full_path = os.path.join(subdir, file)
                file_extension = pathlib.Path(full_path).suffix

                if file_extension != ".class":
                    continue

                #print(full_path)
                with open(full_path, "rb") as f:
                    buffer = f.read()
                    parsed = class_file.parse(buffer)
                    # print(parsed)
                    print("name", get_class_name(parsed))


if __name__ == '__main__':
    main()

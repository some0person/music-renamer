from sys import argv
from os import path, scandir, rename, name

from tinytag import TinyTag


ALLOWED_EXTENSIONS = ("flac", "wav", "mp3", "m4a", "aiff")


def ext_checker(file_name: str) -> bool:
    ext = file_name.split('.')[-1]
    return ext in ALLOWED_EXTENSIONS


def sanitizer(file_name: str, replace_symbol: str) -> str:
    for symbol in "\\/:*?\"<>|":
        file_name = file_name.replace(symbol, replace_symbol)
    return file_name


def file_name_creator(file_path: str) -> str:
    metadata = TinyTag.get(file_path)
    track_info = {
        "track_number": metadata.track,
        "disc_number": metadata.disc,
        "total_discs": metadata.disc_total,
        "title": metadata.title
    }
    name = ""

    if not track_info["title"]:
        print(f"Title error occurred {file_path}")
        return name

    if track_info["disc_number"] != "None" and track_info["disc_number"] != track_info["total_discs"] and track_info["track_number"] != "None":
        name += f"{track_info["disc_number"]}."

    if track_info["track_number"]:
        name += f"{track_info["track_number"].zfill(2)} "

    name += sanitizer(track_info["title"], '')
    name += f".{file_path.split('.')[-1]}"
    
    return name


def browse_folder(folder_path: str, dir_separator: str) -> None:
    changes_check = False

    for file in scandir(folder_path):
        if path.isdir(file.path):
            browse_folder(file.path, dir_separator)
            continue
        
        if not ext_checker(file.name):
            print(f"{file.name} can not be processed.")
            continue
        
        new_file_name = file_name_creator(file.path)

        if not new_file_name or new_file_name == file.name:
            continue

        if not changes_check:
            print(f"#-#-#-#-# [ {folder_path} ] #-#-#-#-#")
            print(f"Old file name: {file.name}")
            print(f"New file name: {new_file_name}")
            changes_check_answer = input("Correct? [Y]es/[N]o ")
            if changes_check_answer.lower() in ("y", "yes"):
               changes_check = True
            else:
                return

        rename(file.path, folder_path + dir_separator + new_file_name)


def main() -> None:
    if len(argv) != 2:
        print("You need to pass exactly 1 argument: working directory.")
        return
    
    if not path.exists(argv[1]):
        print("Your directory does not exists.")
        return

    working_dir = argv[1]

    if name == "nt":
        dir_separator = "\\"
    else:
        dir_separator = "/"

    browse_folder(working_dir, dir_separator)


if __name__ == "__main__":
    main()
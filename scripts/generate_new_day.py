import os
import shutil
import sys


def main():
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dir_2020 = os.path.join(project_root, "year_2020")
    days = [int(folder.strip("day_")) for folder in os.listdir(dir_2020)]
    new_day = f"day_{max(days)+1:02d}"
    new_project_dir = os.path.join(dir_2020, new_day)

    template_src = os.path.join(project_root, "resources", "template.py")
    template_dst = os.path.join(new_project_dir, f"{new_day}.py")

    os.makedirs(new_project_dir)
    shutil.copy2(template_src, template_dst)
    with open(os.path.join(new_project_dir, "input.txt"), 'w'):
        pass
    print(f"Generated new project: {new_project_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

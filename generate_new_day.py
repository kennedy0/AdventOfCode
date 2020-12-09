import os
import shutil
import sys


def main():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.join(this_dir, "2020")
    days = [int(folder) for folder in os.listdir(root_dir)]
    new_day = f"{max(days)+1:02d}"
    new_project_dir = os.path.join(root_dir, new_day)

    template_src = os.path.join(this_dir, "resources", "template.py")
    template_dst = os.path.join(new_project_dir, f"day_{new_day}.py")

    os.makedirs(new_project_dir)
    shutil.copy2(template_src, template_dst)
    with open(os.path.join(new_project_dir, "input.txt"), 'w'):
        pass
    print(f"Generated new project: {new_project_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

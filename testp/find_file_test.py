import sys
import os

def explorer():
    current_dir = os.getcwd()
    print("What would you like to do?")
    print("0) [Go to previous directory]")
    print("1) [Go to parent directory]")
    print("2) [Go to a specified directory]")
    print(" > List of files at", current_dir)
    files = os.listdir()
    for i, file in enumerate(files):
      print(f"{i + 3}) {file}")
    print("x) [exit]")
    print()

    choice = input("Enter your choice: ")
    print("Your choice is", choice)
    print("================================")
    print()

    if choice.isalnum() == False:
      if choice == "x":
        print("exit")
        sys.exit(0)
    else:
      ichoice = int(choice)
      if int(ichoice) > 2:
        file = files[ichoice]
        print(f"Open file {file}!")
        with open(files[ichoice-3]) as f:
          print(f.read())
      elif int(ichoice) == 0:
        print("Chaning directory to", current_dir)
        os.chdir(current_dir)
        explorer()
      elif int(ichoice) == 1:
        print("Chaning directory to", os.path.abspath(os.path.join(current_dir, os.pardir)))
        os.chdir(os.path.abspath(os.path.join(current_dir, os.pardir)))
        explorer()
      elif int(ichoice) == 2:
        target_dir = input("Enter the path of the directory you want to go to: ")
        print("Chaning directory to", target_dir)
        os.chdir(target_dir)
        explorer()
      else:
        print("Invalid choice.")
        explorer()

explorer()

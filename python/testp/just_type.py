import os

current_dir = os.getcwd()
files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]

print("Select an option:")
print("1) Open a file")

user_input = input()

if user_input == "1":
    print("Available files:")
    for i, f in enumerate(files):
        print(f"{i + 1}) {f}")


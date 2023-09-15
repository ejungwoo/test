with open("list_of_journals","r") as f1:
    lines = f1.read().splitlines()
    lines2 = sorted(lines)
    print("\n".join(lines2))

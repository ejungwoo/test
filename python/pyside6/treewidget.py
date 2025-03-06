import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

#import sys
#from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

data = {"Project A": ["file_a.py", "file_a.txt", "something.xls"],
        "Project B": ["file_b.csv", "photo.jpg"],
        "Project C": []}

app = QApplication()

tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["name","type"])

tree_data = []
for key, values in data.items():
    branch = QTreeWidgetItem([key])
    for value in values:
        ext = value.split(".")[-1].upper()
        child = QTreeWidgetItem([value, ext])
        branch.addChild(child)
    tree_data.append(branch)

tree.insertTopLevelItems(0, tree_data)
tree.show()
sys.exit(app.exec())

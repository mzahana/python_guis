import sys
try:
    # Try importing Qt5 libraries
    from PySide2.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
    print("Qt5 is installed.")
except ImportError:
    try:
        # If Qt5 is not found, try importing Qt6 libraries
        from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
        print("Qt6 is installed.")
    except ImportError:
        # Raise an error if neither Qt5 nor Qt6 libraries are found
        raise ImportError("Neither Qt5 nor Qt6 libraries are found. Please install PySide2 or PySide6.")

# You can continue with your application logic here, using the imported QApplication and QWidget


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple PySide6 App')
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        button = QPushButton('Click Me')
        layout.addWidget(button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())

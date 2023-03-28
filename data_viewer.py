import os
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QSlider

class ImageMaskViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.image_dir = ''
        self.mask_dir = ''
        self.image_paths = []
        self.mask_paths = []
        self.current_index = 0
        self.opacity = 0.3 # initial opacity value

        self.image_label = QLabel()
        self.mask_label = QLabel()
        self.overlay_label = QLabel()

        self.prev_button = QPushButton('Previous')
        self.next_button = QPushButton('Next')
        self.mark_button = QPushButton('Mark')

        self.file_text_edit = QTextEdit()
        self.file_name_label = QLabel()
        self.index_edit = QLineEdit()

        self.index_search_button = QPushButton('Go to index')
        self.index_search_button.clicked.connect(self.go_to_index)

        self.prev_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)
        self.mark_button.clicked.connect(self.mark_image)

        main_layout = QVBoxLayout()
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.mask_label)
        image_layout.addWidget(self.overlay_label)

        main_layout.addWidget(self.file_name_label)
        main_layout.addLayout(image_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.mark_button)
        main_layout.addWidget(self.file_text_edit)
        main_layout.addLayout(button_layout)
        button_layout.addWidget(self.index_edit)
        button_layout.addWidget(self.index_search_button)

        self.index_label = QLabel()
        self.index_label.setAlignment(Qt.AlignCenter) # center align index label
        self.index_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        main_layout.addWidget(self.index_label) # add index label to main layout




        # create slider for opacity control
        opacity_slider = QSlider(Qt.Horizontal)
        opacity_slider.setRange(0, 100)
        opacity_slider.setValue(int(self.opacity * 100))
        opacity_slider.setTickInterval(10)
        opacity_slider.setTickPosition(QSlider.TicksBelow)
        opacity_slider.valueChanged.connect(self.set_opacity)
        main_layout.addWidget(opacity_slider)

        self.setLayout(main_layout)


        self.show()

    def set_opacity(self, value):
        self.opacity = value / 100.0 # update the opacity value
        self.show_current() # update the current image and mask

    def set_index_label(self):
        self.index_label.setText(f"Image {self.current_index + 1}/{len(self.image_paths)}") # set text for index label
        self.show_current() # update the current image and mask

    def show_current(self):
        image_path = self.image_paths[self.current_index]
        mask_path = self.mask_paths[self.current_index] if self.mask_paths else ''
        image = QPixmap(image_path)
        mask = QPixmap(mask_path)

        overlay = QPixmap(image.size())
        painter = QPainter(overlay)

        painter.drawPixmap(0, 0, image)
        painter.setOpacity(self.opacity)
        painter.drawPixmap(0, 0, mask)
        del painter
        
        self.image_label.setPixmap(image)
        self.mask_label.setPixmap(mask)
        self.overlay_label.setPixmap(overlay)
        
        self.file_name_label.setText(os.path.basename(image_path))
        index_label_text = f"Index: {self.current_index + 1}/{len(self.image_paths)}"
        self.index_label.setText(index_label_text)


    def go_to_index(self):
        index_str = self.index_edit.text()
        try:
            index = int(index_str)
            if 0 <= index < len(self.image_paths):
                self.current_index = index
                self.show_current()
        except ValueError:
            pass

    def get_directory(self, title):
        directory = QFileDialog.getExistingDirectory(self, title)
        return directory

    def load_images(self):
        image_exts = ['.png', '.jpg', '.jpeg']
        mask_exts = ['.png', '.jpg', '.jpeg']
        self.image_paths = sorted([os.path.join(self.image_dir, f) for f in os.listdir(self.image_dir) if os.path.splitext(f)[1] in image_exts])
        if self.mask_dir != '':
            self.mask_paths = sorted([os.path.join(self.mask_dir, f) for f in os.listdir(self.mask_dir) if os.path.splitext(f)[1] in mask_exts])
        else:
            self.mask_paths = []
        self.current_index = 0

        self.set_index_label()
        self.show_current()


    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current()

    def show_next(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_current()

    def mark_image(self):
        image_path = self.image_paths[self.current_index]
        self.file_text_edit.append(image_path)

    def choose_image_dir(self):
        image_dir = QFileDialog.getExistingDirectory(self, "Select Image Directory")
        if image_dir:
            self.image_dir = image_dir
            self.choose_mask_dir()

    def choose_mask_dir(self):
        mask_dir = QFileDialog.getExistingDirectory(self, "Select Mask Directory")
        if mask_dir:
            self.mask_dir = mask_dir
            self.load_images()

if __name__ == '__main__':
    app = QApplication([])
    viewer = ImageMaskViewer()
    viewer.choose_image_dir()
    app.exec_()

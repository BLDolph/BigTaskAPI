import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.longitude = -64.825251
        self.lattitude = 18.299605
        self.z = 16
        self.z_min = 0
        self.z_max = 21
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1'
        params = {
            'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
            'll': f'{self.longitude},{self.lattitude}',
            'z': self.z
        }

        # Готовим запрос.
        response = requests.get(server_address, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def updateMap(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.z += 1
            if self.z > self.z_max:
                self.z = self.z_max
            self.getImage()
            self.updateMap()

        if key == Qt.Key.Key_PageDown:
            self.z -= 1
            if self.z < self.z_min:
                self.z = self.z_min
            self.getImage()
            self.updateMap()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        if os.path.exists(self.map_file):
            os.remove(self.map_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
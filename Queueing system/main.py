import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, 
    QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout,
    QLineEdit, QGroupBox,QTableWidgetItem, QTableWidget
)
from tab1_widget import Tab1Widget
from tab2_widget import Tab2Widget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Система массового обслуживания")
        self.setGeometry(100, 100, 900, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout()
        
        # Создаем StackedWidget
        self.stacked_widget = QStackedWidget()
        
        # Создаем вкладки
        self.tab1 = Tab1Widget()
        self.tab2 = Tab2Widget()
        
        # Добавляем вкладки в StackedWidget
        self.stacked_widget.addWidget(self.tab1)
        self.stacked_widget.addWidget(self.tab2)
        
        # Панель переключения вкладок
        tab_switch_layout = QHBoxLayout()
        
        self.tab1_btn = QPushButton("Пошаговое моделирование")
        self.tab2_btn = QPushButton("Автоматическое моделирования")
        
        # Стилизация кнопок
        self.tab1_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.tab2_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        
        # Подключаем переключение вкладок
        self.tab1_btn.clicked.connect(lambda: self.switch_tab(0))
        self.tab2_btn.clicked.connect(lambda: self.switch_tab(1))
        
        tab_switch_layout.addWidget(self.tab1_btn)
        tab_switch_layout.addWidget(self.tab2_btn)
        tab_switch_layout.addStretch()  # Растягиваем пространство
        
        # Добавляем всё в основной layout
        main_layout.addLayout(tab_switch_layout)
        main_layout.addWidget(self.stacked_widget)
        
        central_widget.setLayout(main_layout)
        
        # Подключаем кнопки действий
    #    self.tab1.action_btn.clicked.connect(self.on_tab1_action)
    #    self.tab2.action_btn.clicked.connect(self.on_tab2_action)
        
        # Устанавливаем первую вкладку активной
        self.switch_tab(0)
    
    def switch_tab(self, index):
        """Переключение между вкладками"""
        self.stacked_widget.setCurrentIndex(index)
        
        # Обновляем стили кнопок
        if index == 0:
            self.tab1_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2E7D32;
                    color: white;
                    border: 2px solid #1B5E20;
                    padding: 10px;
                    font-weight: bold;
                }
            """)
            self.tab2_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0b7dda;
                }
            """)
        else:
            self.tab1_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.tab2_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1565C0;
                    color: white;
                    border: 2px solid #0D47A1;
                    padding: 10px;
                    font-weight: bold;
                }
            """)
    

def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
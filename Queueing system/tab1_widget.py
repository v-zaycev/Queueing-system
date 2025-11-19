import sys
from PyQt6.QtWidgets import (QWidget, 
    QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout,
    QLineEdit, QGroupBox, QScrollArea, QStatusBar
)
from status_widget import StatusWidget
from PyQt6.QtCore import Qt
import queueing_system


class Tab1Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.qs_params = None
        self.qs = None
        self.initUI()

    def initUI(self):
        self.status_bar = QStatusBar()
        layout = QVBoxLayout()
        # Группа с формой параметров СМО
        form_group = QGroupBox()
        form_layout = QHBoxLayout()  # Меняем на горизонтальный layout
        
        # Левый столбец
        left_column = QFormLayout()
        self.sources_input = QLineEdit()
        self.handlers_input = QLineEdit()
        self.buffer_size_input = QLineEdit()
        self.modeling_time_input = QLineEdit()
        
        left_column.addRow("Источники:", self.sources_input)
        left_column.addRow("Приборы:", self.handlers_input)
        left_column.addRow("Размер буфера:", self.buffer_size_input)
        left_column.addRow("Время моделирования:", self.modeling_time_input)
        
        # Правый столбец
        right_column = QFormLayout()
        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        self.lambda_input = QLineEdit()
        
        right_column.addRow("a:", self.a_input)
        right_column.addRow("b:", self.b_input)
        right_column.addRow("Интенсивность (λ):", self.lambda_input)
        
        # Добавляем столбцы в форму
        form_layout.addLayout(left_column)
        form_layout.addLayout(right_column)
        
        form_group.setLayout(form_layout)
        left_column.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        right_column.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(form_group)
        
        # Кнопка действия
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Сохранить настройки")
        self.reset_btn = QPushButton("Сбросить настройки")
        self.start_btn = QPushButton("Начать моделирование")
        self.step_btn = QPushButton("Следующий шаг")
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.step_btn)
        
        layout.addLayout(buttons_layout)
        # Создаем layout для блоков
        self.create_blocks_layout()
        layout.addLayout(self.blocks_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Заполняем блоки начальными данными
        self.sources_list = []
        self.buffer_list = []
        self.handlers_list = []
        
        self.save_btn.clicked.connect(self.on_save_settings)
        self.reset_btn.clicked.connect(self.on_reset_settings)
        self.start_btn.clicked.connect(self.on_start_modeling)
        self.step_btn.clicked.connect(self.on_next_step)
        self.on_reset_settings()

    def create_blocks_layout(self):
        """Создает layout для трех блоков"""
        self.blocks_layout = QHBoxLayout()
        
        # Блок источников
        self.sources_group = QGroupBox("Источники")
        self.sources_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sources_layout = QVBoxLayout()
        self.sources_scroll = QScrollArea()
        self.sources_content = QWidget()
        self.sources_list_layout = QVBoxLayout(self.sources_content)
        self.sources_scroll.setWidget(self.sources_content)
        self.sources_scroll.setWidgetResizable(True)
        self.sources_scroll.setMinimumHeight(300)  # Увеличиваем высоту
        sources_layout.addWidget(self.sources_scroll)
        self.sources_group.setLayout(sources_layout)
        
        # Блок буфера
        self.buffer_group = QGroupBox("Буфер")
        self.buffer_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buffer_layout = QVBoxLayout()
        self.buffer_scroll = QScrollArea()
        self.buffer_content = QWidget()
        self.buffer_list_layout = QVBoxLayout(self.buffer_content)
        self.buffer_scroll.setWidget(self.buffer_content)
        self.buffer_scroll.setWidgetResizable(True)
        self.buffer_scroll.setMinimumHeight(300)
        buffer_layout.addWidget(self.buffer_scroll)
        self.buffer_group.setLayout(buffer_layout)
        
        # Блок приборов
        self.handlers_group = QGroupBox("Приборы")
        self.handlers_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        handlers_layout = QVBoxLayout()
        self.handlers_scroll = QScrollArea()
        self.handlers_content = QWidget()
        self.handlers_list_layout = QVBoxLayout(self.handlers_content)
        self.handlers_scroll.setWidget(self.handlers_content)
        self.handlers_scroll.setWidgetResizable(True)
        self.handlers_scroll.setMinimumHeight(300)
        handlers_layout.addWidget(self.handlers_scroll)
        self.handlers_group.setLayout(handlers_layout)
        
        # Добавляем блоки в горизонтальный layout с растягиванием
        self.blocks_layout.addWidget(self.sources_group)
        self.blocks_layout.addWidget(self.buffer_group)
        self.blocks_layout.addWidget(self.handlers_group)
    
    def clear_layout(self, layout):
        """Очищает layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_save_settings(self):
        """Сохранить новые настройки"""
        self.reset_field_colors()
        
        try:
            has_errors = False
            
            # Проверка и преобразование типов
            try:
                sources_nmb = int(self.sources_input.text())
                if sources_nmb <= 0:
                    self.highlight_field("sources")
                    has_errors = True
            except ValueError:
                self.highlight_field("sources")
                has_errors = True
            
            try:
                handlers_nmb = int(self.handlers_input.text())
                if handlers_nmb <= 0:
                    self.highlight_field("handlers")
                    has_errors = True
            except ValueError:
                self.highlight_field("handlers")
                has_errors = True
            
            try:
                buffer_sz = int(self.buffer_size_input.text())
                if buffer_sz < 0:
                    self.highlight_field("buffer")
                    has_errors = True
            except ValueError:
                self.highlight_field("buffer")
                has_errors = True
            
            try:
                a = float(self.a_input.text())
                if a < 0:
                    self.highlight_field("a")
                    has_errors = True
            except ValueError:
                self.highlight_field("a")
                has_errors = True
            
            try:
                b = float(self.b_input.text())
                if b < 0:
                    self.highlight_field("b")
                    has_errors = True
            except ValueError:
                self.highlight_field("b")
                has_errors = True
            
            try:
                lambda_ = float(self.lambda_input.text())
                if lambda_ <= 0:
                    self.highlight_field("lambda")
                    has_errors = True
            except ValueError:
                self.highlight_field("lambda")
                has_errors = True
            
            try:
                modeling_time = float(self.modeling_time_input.text())
                if modeling_time <= 0:
                    self.highlight_field("time")
                    has_errors = True
            except ValueError:
                self.highlight_field("time")
                has_errors = True
            
            # Проверка a < b
            if not has_errors and a >= b:
                self.highlight_field("a")
                self.highlight_field("b")
                has_errors = True
            
            if has_errors:
                self.qs_params = None
                return

            # Создание объекта параметров
            self.qs_params = queueing_system.SystemParams()
            self.qs_params.sources_nmb = sources_nmb
            self.qs_params.handlers_nmb = handlers_nmb
            self.qs_params.buffer_sz = buffer_sz
            self.qs_params.a = a
            self.qs_params.b = b
            self.qs_params.lambda_ = lambda_
            self.qs_params.modelligng_time = modeling_time
            
            self.fill_blocks_from_params()
            self.highlight_success()
            # Разблокировка кнопки
            self.start_btn.setEnabled(True)

            self.sources_input.setEnabled(False)
            self.handlers_input.setEnabled(False)
            self.buffer_size_input.setEnabled(False)
            self.a_input.setEnabled(False)
            self.b_input.setEnabled(False)
            self.lambda_input.setEnabled(False)
            self.modeling_time_input.setEnabled(False)

            self.save_btn.setEnabled(False)


        except Exception:
            self.qs_params = None

    def highlight_field(self, field_name):
        """Подсветить поле с ошибкой"""
        field_map = {
            "sources": self.sources_input,
            "handlers": self.handlers_input,
            "buffer": self.buffer_size_input,
            "a": self.a_input,
            "b": self.b_input,
            "lambda": self.lambda_input,
            "time": self.modeling_time_input
        }
        
        if field_name in field_map:
            field_map[field_name].setStyleSheet("background-color: #ffebee; border: 1px solid #f44336;")

    def reset_field_colors(self):
        """Сбросить цвет всех полей"""
        fields = [
            self.sources_input, self.handlers_input, self.buffer_size_input,
            self.a_input, self.b_input, self.lambda_input, self.modeling_time_input
        ]
        
        for field in fields:
            field.setStyleSheet("background-color: white; border: 1px solid #cccccc;")

    def highlight_success(self):
        """Подсветить все поля зелёным при успехе"""
        fields = [
            self.sources_input, self.handlers_input, self.buffer_size_input,
            self.a_input, self.b_input, self.lambda_input, self.modeling_time_input
        ]
        
        for field in fields:
            field.setStyleSheet("background-color: #e8f5e8; border: 1px solid #4caf50;")

    def on_reset_settings(self):
        """Сбросить настройки"""
        self.sources_input.clear()
        self.handlers_input.clear()
        self.buffer_size_input.clear()
        self.a_input.clear()
        self.b_input.clear()
        self.lambda_input.clear()
        self.modeling_time_input.clear()
        self.reset_field_colors()
        self.start_btn.setEnabled(False)
        self.step_btn.setEnabled(False)
        self.qs_params = None 
        del self.qs
        self.qs = None # Сбрасываем параметры
        self.clear_all_blocks()

        self.sources_input.setEnabled(True)
        self.handlers_input.setEnabled(True)
        self.buffer_size_input.setEnabled(True)
        self.a_input.setEnabled(True)
        self.b_input.setEnabled(True)
        self.lambda_input.setEnabled(True)
        self.modeling_time_input.setEnabled(True)

        self.save_btn.setEnabled(True)

    def on_start_modeling(self):
        self.qs = queueing_system.QueueingSystem(self.qs_params)
        self.qs.init()
        self.start_btn.setEnabled(False)
        self.step_btn.setEnabled(True)
        self.update_blocks_from_state(self.qs.getState())

    def on_next_step(self):
        self.qs.nextEvent()
        self.update_blocks_from_state(self.qs.getState())
    
    def clear_all_blocks(self):
        """Очистить все блоки (источники, буфер, приборы)"""
        self.clear_layout(self.sources_list_layout)
        self.clear_layout(self.buffer_list_layout)
        self.clear_layout(self.handlers_list_layout)
        self.sources_list.clear()
        self.buffer_list.clear()
        self.handlers_list.clear()
    
    def fill_blocks_from_params(self):
        """Заполнить блоки элементами согласно сохранённым параметрам"""
        if self.qs_params is None:
            return
        
        # Заполняем источники
        self.sources_list = [
            StatusWidget("source", i+1) 
            for i in range(self.qs_params.sources_nmb)
        ]
        for source in self.sources_list:
            self.sources_list_layout.addWidget(source)
        
        # Заполняем буфер
        self.buffer_list = [
            StatusWidget("buffer", i+1)
            for i in range(self.qs_params.buffer_sz)
        ]
        for buffer_cell in self.buffer_list:
            self.buffer_list_layout.addWidget(buffer_cell)
        
        # Заполняем приборы
        self.handlers_list = [
            StatusWidget("handler", i+1)
            for i in range(self.qs_params.handlers_nmb)
        ]
        for handler in self.handlers_list:
            self.handlers_list_layout.addWidget(handler)

    def update_blocks_from_state(self, system_state : queueing_system.SystemState):
        """Обновить блоки из состояния системы"""
        # Обновляем источники
        for i, next_event_time in enumerate(system_state.sources):
            if i < len(self.sources_list):
                self.sources_list[i].set_status(time = next_event_time)
        
        # Обновляем буфер
        for i in range(len(self.buffer_list)):
            source_num, creation_time = system_state.buffer[i]
            self.buffer_list[i].set_status(source_num + 1, creation_time)

        # Обновляем приборы
        for i, handler_data in enumerate(system_state.handlers):
            source_num, end_time = handler_data
            self.handlers_list[i].set_status(source_num + 1, end_time)
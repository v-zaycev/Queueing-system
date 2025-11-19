from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout,
    QLineEdit, QGroupBox,QTableWidgetItem, QTableWidget
)
from PyQt6.QtCore import Qt
import queueing_system

class Tab2Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.qs_params = None
        self.qs = None
        self.initUI()
    #   self.fill_tables_with_examples()
    def initUI(self):
        layout = QVBoxLayout()
        
        # Группа с формой параметров СМО
        form_group = QGroupBox("Параметры автоматического моделирования")
        form_layout = QHBoxLayout()
        
        # Левый столбец
        left_column = QFormLayout()
        left_column.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
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
        right_column.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
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
        layout.addWidget(form_group)
        
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Сохранить настройки")
        self.reset_btn = QPushButton("Сбросить настройки")
        self.start_btn = QPushButton("Начать моделирование")
        self.step_btn = QPushButton("Следующий шаг")
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.step_btn)

        invisible_btn_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: transparent;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: transparent;
                border: none;
            }
            QPushButton:pressed {
                background-color: transparent;
                border: none;
            }
        """
        self.step_btn.setStyleSheet(invisible_btn_style)
        self.step_btn.setEnabled(False)  # Блокируем клики

        # Кнопка действия
        layout.addLayout(buttons_layout)
        
        # Таблицы статистики
        stats_layout = QHBoxLayout()
        
        # Таблица статистики источников
        sources_stats_group = QGroupBox("Статистика источников")
        sources_stats_layout = QVBoxLayout()
        
        self.sources_table = QTableWidget()
        self.sources_table.setColumnCount(8)
        self.sources_table.setHorizontalHeaderLabels([
            "Источник", "Дисп. обработки", "Дисп. буфера", 
            "Ср. время буфера", "Ср. время системы", 
            "Ср. время обработки", "Вер. отказа", "Всего заявок"
        ])
        self.sources_table.horizontalHeader().setStretchLastSection(True)
        
        sources_stats_layout.addWidget(self.sources_table)
        sources_stats_group.setLayout(sources_stats_layout)
        
        # Таблица статистики приборов
        handlers_stats_group = QGroupBox("Статистика приборов")
        handlers_stats_layout = QVBoxLayout()
        
        self.handlers_table = QTableWidget()
        self.handlers_table.setColumnCount(2)
        self.handlers_table.setHorizontalHeaderLabels([
            "Прибор", "Коэф. использования"
        ])
        self.handlers_table.horizontalHeader().setStretchLastSection(True)
        
        handlers_stats_layout.addWidget(self.handlers_table)
        handlers_stats_group.setLayout(handlers_stats_layout)
        
        # Добавляем таблицы в layout
        stats_layout.addWidget(sources_stats_group)
        stats_layout.addWidget(handlers_stats_group)
        
        layout.addLayout(stats_layout)
        
        self.setLayout(layout)

        self.save_btn.clicked.connect(self.on_save_settings)
        self.reset_btn.clicked.connect(self.on_reset_settings)
        self.start_btn.clicked.connect(self.on_start_modeling)
        # self.step_btn.clicked.connect(self.on_next_step)
    
    def update_sources_stats(self, stats_data : queueing_system.SystemResult):
        """Обновить статистику источников"""
        self.sources_table.setRowCount(len(stats_data.sources))
        
        for row, stats in enumerate(stats_data.sources):
            self.sources_table.setItem(row, 0, QTableWidgetItem(f"Источник {row+1}"))
            self.sources_table.setItem(row, 1, QTableWidgetItem(f"{stats.dispersion_processing_time:.4f}"))
            self.sources_table.setItem(row, 2, QTableWidgetItem(f"{stats.dispersion_time_in_buffer:.4f}"))
            self.sources_table.setItem(row, 3, QTableWidgetItem(f"{stats.mean_time_in_buffer:.4f}"))
            self.sources_table.setItem(row, 4, QTableWidgetItem(f"{stats.mean_time_in_system:.4f}"))
            self.sources_table.setItem(row, 5, QTableWidgetItem(f"{stats.mean_time_of_processing:.4f}"))
            self.sources_table.setItem(row, 6, QTableWidgetItem(f"{stats.probability_of_refusal:.4f}"))
            self.sources_table.setItem(row, 7, QTableWidgetItem(f"{stats.total_requests}"))
    
    def update_handlers_stats(self, stats_data : queueing_system.SystemResult):
        """Обновить статистику приборов"""
        self.handlers_table.setRowCount(len(stats_data.handlers))
        
        for row, utilization_rate in enumerate(stats_data.handlers):
            self.handlers_table.setItem(row, 0, QTableWidgetItem(f"Прибор {row+1}"))
            self.handlers_table.setItem(row, 1, QTableWidgetItem(f"{utilization_rate:.4f}"))
            
    def fill_tables_with_examples(self):
        """Заполнить таблицы примерами данных"""
        # Примеры для источников
        sources_examples = [
            (0.125, 0.089, 2.345, 5.678, 3.210, 0.023, 150),
            (0.234, 0.156, 1.987, 4.567, 2.543, 0.045, 120),
            (0.178, 0.134, 2.123, 5.432, 3.087, 0.032, 180),
            (0.267, 0.198, 1.765, 4.321, 2.456, 0.067, 90)
        ]
        
        self.sources_table.setRowCount(len(sources_examples))
        for row, (disp_proc, disp_buf, mean_buf, mean_sys, mean_proc, prob_ref, total) in enumerate(sources_examples):
            self.sources_table.setItem(row, 0, QTableWidgetItem(f"Источник {row+1}"))
            self.sources_table.setItem(row, 1, QTableWidgetItem(f"{disp_proc:.3f}"))
            self.sources_table.setItem(row, 2, QTableWidgetItem(f"{disp_buf:.3f}"))
            self.sources_table.setItem(row, 3, QTableWidgetItem(f"{mean_buf:.3f}"))
            self.sources_table.setItem(row, 4, QTableWidgetItem(f"{mean_sys:.3f}"))
            self.sources_table.setItem(row, 5, QTableWidgetItem(f"{mean_proc:.3f}"))
            self.sources_table.setItem(row, 6, QTableWidgetItem(f"{prob_ref:.3f}"))
            self.sources_table.setItem(row, 7, QTableWidgetItem(f"{total}"))
        
        # Примеры для приборов
        handlers_examples = [0.856, 0.723, 0.912, 0.645, 0.789]
        
        self.handlers_table.setRowCount(len(handlers_examples))
        for row, utilization in enumerate(handlers_examples):
            self.handlers_table.setItem(row, 0, QTableWidgetItem(f"Прибор {row+1}"))
            self.handlers_table.setItem(row, 1, QTableWidgetItem(f"{utilization:.3f}"))
        
        # Подгонка размеров столбцов под содержимое
        self.sources_table.resizeColumnsToContents()
        self.handlers_table.resizeColumnsToContents()

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
        self.qs.autoModeling()
        self.update_sources_stats(self.qs.getResult())
        self.update_handlers_stats(self.qs.getResult())

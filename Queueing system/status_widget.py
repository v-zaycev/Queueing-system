from PyQt6.QtWidgets import (
     QLabel,  QSizePolicy
)
from PyQt6.QtCore import Qt

class StatusWidget(QLabel):
    def __init__(self, widget_type="source", num=0, source_num=0, time=-1.0):
        super().__init__()
        if time is None or time < 0.0:
            self.is_free = True
        else:
            self.is_free = False
        
        self.widget_type = widget_type
        self.num = num
        self.source_num = source_num
        self.time = time
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.update_text()
        self.update_style()
        
    def set_status(self, source_num=None, time=None):
        if time is None or time <0.0:
            self.is_free = True
        else:
            self.is_free = False
        if source_num is not None:
            self.source_num = source_num
        if time is not None:
            self.time = time
        self.update_text()
        self.update_style()
            
    def update_text(self):
        if self.widget_type == "source":
            self.setText(f"Источник {self.num}\n{self.time:.5f}")
        elif self.widget_type == "buffer":
            if self.is_free:
                self.setText(f"Ячейка {self.num}\nСвободно")
            else:
                self.setText(f"Ячейка {self.num}\nИсточник {self.source_num} : {self.time:.5f}")
        else:  # handler
            if self.is_free:
                self.setText(f"Прибор {self.num}\nСвободно")
            else:
                self.setText(f"Прибор {self.num}\nИсточник {self.source_num} : {self.time:.5f}")
        
    def update_style(self):
        if self.widget_type == "source":
            # Источники всегда белые
            self.setStyleSheet("""
                StatusWidget {
                    background-color: #ffffff;
                    border: 2px solid #cccccc;
                    border-radius: 8px;
                    padding: 8px;
                    margin: 2px;
                    font-weight: bold;
                    color: #333333;
                    text-align: center;
                }
            """)
        else:
            # Буфер и приборы - красные/зелёные
            if self.is_free:
                self.setStyleSheet("""
                    StatusWidget {
                        background-color: #e8f5e8;
                        border: 2px solid #4caf50;
                        border-radius: 8px;
                        padding: 8px;
                        margin: 2px;
                        font-weight: bold;
                        color: #2e7d32;
                        text-align: center;
                    }
                """)
            else:
                self.setStyleSheet("""
                    StatusWidget {
                        background-color: #ffebee;
                        border: 2px solid #f44336;
                        border-radius: 8px;
                        padding: 8px;
                        margin: 2px;
                        font-weight: bold;
                        color: #c62828;
                        text-align: center;
                    }
                """)

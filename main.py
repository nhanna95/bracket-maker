from functools import partial
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import os

win_placements = [
    12, 12, 13, 13, 14, 14, 15, 15, 17, 17, 19, 19, 20, 20, 21, 
    21, 22, 22, 23, 23, 26, 26, 25, 25, 27, 27, -1, 29, -1, -1
]
lose_placements = [
    8, 8, 9, 9, 10, 10, 11, 11, -1, -1, -1, -1, 18, 18, 16, 
    16, -1, -1, -1, -1, 24, 24, -1, -1, -1, -1, 28, -1, -1, -1
]
opponent_placements = [
    1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 
    17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28
]
button_locations = [
    [0, 0],  # 1
    [1, 0],

    [4, 0],  # 2
    [5, 0],

    [8, 0],  # 3
    [9, 0],

    [12, 0],  # 4
    [13, 0],

    [18, 0],  # 5
    [19, 0],

    [22, 0],  # 6
    [23, 0],

    [2, 1],  # 7
    [3, 1],

    [10, 1],  # 8
    [11, 1],

    [17, 1],  # 9
    [18, 1],

    [21, 1],  # 10
    [22, 1],

    [6, 2],  # 11
    [7, 2],

    [19, 2],  # 12
    [20, 2],

    [18, 3],  # 13
    [19, 3],

    [6, 3],  # 14
    [7, 3],

    [6, 4],  # 15
    [7, 4]
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.input_win = None
        self.win_indexes = []
        self.names = []
        
        width = 1000
        height = 600
        self.resize(width, height)
        self.setWindowTitle('Game Bracket')
        layout = QGridLayout()
        
        self.input_button = QPushButton('Input names')
        layout.addWidget(self.input_button, 14, 4)
        self.input_button.clicked.connect(self.input_names)
        
        self.save_button = QPushButton('Save Bracket')
        layout.addWidget(self.save_button, 15, 4)
        self.save_button.clicked.connect(self.save_bracket)
        
        self.load_button = QPushButton('Load Bracket')
        layout.addWidget(self.load_button, 16, 4)
        self.load_button.clicked.connect(self.load_bracket)
        
        self.winner_label = QLabel('Winner: ')
        layout.addWidget(self.winner_label, 0, 4)
        
        self.buttons = []
        for i in range(30):
            b = QPushButton()
            b.clicked.connect(partial(self.advance_player, i))
            self.buttons.append(b)
            layout.addWidget(
                b, button_locations[i][0], button_locations[i][1])
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

# Nixon, Yakub, Arnav, Juwon, Mason, Subbu
    def advance_player(self, index):
        if not (index in self.win_indexes):
            self.win_indexes.append(index)
            
        if index == 26 or index == 28 or index == 29:
            self.winner_label.setText('Winner: ' + self.buttons[index].text())
            
        self.buttons[index].setStyleSheet('background-color : cornflowerblue')
        
        next_placement = win_placements[index]
        if next_placement != -1:
            self.buttons[next_placement].setText(self.buttons[index].text())
            
            if next_placement in self.win_indexes:
                self.advance_player(next_placement)
            elif opponent_placements[next_placement] in self.win_indexes:
                self.advance_player(opponent_placements[next_placement])

        opp_index = opponent_placements[index]
        if opp_index in self.win_indexes:
            self.win_indexes.remove(opp_index)
            
        self.buttons[opp_index].setStyleSheet('background-color : light gray')
        
        next_placement = lose_placements[opp_index]
        if next_placement != -1:
            self.buttons[next_placement].setText(
                self.buttons[opp_index].text())
            
            # TODO hide buttons if by
            if self.buttons[opponent_placements[next_placement]].text() == 'By':
                self.advance_player(next_placement)
            elif next_placement in self.win_indexes:
                self.advance_player(next_placement)
            elif opponent_placements[next_placement] in self.win_indexes:
                self.advance_player(opponent_placements[next_placement])

    def save_bracket(self, file_name):
        file_filter = 'Text File (*.txt)'
        file_name = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Text File (*.txt)'
        )
        with open(file_name[0], 'w') as f:
            file_text = ''
            for name in self.names:
                if name is None:
                    file_text += '? '
                else:
                    file_text += name + ' '
            file_text += '\n'
            for ind in self.win_indexes:
                file_text += str(ind) + ' '
            f.write(file_text)

    def load_bracket(self):
        file_filter = 'Text File (*.txt)'
        file_name = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Text File (*.txt)'
        )
        with open(file_name[0], 'r') as f:
            lines = f.readlines()
            
            self.names = lines[0].split(' ')[:-1]
            self.names = [None if n == '?' else n for n in self.names]
            self.init_bracket(self.names)
            
            indexes = lines[1].split(' ')[:-1]
            self.win_indexes = [int(i) for i in indexes]
            for ind in self.win_indexes:
                self.advance_player(ind)

    def input_names(self, checked):
        if self.input_win is None:
            self.input_win = self.InputWindow(self)
        self.input_win.show()

    def init_bracket(self, names):
        self.names = names + [None] * (8-len(names))
        placements = [0, 6, 4, 2, 3, 5, 7, 1]
        
        for i in range(8):
            if self.names[i] is None:
                self.buttons[placements[i]].setText('By')
                self.advance_player(placements[i]-1)
            else:
                self.buttons[placements[i]].setText(self.names[i])

    class InputWindow(QWidget):
        def __init__(self, main_win):
            super().__init__()
            self.main_win = main_win
            self.setWindowTitle('Name Entry')
            layout = QVBoxLayout()
            
            self.label = QLabel(
                'Input up to 8 names seperated by comma-spaces')
            layout.addWidget(self.label)
            
            self.input = QLineEdit(self)
            layout.addWidget(self.input)
            
            self.setLayout(layout)

        def on_return(self):
            names = self.input.text().split(', ')
            self.close()
            self.main_win.init_bracket(names)

        def keyPressEvent(self, event):
            if event.key() == Qt.Key.Key_Return:
                self.on_return()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

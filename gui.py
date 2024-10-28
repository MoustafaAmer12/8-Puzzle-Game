from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from SolverFactory import SolverFactory as factory

states = ["123405678", "123450678", "123456078", "123456708", "123456780"]

class GameData(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        container = QVBoxLayout()

        game_data_label = QLabel("Solution Data")
        game_data_label.setContentsMargins(0,30,0,20)

        path = QHBoxLayout()
        path.addWidget(QLabel("Path To Goal"), stretch=4)
        path.addWidget(QLabel("Up, Down, Left ..."), stretch=6)

        cost = QHBoxLayout()
        cost.addWidget(QLabel("Cost Of Path"), stretch=4)
        cost.addWidget(QLabel("1231"), stretch=6)

        nodes_expanded = QHBoxLayout()
        nodes_expanded.addWidget(QLabel("Nodes Expanded"), stretch=4)
        nodes_expanded.addWidget(QLabel("12"), stretch=6)

        depth = QHBoxLayout()
        depth.addWidget(QLabel("Search Depth"), stretch=4)
        depth.addWidget(QLabel("123"), stretch=6)

        run_time = QHBoxLayout()
        run_time.addWidget(QLabel("Running Time"), stretch=4)
        run_time.addWidget(QLabel("12311014"), stretch=6)

        container.addWidget(game_data_label)
        container.addLayout(path)
        container.addLayout(cost)
        container.addLayout(nodes_expanded)
        container.addLayout(depth)
        container.addLayout(run_time)

        container.setSpacing(10)

        self.setLayout(container)

class ValLineEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("012345678")

        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red;")

        layout.addWidget(self.line_edit)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def validate_input(self):
        input_text = self.line_edit.text()

        self.error_label.setText("")
        if len(input_text) != 9:
            self.error_label.setText("Error: Input must be exactly 9 characters long.")
            return False

        if not all(char in '012345678' for char in input_text):
            self.error_label.setText("Error: Input must only contain digits from 0 to 8.")
            return False

        if len(set(input_text)) != 9:
            self.error_label.setText("Error: Each digit must appear exactly once.")
            return False

        self.error_label.setText("")
        return True

class AlgSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.algo_selection = QComboBox()
        choices = ["DFS", "BFS", "Iterative DFS", "A* (Manhattan)", "A* (Euclidean)"]

        self.algo_selection.addItems(choices)

        layout = QVBoxLayout()
        layout.addWidget(self.algo_selection)
        self.setLayout(layout)

    def on_change_selection(self):
        return self.algo_selection.currentText()



# Grid Control
class GridControl(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(31)
        slider.setMaximum(31)
        prevButton = QToolButton()
        nextButton = QToolButton()

        self.addWidget(slider, stretch=6)
        self.addWidget(prevButton, stretch=2)
        self.addWidget(nextButton, stretch=2)
        self.setContentsMargins(30, 0, 30, 20)


class SolveButton(QWidget):
    def __init__(self, validator: ValLineEdit, alg_selection: AlgSelection):
        super().__init__()
        self.validator = validator
        self.alg_selection = alg_selection
        self.states = []
        self.initialState = "012345678"
        self.alg = "DFS"
        self.initUI()
    
    def initUI(self):
        self.submitButton = QPushButton("Solve", self)

        self.submitButton.clicked.connect(self.handle_submission)
        layout = QVBoxLayout()
        layout.addWidget(self.submitButton)
        self.setLayout(layout)



    def handle_submission(self):
        if self.validator.validate_input():
            self.initialState = self.validator.line_edit.text()
            self.alg = self.alg_selection.on_change_selection()
            solver = factory(self.initialState).get_method(self.alg)
            solver.solve()
            # self.states = states

# Side Layout
class SideLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        input_label = QLabel("Enter Input Row Wise")
        input = ValLineEdit()
        widget1 = QVBoxLayout()
        widget1.addWidget(input_label)
        widget1.addWidget(input)
        widget1.setSpacing(10)

        algo_label = QLabel("Choose Algorithm")
        alg_selection = AlgSelection()

        widget2 = QVBoxLayout()
        widget2.addWidget(algo_label)
        widget2.addWidget(alg_selection)
        widget2.setSpacing(10)

        widget3 = QHBoxLayout()
        self.button = SolveButton(input, alg_selection)
        widget3.addWidget(QLabel(), stretch=8)
        widget3.addWidget(self.button, stretch=2)
        widget3.setContentsMargins(0,0,20,0)

        controller = GridControl()
        game_controller = QVBoxLayout()
        game_controller.addWidget(QLabel("Inspect Solution"))
        game_controller.addLayout(controller)
        game_controller.setSpacing(10)

        game_data = GameData()

        self.addLayout(widget1, stretch=1)
        self.addLayout(widget2, stretch=1)
        self.addLayout(widget3, stretch=1)
        self.addLayout(game_controller, stretch=1)
        self.addWidget(game_data)
        self.addWidget(QLabel(), stretch=3)
        self.setContentsMargins(30, 20, 30, 20)
    
    @property
    def states(self):
        return self.button.states
    
    @property
    def initalState(self):
        return self.button.initialState
    
    @property
    def alg(self):
        return self.button.alg
        
# Game Grid
class GameGrid(QGraphicsView):
    def __init__(self, state="012345678"):
        super().__init__()
        self.state = state
        self.items = []
        self.animations = []
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setFixedSize(600, 600)
        self.initUI()

    def initUI(self):
        self.refreshGrid(self.state)

    def refreshGrid(self, custom_state = None):
        self.scene.clear()
        self.items = []
        
        if custom_state is not None: 
            self.state = custom_state
        
        for i in range(len(self.state)):
            item = QGraphicsTextItem(f"{self.state[i]}")
            item.setDefaultTextColor(Qt.GlobalColor.white)
            item.setFont(QFont("Arial", 24))
            item.setPos((i % 3) * 200, int(i / 3) * 200)
            self.scene.addItem(item)
            self.items.append(item)

    def find_swapped_indices(self, prev_state: str, new_state: str):
        ind1 = prev_state.find('0')
        ind2 = new_state.find('0')
        return ind1, ind2
    

    def animate_swap(self, index1, index2):
        item1 = self.items[index1]
        item2 = self.items[index2]

        # Create animations for both widgets
        anim1 = QPropertyAnimation(item1, b"pos")
        anim1.setDuration(500)
        anim1.setStartValue(item1.pos())
        anim1.setEndValue(item2.pos())

        anim2 = QPropertyAnimation(item2, b"pos")
        anim2.setDuration(500)
        anim2.setStartValue(item2.pos())
        anim2.setEndValue(item1.pos())

        self.animations.append(anim1)
        self.animations.append(anim2)

        # Update state after animations
        anim1.finished.connect(lambda: self.update_state(index1, index2))
        anim2.finished.connect(lambda: self.update_state(index1, index2))

        # Start animations
        anim1.start()
        anim2.start()

    def update_state(self, index1, index2):
        # Swap the values in the state
        self.state = list(self.state)
        self.state[index1], self.state[index2] = self.state[index2], self.state[index1]
        self.state = ''.join(self.state)
        self.refreshGrid()
        self.animations.clear()

    def updateState(self, new_state):
        ind1, ind2 = self.find_swapped_indices(self.state, new_state)
        self.animate_swap(ind1, ind2)
        

# Game Side Layout
class GameLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.game_grid = GameGrid()

        centered_layout = QHBoxLayout()
        centered_layout.addStretch()
        centered_layout.addWidget(self.game_grid)
        centered_layout.addStretch()


        self.addLayout(centered_layout)
    
    
    def playTransitions(self, states):
        for i, state in enumerate(states):
            QTimer.singleShot(i * 1000, lambda st=state: self.game_grid.updateState(st))

# App Layout
class AppLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.initialState = ""
        self.alg = ""
        self.initUI()

    def initUI(self):
        self.side_layout = SideLayout()
        self.game_layout = GameLayout()

        self.setSpacing(40)

        height = int(QApplication.primaryScreen().availableGeometry().height()*0.6)
        widget = QWidget()
        widget.setFixedHeight(height)
        widget.setLayout(self.game_layout) 
        self.addWidget(widget, stretch=6)
        self.addLayout(self.side_layout, stretch=4)

        self.side_layout.button.submitButton.clicked.connect(
            self.handleSubmission
        )
    
    def handleSubmission(self):
        self.initialState = self.side_layout.initalState
        # self.alg = self.side_layout.alg
        self.game_layout.game_grid.refreshGrid(self.initialState),
        QTimer.singleShot(2000, lambda: 
            self.game_layout.playTransitions(self.side_layout.states)
        )

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    
    def initUI(self):
        # Set The Size & Position Dynamically
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        width = int(screen_geometry.width() * 0.7)
        height = int(screen_geometry.height() * 0.8)
        self.resize(width, height)

        x = int((screen_geometry.width() - width) / 2)
        y = int((screen_geometry.height() - height) / 2)
        self.move(x, y)

        # Set Title
        self.setWindowTitle("8 Puzzle Game")
        
        # Define Custom Layout
        layout = AppLayout()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
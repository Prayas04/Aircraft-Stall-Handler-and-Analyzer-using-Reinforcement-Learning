import sys
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QApplication, QTabWidget, QMainWindow, QPushButton, QVBoxLayout, QWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from stable_baselines3 import PPO
from threading import Thread
import time

# Import your custom environment
from AircraftSHAgent import CustomStallRecoveryEnv


class FlightPlot(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.ax.set_facecolor("#1e1e1e")  # Dark background
        self.ax.set_xlabel("Time Elapsed (seconds)", color="white", fontsize=12)
        self.ax.set_ylabel("Angle of Attack (degrees) and Altitude (feet)", color="white", fontsize=12)
        self.ax.tick_params(colors="white")
        self.ax.grid(color="gray")
        self.alpha_data, self.alt_data = [], []
        self.time_data = []

    def update_plot(self, alpha, alt, timestep):
        self.time_data.append(timestep)
        self.alpha_data.append(alpha)
        self.alt_data.append(alt)
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")

        # Plot the data
        self.ax.plot(self.time_data, self.alpha_data, label='Angle of Attack (deg)', color="cyan", linewidth=2)
        self.ax.plot(self.time_data, self.alt_data, label='Altitude (ft)', color="orange", linewidth=2)

        # Set axis limits
        self.ax.set_xlim(0, max(self.time_data) + 1)  # Extend x-axis slightly beyond the max time
        self.ax.set_ylim(0, max(max(self.alpha_data, default=0), max(self.alt_data, default=0)) + 1000)  # Extend y-axis

        # Add labels and legend
        self.ax.legend(facecolor="#1e1e1e", edgecolor="white", labelcolor="white", fontsize=10)
        self.ax.set_xlabel("Time Elapsed (seconds)", color="white", fontsize=12)
        self.ax.set_ylabel("Angle of Attack (degrees) and Altitude (feet)", color="white", fontsize=12)
        self.ax.tick_params(colors="white")
        self.ax.grid(color="gray")
        self.draw()


class AnalysisTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a scrollable area for the plots
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main container widget for the scroll area
        container = QWidget()
        self.layout = QVBoxLayout(container)

        # Add individual plots with fixed heights and spacing
        self.alpha_scatter_plot = self.create_plot("Scatter: Angle of Attack vs. Time", "Time (s)", "Angle of Attack (degrees)")
        self.alpha_scatter_plot.setFixedHeight(600)
        self.layout.addWidget(self.alpha_scatter_plot)
        self.layout.addSpacing(20)

        self.altitude_bar_plot = self.create_plot("Bar Graph: Altitude vs. Time", "Time (s)", "Altitude (feet)")
        self.altitude_bar_plot.setFixedHeight(600)
        self.layout.addWidget(self.altitude_bar_plot)
        self.layout.addSpacing(20)

        self.speed_plot = self.create_plot("Line Plot: Speed vs. Time", "Time (s)", "Speed (knots)")
        self.speed_plot.setFixedHeight(600)
        self.layout.addWidget(self.speed_plot)
        self.layout.addSpacing(20)

        self.vertical_speed_plot = self.create_plot("Line Plot: Vertical Speed vs. Time", "Time (s)", "Vertical Speed (ft/min)")
        self.vertical_speed_plot.setFixedHeight(600)
        self.layout.addWidget(self.vertical_speed_plot)
        self.layout.addSpacing(20)

        self.throttle_plot = self.create_plot("Line Plot: Throttle vs. Time", "Time (s)", "Throttle (%)")
        self.throttle_plot.setFixedHeight(600)
        self.layout.addWidget(self.throttle_plot)
        self.layout.addSpacing(20)

        self.roll_plot = self.create_plot("Line Plot: Roll vs. Time", "Time (s)", "Roll (degrees)")
        self.roll_plot.setFixedHeight(600)
        self.layout.addWidget(self.roll_plot)
        self.layout.addSpacing(20)

        self.stall_margin_plot = self.create_plot("Line Plot: Stall Margin vs. Time", "Time (s)", "Stall Margin (degrees)")
        self.stall_margin_plot.setFixedHeight(600)
        self.layout.addWidget(self.stall_margin_plot)

        # Set the container widget as the scroll area's widget
        scroll_area.setWidget(container)

        # Add the scroll area to the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_plot(self, title, xlabel, ylabel):
        """Helper function to create a plot with a title, x-label, and y-label."""
        fig, ax = plt.subplots()
        canvas = FigureCanvas(fig)
        ax.set_facecolor("#f9f9f9")  # Light background
        ax.set_title(title, color="black", fontsize=14)
        ax.set_xlabel(xlabel, color="black", fontsize=12)
        ax.set_ylabel(ylabel, color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        return canvas

    def update_alpha_scatter_plot(self, time_data, alpha_data):
        """Update the Scatter Plot for Angle of Attack vs. Time."""
        self.alpha_scatter_plot.figure.clear()
        ax = self.alpha_scatter_plot.figure.add_subplot(111)
        ax.set_facecolor("#f9f9f9")
        ax.scatter(time_data, alpha_data, label="Angle of Attack (deg)", color="blue", s=10)
        ax.set_title("Scatter: Angle of Attack vs. Time", color="black", fontsize=14)
        ax.set_xlabel("Time (s)", color="black", fontsize=12)
        ax.set_ylabel("Angle of Attack (degrees)", color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        ax.legend(facecolor="#f9f9f9", edgecolor="black", labelcolor="black", fontsize=10)
        self.alpha_scatter_plot.draw()

    def update_altitude_bar_plot(self, time_data, altitude_data):
        """Update the Bar Graph for Altitude vs. Time."""
        self.altitude_bar_plot.figure.clear()
        ax = self.altitude_bar_plot.figure.add_subplot(111)
        ax.set_facecolor("#f9f9f9")
        ax.bar(time_data, altitude_data, label="Altitude (ft)", color="orange", width=0.1)
        ax.set_title("Bar Graph: Altitude vs. Time", color="black", fontsize=14)
        ax.set_xlabel("Time (s)", color="black", fontsize=12)
        ax.set_ylabel("Altitude (feet)", color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        ax.legend(facecolor="#f9f9f9", edgecolor="black", labelcolor="black", fontsize=10)
        self.altitude_bar_plot.draw()

    def update_speed_plot(self, time_data, speed_data):
        """Update the Speed vs. Time plot."""
        self.speed_plot.figure.clear()
        ax = self.speed_plot.figure.add_subplot(111)
        ax.set_facecolor("#f9f9f9")
        ax.plot(time_data, speed_data, label="Speed (knots)", color="blue", linewidth=2)
        ax.set_title("Speed vs. Time", color="black", fontsize=14)
        ax.set_xlabel("Time (s)", color="black", fontsize=12)
        ax.set_ylabel("Speed (knots)", color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        ax.legend(facecolor="#f9f9f9", edgecolor="black", labelcolor="black", fontsize=10)
        self.speed_plot.draw()

    def update_vertical_speed_plot(self, time_data, vertical_speed_data):
        """Update the Vertical Speed vs. Time plot."""
        self.vertical_speed_plot.figure.clear()
        ax = self.vertical_speed_plot.figure.add_subplot(111)
        ax.set_facecolor("#f9f9f9")
        ax.plot(time_data, vertical_speed_data, label="Vertical Speed (ft/min)", color="green", linewidth=2)
        ax.set_title("Vertical Speed vs. Time", color="black", fontsize=14)
        ax.set_xlabel("Time (s)", color="black", fontsize=12)
        ax.set_ylabel("Vertical Speed (ft/min)", color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        ax.legend(facecolor="#f9f9f9", edgecolor="black", labelcolor="black", fontsize=10)
        self.vertical_speed_plot.draw()

    def update_throttle_plot(self, time_data, throttle_data):
        """Update the Throttle vs. Time plot."""
        self.throttle_plot.figure.clear()
        ax = self.throttle_plot.figure.add_subplot(111)
        ax.set_facecolor("#f9f9f9")
        ax.plot(time_data, throttle_data, label="Throttle (%)", color="orange", linewidth=2)
        ax.set_title("Throttle vs. Time", color="black", fontsize=14)
        ax.set_xlabel("Time (s)", color="black", fontsize=12)
        ax.set_ylabel("Throttle (%)", color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        ax.legend(facecolor="#f9f9f9", edgecolor="black", labelcolor="black", fontsize=10)
        self.throttle_plot.draw()

    def update_roll_plot(self, time_data, roll_data):
        """Update the Roll vs. Time plot."""
        self.roll_plot.figure.clear()
        ax = self.roll_plot.figure.add_subplot(111)
        ax.set_facecolor("#f9f9f9")
        ax.plot(time_data, roll_data, label="Roll (degrees)", color="purple", linewidth=2)
        ax.set_title("Roll vs. Time", color="black", fontsize=14)
        ax.set_xlabel("Time (s)", color="black", fontsize=12)
        ax.set_ylabel("Roll (degrees)", color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        ax.legend(facecolor="#f9f9f9", edgecolor="black", labelcolor="black", fontsize=10)
        self.roll_plot.draw()

    def update_stall_margin_plot(self, time_data, stall_margin_data):
        """Update the Stall Margin vs. Time plot."""
        self.stall_margin_plot.figure.clear()
        ax = self.stall_margin_plot.figure.add_subplot(111)
        ax.set_facecolor("#f9f9f9")
        ax.plot(time_data, stall_margin_data, label="Stall Margin (degrees)", color="red", linewidth=2)
        ax.set_title("Stall Margin vs. Time", color="black", fontsize=14)
        ax.set_xlabel("Time (s)", color="black", fontsize=12)
        ax.set_ylabel("Stall Margin (degrees)", color="black", fontsize=12)
        ax.tick_params(colors="black")
        ax.grid(color="gray")
        ax.legend(facecolor="#f9f9f9", edgecolor="black", labelcolor="black", fontsize=10)
        self.stall_margin_plot.draw()


class FlightDataTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        # Flight Plot
        self.flight_plot = FlightPlot()
        self.layout.addWidget(self.flight_plot)

        # Flight Data Table
        self.flight_data_table = QTableWidget()
        self.flight_data_table.setColumnCount(9)  # Add columns for new parameters
        self.flight_data_table.setHorizontalHeaderLabels([
            "Time (s)", "Angle of Attack (deg)", "Altitude (ft)", "Speed (knots)",
            "Vertical Speed (ft/min)", "Throttle (%)", "Roll (deg)", "Stall Margin (deg)", "Status"
        ])
        self.flight_data_table.setStyleSheet("""
            QTableWidget {
                background-color: #0d1b2a;
                color: #00d4ff;
                border: 2px solid #3a607f;
                font-size: 14px;
                font-family: 'Orbitron', sans-serif;
            }
            QHeaderView::section {
                background-color: #1e3a5f;
                color: white;
                font-size: 14px;
                font-family: 'Orbitron', sans-serif;
            }
        """)
        self.layout.addWidget(self.flight_data_table)

        self.setLayout(self.layout)

    def update_flight_data(self, time_data, alpha_data, altitude_data, speed_data, vertical_speed_data, throttle_data, roll_data, stall_margin_data, status_data):
        """Update the flight data table with new data."""
        self.flight_data_table.setRowCount(len(time_data))
        for i, (time, alpha, altitude, speed, vertical_speed, throttle, roll, stall_margin, status) in enumerate(
                zip(time_data, alpha_data, altitude_data, speed_data, vertical_speed_data, throttle_data, roll_data, stall_margin_data, status_data)):
            self.flight_data_table.setItem(i, 0, QTableWidgetItem(f"{time:.2f}"))
            self.flight_data_table.setItem(i, 1, QTableWidgetItem(f"{alpha:.2f}"))
            self.flight_data_table.setItem(i, 2, QTableWidgetItem(f"{altitude:.2f}"))
            self.flight_data_table.setItem(i, 3, QTableWidgetItem(f"{speed:.2f}"))
            self.flight_data_table.setItem(i, 4, QTableWidgetItem(f"{vertical_speed:.2f}"))
            self.flight_data_table.setItem(i, 5, QTableWidgetItem(f"{throttle:.2f}"))
            self.flight_data_table.setItem(i, 6, QTableWidgetItem(f"{roll:.2f}"))
            self.flight_data_table.setItem(i, 7, QTableWidgetItem(f"{stall_margin:.2f}"))
            self.flight_data_table.setItem(i, 8, QTableWidgetItem(status))


class SHAA(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SHAA")
        self.setGeometry(100, 100, 1280, 720)  # Set initial size
        self.setMinimumSize(800, 600)  # Minimum size

        # Apply new theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #0d1b2a, stop:1 #1b263b);
                color: white;
            }
            QPushButton {
                background-color: #1e3a5f;
                color: white;
                border: 2px solid #3a607f;
                padding: 10px;
                border-radius: 10px;
                font-size: 16px;
                font-family: 'Orbitron', sans-serif;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #28547a;
            }
            QLabel {
                color: #00d4ff;
                font-size: 18px;
                font-family: 'Orbitron', sans-serif;
                letter-spacing: 1px;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #1e3a5f;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                font-family: 'Orbitron', sans-serif;
            }
            QTabBar::tab:selected {
                background: #28547a;
                font-size: 16px;
            }
            QTextEdit {
                background-color: #0d1b2a;
                color: #00d4ff;
                border: 2px solid #3a607f;
                border-radius: 10px;
                font-size: 14px;
                font-family: 'Orbitron', sans-serif;
            }
        """)

        self.env = CustomStallRecoveryEnv(aircraft='B747')
        self.model = PPO('MlpPolicy', self.env, verbose=1, device='cpu')

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Header
        header = QLabel("Stall Recovery Simulation")
        header.setFont(QFont("Orbitron", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #00d4ff; padding: 10px; letter-spacing: 2px;")

        # Tab 1: Flight Data Tab
        self.flight_data_tab = FlightDataTab()
        self.central_widget.addTab(self.flight_data_tab, "Flight Data")

        # Tab 2: Controls
        self.control_tab = QWidget()
        self.control_layout = QVBoxLayout()
        self.train_button = QPushButton("Train Agent")
        self.train_button.clicked.connect(self.train_agent)
        self.control_layout.addWidget(self.train_button)

        self.eval_button = QPushButton("Evaluate Agent")
        self.eval_button.clicked.connect(self.evaluate_agent)
        self.control_layout.addWidget(self.eval_button)

        # Status Label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: black; font-size: 14px;")
        self.control_layout.addWidget(self.status_label)
        self.control_tab.setLayout(self.control_layout)
        self.central_widget.addTab(self.control_tab, "Controls")

        # Tab 3: Analysis
        self.analysis_tab = AnalysisTab()
        self.central_widget.addTab(self.analysis_tab, "Analysis")

        self.training_thread = None
        self.timestep = 0

    def train_agent(self):
        if not self.training_thread:
            self.training_thread = Thread(target=self._train)
            self.training_thread.start()

    def _train(self):
        self.status_label.setText("Status: Training...")
        self.model.learn(total_timesteps=8000)
        self.model.save('stall_recovery_agent')
        self.status_label.setText("Status: Training Complete")
        self.training_thread = None

    def display_stall_warning(self):
        """Display a warning message when a stall condition is detected."""
        warning_message = QLabel("Warning: Stall Condition Detected! Adjusting Parameters...")
        warning_message.setStyleSheet("""
            QLabel {
                color: red;
                font-size: 16px;
                font-family: 'Orbitron', sans-serif;
                background-color: #1e1e1e;
                padding: 10px;
                border: 2px solid red;
                border-radius: 10px;
            }
        """)
        warning_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.control_layout.addWidget(warning_message)

        # Automatically remove the warning message after 3 seconds
        def remove_warning():
            self.control_layout.removeWidget(warning_message)
            warning_message.deleteLater()

        QTimer.singleShot(3000, remove_warning)

    def evaluate_agent(self):
        self.status_label.setText("Status: Evaluating...")
        self.model = PPO.load('stall_recovery_agent')
        obs, _ = self.env.reset()
        terminated = False
        self.timestep = 0

        # Initialize data lists
        time_data, alpha_data, altitude_data, speed_data = [], [], [], []
        vertical_speed_data, throttle_data, roll_data, stall_margin_data, status_data = [], [], [], [], []

        while not terminated:
            action, _ = self.model.predict(obs, deterministic=True)
            obs, _, terminated, _, _ = self.env.step(action)
            alpha = obs[0]
            altitude = obs[4]
            speed = obs[5]  # Example: Assuming speed is available in obs[5]
            vertical_speed = (altitude - altitude_data[-1]) / 0.1 if altitude_data else 0  # Calculate vertical speed
            throttle = obs[6] if len(obs) > 6 else 50  # Example: Assuming throttle is available in obs[6]
            roll = obs[7] if len(obs) > 7 else 0  # Example: Assuming roll is available in obs[7]
            stall_margin = 15 - alpha  # Example: Assuming critical stall angle is 15 degrees

            # Detect stall condition
            if alpha > 15:  # Stall condition: angle of attack > 15 degrees
                self.display_stall_warning()
                alpha = 10  # Adjust angle of attack to recover from stall
                obs[0] = alpha  # Update the observation with the adjusted alpha
                status = "Recovery"
            else:
                status = "Normal"

            # Collect data for analysis
            time_data.append(self.timestep)
            alpha_data.append(alpha)
            altitude_data.append(altitude)
            speed_data.append(speed)
            vertical_speed_data.append(vertical_speed)
            throttle_data.append(throttle)
            roll_data.append(roll)
            stall_margin_data.append(stall_margin)
            status_data.append(status)

            # Update flight data plot
            self.flight_data_tab.flight_plot.update_plot(alpha, altitude, self.timestep)

            self.timestep += 0.1
            time.sleep(0.1)
            QApplication.processEvents()

        # Update flight data table
        self.flight_data_tab.update_flight_data(
            time_data, alpha_data, altitude_data, speed_data, vertical_speed_data,
            throttle_data, roll_data, stall_margin_data, status_data
        )

        # Update analysis plots
        self.analysis_tab.update_alpha_scatter_plot(time_data, alpha_data)
        self.analysis_tab.update_altitude_bar_plot(time_data, altitude_data)
        self.analysis_tab.update_speed_plot(time_data, speed_data)
        self.analysis_tab.update_vertical_speed_plot(time_data, vertical_speed_data)
        self.analysis_tab.update_throttle_plot(time_data, throttle_data)
        self.analysis_tab.update_roll_plot(time_data, roll_data)
        self.analysis_tab.update_stall_margin_plot(time_data, stall_margin_data)

        self.status_label.setText("Status: Evaluation Complete")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SHAA()
    window.show()
    sys.exit(app.exec())

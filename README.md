# ✈️ Aircraft Stall Handler and Analysis using Reinforcement Learning and Historical Datasets

An intelligent flight simulation tool that uses reinforcement learning to detect and recover from aircraft stall conditions, visualized through a modern PyQt6 GUI. The system is capable of both training and evaluating agents in a custom Gym environment using simplified flight dynamics.

---

## 📌 Overview

This project features:

- A **custom reinforcement learning environment** simulating aircraft stall behavior.
- A **PPO agent** (from Stable-Baselines3) trained to recover from stall.
- A **PyQt6 GUI** for live simulation, analysis, and control.
- **Real-time plots** and **flight metrics tables** for post-simulation review.

The goal is to simulate stall recovery with interpretable metrics and a user-friendly interface suitable for researchers, engineers, or enthusiasts.

---

## 🧠 Key Components

- `AircraftSHAgent.py` – Contains the custom Gym environment and training/evaluation logic.
- `main.py` – GUI application for simulation, visualization, training, and analysis.

---

## 🚀 Features

- ✅ Train and evaluate a stall recovery RL agent.
- ✅ Real-time simulation with graphical plots.
- ✅ Flight metrics table with color-coded statuses.
- ✅ Stall detection alerts with automatic adjustment.
- ✅ Scrollable analysis tab with multiple time-series plots.

---

## 🛠️ Installation

### Requirements
- Python 3.10+
- PyQt6
- Gymnasium
- Stable-Baselines3
- NumPy
- Matplotlib

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/aircraft-stall-handler.git
cd aircraft-stall-handler

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
▶️ Usage
1. Run the GUI
bash
Copy
Edit
python main.py
2. Train the Agent
Go to the Controls tab.

Click Train Agent to begin PPO training.

Model is saved as stall_recovery_agent.zip.

3. Evaluate the Agent
Click Evaluate Agent to run a test simulation.

Watch the Flight Data and Analysis tabs update in real time.

📊 Visualizations
Flight Data Tab: Displays a plot of Angle of Attack vs. Altitude over time.

Analysis Tab: Contains scatter, line, and bar plots for:

AoA

Altitude

Speed

Vertical speed

Throttle

Roll

Stall margin

📂 File Structure
python
Copy
Edit
.
├── AircraftSHAgent.py       # Gym environment + PPO training/evaluation
├── main.py                  # PyQt6 GUI application
├── README.md                # Project documentation
├── requirements.txt         # Required dependencies
└── stall_recovery_agent.zip # (generated) trained model file
⚙️ How It Works
The RL agent receives a 7-dimensional observation space (alpha, speed, pitch rate, etc.).

It controls elevator and throttle to adjust flight state.

Rewards are computed based on angle-of-attack and altitude preservation.

Termination occurs on successful recovery or crash.

The GUI tracks the state, logs metrics, and provides intuitive visual feedback.

📌 Future Enhancements
✅ Integrate real-world flight data logs.

🔲 Add 3D visual model or simulation playback.

🔲 Expand to more aircraft models.

🔲 Incorporate adverse weather conditions and control surface failures.

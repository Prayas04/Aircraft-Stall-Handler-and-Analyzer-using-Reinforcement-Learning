# ✈️ Aircraft Stall Handler and Analysis using Reinforcement Learning and Historical Datasets

A simulation-driven system that trains reinforcement learning agents to recognize and recover from aircraft stall conditions, integrated with a PyQt6 GUI for real-time monitoring and data visualization.

---

## 📌 Project Overview

This project leverages **JSBSim**, **Stable-Baselines3**, and **PyQt6** to build a robust aircraft stall recovery handler. Using reinforcement learning (PPO algorithm) and synthetic/historical data, the system:
- Trains an agent to recover from stall conditions.
- Evaluates the agent’s performance across flight episodes.
- Provides real-time plots and tables for detailed analysis.
- Visually alerts when a stall occurs.

---

## 🚀 Features

- **Custom Gym Environment** simulating a Boeing 747 using JSBSim.
- **Reinforcement Learning Agent** using Proximal Policy Optimization (PPO).
- **Real-time PyQt6 GUI**:
  - Dynamic plots for AoA, altitude, throttle, etc.
  - Interactive flight data tables.
  - Warnings for detected stall conditions.
- **Evaluation Mode** to simulate and analyze stall scenarios post-training.

---

## 🧠 Technologies Used

| Category | Libraries/Frameworks |
|---------|----------------------|
| Simulation | [JSBSim](https://github.com/JSBSim-Team/jsbsim) |
| RL Agent | [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3) |
| Environment | [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) |
| GUI | PyQt6, Matplotlib |
| Backend | Python 3.10+ |

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/aircraft-stall-handler.git
   cd aircraft-stall-handler
Create a virtual environment & install dependencies

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
Ensure JSBSim is installed and available

On Linux/macOS: use apt, brew, or build from source.

Windows users may need WSL or precompiled binaries.

📁 Project Structure
bash
Copy
Edit
.
├── AircraftSHAgent.py       # Custom gym environment for stall detection
├── main.py                  # PyQt6-based GUI application
├── stall_recovery_agent.zip # (Generated after training) Trained PPO agent
├── README.md                # You're reading it!
└── requirements.txt         # List of required packages
🧪 How to Use
▶️ Train the Agent
Run the GUI:

bash
Copy
Edit
python main.py
Go to the Controls tab and click "Train Agent".

🧪 Evaluate the Agent
After training, click "Evaluate Agent".

The system will simulate flight scenarios and auto-adjust on stall detection.

📊 Analysis & Visualization
Flight Data Tab: Plots of angle of attack vs. altitude with time.

Analysis Tab: Multiple subplots including throttle, speed, roll, stall margin, etc.

Flight Table: Displays time-series flight stats including recovery status.

⚠️ Stall Warning System
During simulation, if AoA exceeds the critical stall threshold (e.g., 15°), a red warning is shown in the GUI, and the agent attempts automatic recovery.

📸 Screenshots
(Add GUI screenshots here to enhance the readme)

📌 To-Do / Future Improvements
Integration with real historical flight datasets.

Extend support for other aircraft models.

Add more sophisticated failure conditions (engine loss, wind shear, etc.).

Export flight logs to CSV/JSON.

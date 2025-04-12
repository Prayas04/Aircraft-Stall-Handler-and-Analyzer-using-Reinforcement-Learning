🚀 Aircraft Stall Handler and Analysis using Reinforcement Learning and Historical Datasets
Welcome to the Aircraft Stall Handler and Analysis (SHAA) project, a cutting-edge exploration into the world of aviation safety through reinforcement learning (RL)! This project harnesses the power of JSBSim, Stable Baselines3, and a sleek PyQt6-based GUI to train an intelligent agent to recover aircraft from stalls—one of the most critical scenarios in flight dynamics. Whether you're an aviation enthusiast, a machine learning wizard, or simply curious about blending tech with flight, SHAA offers an exciting journey into simulating, analyzing, and mastering stall recovery with a Boeing 747.

Imagine an RL agent acting as a co-pilot, learning to finesse the elevator and throttle to pull a massive jet out of a stall, all while you watch live plots and 3D visualizations dance across your screen. SHAA doesn't just stop at training—it dives deep into flight data analysis, presenting you with vibrant graphs and tables to uncover the secrets of each maneuver. Ready to take off? Let’s explore what makes this project soar!

🌟 Project Highlights
Reinforcement Learning in Action: Train a PPO agent to expertly handle stall recovery, balancing altitude preservation with smooth control inputs.
Realistic Flight Simulation: Powered by JSBSim, a robust open-source flight dynamics model, simulating a B747 with precision.
Interactive GUI: A futuristic PyQt6 interface with tabs for live flight data, agent control, and detailed analytics—think of it as your mission control dashboard!
Rich Visualizations:
Real-time plots of angle of attack, altitude, speed, and more.
Analytical charts (scatter, bar, line) to dissect flight performance.
Stall Detection & Recovery: Instant warnings when stalls occur, with automatic recovery adjustments for seamless simulation.
Extensible Design: Swap aircraft models, tweak rewards, or add historical datasets to take the project to new heights.
🛠️ What’s Under the Hood?
SHAA is built on two core components:

AircraftSHAgent.py:
Defines a CustomStallRecoveryEnv, a Gymnasium environment tailored for stall recovery.
Uses JSBSim to simulate flight dynamics and Stable Baselines3’s PPO for RL training.
Includes a standalone script to train and evaluate the agent for 50,000 timesteps.
main.py:
Powers the SHAA GUI with PyQt6, featuring three tabs:
Flight Data: Live plots and a table tracking nine flight parameters.
Controls: Buttons to train (8,000 timesteps) or evaluate the agent, with status updates and stall warnings.
Analysis: Seven detailed plots to analyze flight metrics like stall margin, roll, and vertical speed.
Runs simulations in real-time, updating visuals every 0.1 seconds.
🎮 Why This Project Rocks
Aviation Meets AI: Test your RL skills in a high-stakes aviation scenario—saving a jet from a stall is no small feat!
Visual Feast: From live plots to analytical graphs, SHAA makes complex data feel like a sci-fi cockpit experience.
Learn by Doing: Experiment with RL hyperparameters, aircraft models, or visualization styles to make the project your own.
Real-World Impact: Insights from stall recovery could inspire advancements in flight safety and autonomous aviation.
📋 Prerequisites
To get SHAA up and running, you’ll need a few tools and libraries. Don’t worry—it’s easier than assembling a model airplane!

Software
Python 3.8+: The backbone of our project. Download Python.
JSBSim: For realistic flight dynamics. Grab it from JSBSim SourceForge or JSBSim GitHub.
TensorBoard (optional): To monitor training like a pro. Install via pip install tensorboard.
Python Libraries
Install these dependencies to fuel the simulation:

bash

Collapse

Wrap

Copy
pip install gymnasium jsbsim numpy stable-baselines3 pyqt6 matplotlib
JSBSim Setup
JSBSim requires aircraft, engine, and systems directories. Place them in your project root or update paths in AircraftSHAgent.py:
python

Collapse

Wrap

Copy
self.sim.set_aircraft_path('path/to/aircraft')
self.sim.set_engine_path('path/to/engine')
self.sim.set_systems_path('path/to/systems')
Ensure the B747 model is included in the aircraft directory.
🛠️ Installation
Let’s get SHAA airborne in a few simple steps:

Clone the Repository:
bash

Collapse

Wrap

Copy
git clone https://github.com/your-repo/aircraft-stall-handler-analysis.git
cd aircraft-stall-handler-analysis
Install Python Dependencies: Create a requirements.txt with:
text

Collapse

Wrap

Copy
gymnasium
jsbsim
numpy
stable-baselines3
pyqt6
matplotlib
Then run:
bash

Collapse

Wrap

Copy
pip install -r requirements.txt
Set Up JSBSim:
Download JSBSim and copy the aircraft, engine, and systems folders to your project directory.
Verify the B747 model is available (aircraft/B747).
Test Your Setup: Run a quick check:
bash

Collapse

Wrap

Copy
python AircraftSHAgent.py
If it starts training, you’re ready to fly!
🚀 Usage
SHAA offers two ways to explore stall recovery: a standalone script for hardcore RL enthusiasts and a dazzling GUI for interactive fun.

1. Standalone Training & Evaluation (AircraftSHAgent.py)
Perfect for diving deep into RL without distractions.

Run It:
bash

Collapse

Wrap

Copy
python AircraftSHAgent.py
What Happens:
Creates a CustomStallRecoveryEnv with a B747.
Trains a PPO agent for 50,000 timesteps—enough to make it a stall-recovery expert!
Saves the model as stall_recovery_agent.zip.
Evaluates the agent, logging:
Total episode reward.
Number of stall events (angle of attack > 15°).
Average altitude loss during stalls.
Outputs results to the console.
Pro Tip: Monitor training with TensorBoard:
bash

Collapse

Wrap

Copy
tensorboard --logdir ./ppo_stall_recovery_tensorboard/
Watch metrics like rewards and losses in real-time!
Training Duration: Expect a few minutes to an hour, depending on your hardware and JSBSim’s simulation speed. Each timestep simulates 0.1 seconds of flight (dt=0.1).
2. Interactive GUI (main.py)
The star of the show—a cockpit-like interface to train, evaluate, and analyze with style.

Launch It:
bash

Collapse

Wrap

Copy
python main.py
Explore the Tabs:
Flight Data:
Live Plot: Tracks angle of attack and altitude in real-time (cyan and orange lines).
Data Table: Displays nine columns: time, angle of attack, altitude, speed, vertical speed, throttle, roll, stall margin, and status (Normal/Recovery).
Controls:
Train Agent: Kicks off training for 8,000 timesteps (shorter for quick testing).
Evaluate Agent: Runs a single episode with the trained model, updating visuals live.
Status Bar: Shows “Training…”, “Evaluating…”, or “Complete”.
Stall Warnings: Red alerts pop up if the angle of attack exceeds 15°, vanishing after 3 seconds.
Analysis:
Seven gorgeous plots in a scrollable panel:
Scatter: Angle of attack vs. time.
Bar: Altitude vs. time.
Line Plots: Speed, vertical speed, throttle, roll, and stall margin vs. time.
Each plot is 600px tall, with clear labels and grids for easy analysis.
Stall Recovery in Action:
During evaluation, if the angle of attack exceeds 15°, the GUI triggers a recovery by setting it to 10° and marks the status as “Recovery”.
Updates occur every 0.1 seconds, giving a smooth, real-time experience.
Training Duration: The GUI’s 8,000 timesteps typically take a few minutes, making it ideal for iterative testing.
Output Files
Model: stall_recovery_agent.zip (saved after training).
Logs: ./ppo_stall_recovery_tensorboard/ (TensorBoard data for training metrics).
Visuals: Live plots and tables persist in the GUI during evaluation.
🗂️ Project Structure
Here’s how SHAA is organized:

text

Collapse

Wrap

Copy
aircraft-stall-handler-analysis/
├── AircraftSHAgent.py              # RL environment and standalone training
├── main.py                         # Interactive GUI with visualizations
├── stall_recovery_agent.zip        # Trained RL model (generated)
├── ppo_stall_recovery_tensorboard/ # Training logs
├── aircraft/                       # JSBSim aircraft models (B747)
├── engine/                         # JSBSim engine configs
├── systems/                        # JSBSim systems configs
├── requirements.txt                # Python dependencies
└── README.md                       # You’re reading it!
🧠 How It Works
Environment (CustomStallRecoveryEnv):
Observation Space: 7D vector [alpha, vc, q, theta, h, throttle, roll] (angle of attack, airspeed, pitch rate, pitch angle, altitude, throttle %, roll angle).
Action Space: 2D vector [elevator, throttle] (normalized between -1 and 1).
Reward Function:
Penalizes high angles of attack (>15°): -(alpha - 15).
Rewards altitude gain: 0.1 * (current_alt - prev_alt).
Penalizes large elevator inputs: -0.01 * |elevator|.
Termination:
Crashes if altitude ≤ 0.
Succeeds if angle of attack < 10° for 10 steps.
Training:
PPO learns to balance elevator and throttle to recover from stalls (initial conditions: alpha 12–18°, speed 40–60 knots, pitch 10–20°).
Standalone: 50,000 timesteps for robust learning.
GUI: 8,000 timesteps for quick demos.
Evaluation:
Loads the trained model and runs one episode.
GUI logs nine parameters, adjusts stalls, and updates plots/tables live.
🔧 Customization Ideas
Make SHAA your own with these tweaks:

New Aircraft: Swap the B747 for another JSBSim model (e.g., Cessna, F-16) in CustomStallRecoveryEnv.
Reward Tuning: Adjust penalties/rewards in step() for different behaviors (e.g., prioritize speed).
GUI Enhancements: Add 3D visualizations using QOpenGLWidget (partially implemented in earlier versions).
Historical Data: Integrate real flight data to validate the agent (not yet implemented but a great extension!).
Hyperparameters: Experiment with PPO’s learning rate, batch size, or network architecture in PPO('MlpPolicy', ...).
⚠️ Known Issues
Observation Mismatch: The GUI assumes obs[5] (speed), obs[6] (throttle), and obs[7] (roll) exist, but the environment’s observation space is correct. Fix by aligning evaluate_agent() with [alpha, vc, q, theta, h, throttle, roll].
Performance: JSBSim can be slow on older hardware. Try reducing dt (e.g., 0.05) or optimizing simulation calls.
GUI Flickering: Frequent plot updates may cause lag. Adjust time.sleep(0.1) to 0.05 or 0.2 for balance.
Training Time: 50,000 timesteps may take hours on slower machines. Use the GUI’s 8,000 timesteps for testing.
🌈 Future Enhancements
Multi-Aircraft Support: Train agents for various planes (fighters, gliders, etc.).
Historical Datasets: Incorporate real-world stall data for training or comparison.
Advanced Visuals: Add 3D aircraft rendering (expand OpenGLAircraft from earlier versions).
Export Data: Save flight logs and plots as CSV/PNG for reports.
Cloud Integration: Run training on GPUs via cloud platforms for speed.
📜 License
SHAA is released under the MIT License. Feel free to use, modify, and share—just give credit where it’s due!

🙌 Acknowledgments
JSBSim Team: For their incredible flight dynamics engine.
Stable Baselines3: Making RL accessible and fun.
PyQt6 & Matplotlib: Powering our sleek GUI and vibrant plots.
You: For exploring this project and pushing aviation AI forward!

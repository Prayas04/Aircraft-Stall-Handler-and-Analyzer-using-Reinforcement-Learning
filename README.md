✈️ Aircraft Stall Handler and Analysis using Reinforcement Learning and Historical Datasets
Welcome to the Aircraft Stall Handler and Analysis (SHAA) project—an exhilarating fusion of reinforcement learning (RL) and aviation safety! Picture this: a Boeing 747 teetering on the edge of a stall, with an AI co-pilot skillfully adjusting the elevator and throttle to save the day. SHAA brings this vision to life using JSBSim for realistic flight dynamics, Stable Baselines3 PPO for intelligent control, and a stunning PyQt6 GUI to visualize every heart-pounding moment. Whether you’re an AI enthusiast, an aviation buff, or just curious about cutting-edge tech, SHAA invites you to soar into the world of stall recovery and flight analysis!

This project trains an RL agent to master stall recovery, displays live flight data in vibrant plots and tables, and dives deep into post-flight analytics with colorful graphs. From real-time stall warnings to detailed breakdowns of angle of attack, altitude, and more, SHAA is your cockpit for exploring the skies of AI-driven aviation. Ready to take the controls? Let’s get started!

🌟 Why SHAA Rocks
AI Meets Aviation: Train a PPO agent to recover a B747 from stalls, learning the art of smooth, safe flying.
Realistic Simulations: Powered by JSBSim, delivering authentic flight dynamics for immersive training.
Sleek GUI: A PyQt6 interface with live plots, data tables, and analytical charts—your personal flight dashboard!
Stall Recovery Smarts: Detects stalls (angle of attack > 15°) and triggers recovery, with red alerts for drama.
Data Deep Dive: Analyze speed, roll, throttle, and stall margin with scatter, bar, and line plots.
Hackable & Fun: Swap aircraft, tweak rewards, or add historical data to make SHAA your own.
🛠️ What’s Inside?
SHAA is built on two key components:

AircraftSHAgent.py:
Defines the CustomStallRecoveryEnv, a Gymnasium environment for stall recovery using JSBSim.
Trains and evaluates a PPO agent standalone for 50,000 timesteps.
Tracks stall events and altitude loss, saving the model as stall_recovery_agent.zip.
main.py:
Launches the SHAA GUI with three tabs:
Flight Data: Real-time plots of angle of attack and altitude, plus a table of nine flight metrics.
Controls: Buttons to train (8,000 timesteps) or evaluate the agent, with status updates and stall warnings.
Analysis: Seven scrollable plots for in-depth flight parameter analysis.
Updates visuals every 0.1 seconds during evaluation for a smooth, immersive experience.
📋 Prerequisites
To launch SHAA, you’ll need a few tools. Think of this as pre-flight prep—quick and painless!

Software
Python 3.8+: The engine of our project. Download Python.
JSBSim: For realistic flight simulation. Get it from JSBSim SourceForge or JSBSim GitHub.
TensorBoard (optional): To monitor training like a flight data recorder. Install with pip install tensorboard.
Python Libraries
Fuel up with these dependencies:

bash

Collapse

Wrap

Copy
pip install gymnasium jsbsim numpy stable-baselines3 pyqt6 matplotlib
JSBSim Setup
JSBSim needs aircraft, engine, and systems directories. Place them in your project root or update paths in AircraftSHAgent.py:
python

Collapse

Wrap

Copy
self.sim.set_aircraft_path('path/to/aircraft')
self.sim.set_engine_path('path/to/engine')
self.sim.set_systems_path('path/to/systems')
Ensure the B747 model is in the aircraft directory.
🛠️ Installation
Get SHAA airborne in four easy steps:

Clone the Repository:
bash

Collapse

Wrap

Copy
git clone https://github.com/your-repo/aircraft-stall-handler-analysis.git
cd aircraft-stall-handler-analysis
Install Dependencies: Create a requirements.txt:
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
Configure JSBSim:
Copy the aircraft, engine, and systems folders from JSBSim to your project directory.
Verify the B747 model exists (aircraft/B747).
Test the Setup: Try a quick flight:
bash

Collapse

Wrap

Copy
python AircraftSHAgent.py
If training starts, you’re cleared for takeoff!
🚀 How to Use SHAA
SHAA offers two modes: a standalone script for RL purists and a dazzling GUI for interactive exploration.

1. Standalone Mode (AircraftSHAgent.py)
Perfect for deep dives into RL training and evaluation.

Run It:
bash

Collapse

Wrap

Copy
python AircraftSHAgent.py
What You Get:
Initializes a B747 in CustomStallRecoveryEnv with stall-prone conditions (alpha 12–18°, speed 40–60 knots).
Trains a PPO agent for 50,000 timesteps, learning to dodge stalls.
Saves the model as stall_recovery_agent.zip.
Evaluates the agent in one episode, reporting:
Total reward earned.
Number of stalls (angle of attack > 15°).
Average altitude loss during stalls.
Logs results to the console.
Monitor Progress: Watch training metrics live:
bash

Collapse

Wrap

Copy
tensorboard --logdir ./ppo_stall_recovery_tensorboard/
Time Estimate: Training may take minutes to hours, depending on your CPU and JSBSim speed (each timestep = 0.1s of flight).
2. GUI Mode (main.py)
The star attraction—a sci-fi-inspired interface to train, evaluate, and analyze flights.

Launch It:
bash

Collapse

Wrap

Copy
python main.py
Navigate the Tabs:
Flight Data:
Live Plot: Angle of attack (cyan) and altitude (orange) updated every 0.1s.
Table: Tracks time, angle of attack, altitude, speed, vertical speed, throttle, roll, stall margin, and status (Normal/Recovery).
Controls:
Train Agent: Starts a 8,000-timestep training session (runs in a background thread).
Evaluate Agent: Loads the trained model and runs one episode, updating visuals live.
Status: Shows “Ready”, “Training…”, “Evaluating…”, or “Complete”.
Stall Alerts: Red warnings flash for 3 seconds if angle of attack exceeds 15°, triggering recovery.
Analysis:
Scrollable plots (600px each):
Scatter: Angle of attack vs. time (blue dots).
Bar: Altitude vs. time (orange bars).
Line Plots: Speed (blue), vertical speed (green), throttle (orange), roll (purple), stall margin (red).
Updates after evaluation for deep insights.
Stall Handling:
If angle of attack > 15°, the GUI sets it to 10°, marks status as “Recovery”, and shows a warning.
Data updates every 0.1s for a smooth, real-time feel.
Time Estimate: GUI training (8,000 timesteps) takes a few minutes, ideal for quick experiments.
Outputs
Model: stall_recovery_agent.zip (post-training).
Logs: ./ppo_stall_recovery_tensorboard/ (training metrics).
Visuals: Live GUI plots and tables, persisting during evaluation.
🗂️ Project Structure
Here’s your flight plan:

text

Collapse

Wrap

Copy
aircraft-stall-handler-analysis/
├── AircraftSHAgent.py              # RL environment and standalone training
├── main.py                         # GUI with live visualizations
├── stall_recovery_agent.zip        # Trained model (generated)
├── ppo_stall_recovery_tensorboard/ # TensorBoard logs
├── aircraft/                       # JSBSim aircraft (B747)
├── engine/                         # JSBSim engine configs
├── systems/                        # JSBSim systems configs
├── requirements.txt                # Python dependencies
└── README.md                       # Your guide to SHAA
🧠 How SHAA Works
Environment:
Observation: 7D vector [alpha, vc, q, theta, h, throttle, roll] (angle of attack, airspeed, pitch rate, pitch, altitude, throttle %, roll).
Action: 2D vector [elevator, throttle] (-1 to 1).
Rewards:
- (alpha - 15) for angles > 15° (avoid stalls).
0.1 * altitude_gain for climbing.
-0.01 * |elevator| for smooth controls.
Termination:
Crash: Altitude ≤ 0.
Success: Angle of attack < 10° for 10 steps.
Training:
PPO learns to recover from stalls (initial alpha 12–18°, speed 40–60 knots).
Standalone: 50,000 timesteps for mastery.
GUI: 8,000 timesteps for quick results.
Evaluation:
Runs one episode with the trained model.
GUI logs nine metrics, adjusts stalls, and updates visuals live.
🔧 Customize Your Flight
Take SHAA to new altitudes:

Aircraft Swap: Use Cessna or F-16 by changing aircraft='B747' in CustomStallRecoveryEnv.
Reward Play: Tweak step() rewards (e.g., prioritize speed with 0.05 * vc).
GUI Upgrades: Add 3D visuals via QOpenGLWidget or new plot types.
Historical Data: Mock up flight logs to train or validate (future feature!).
PPO Tuning: Adjust learning rate or layers in PPO('MlpPolicy', ...).
⚠️ Heads-Up
Observation Bug: GUI assumes obs[5] (speed), obs[6] (throttle), obs[7] (roll), but indices are off. Fix by mapping to [alpha, vc, q, theta, h, throttle, roll].
Performance: JSBSim can tax older CPUs. Try dt=0.05 or a faster machine.
GUI Lag: Frequent updates may stutter. Adjust time.sleep(0.1) to 0.2 for stability.
Training Time: 50,000 timesteps may take hours. Use GUI’s 8,000 for speed.
🌈 Future Horizons
Multi-Aircraft: Train for fighters, drones, or gliders.
Real Data: Add historical stall logs for training.
3D Visuals: Revive OpenGL aircraft rendering for immersive views.
Export Tools: Save plots/tables as PNG/CSV.
Cloud Power: Train faster with GPU clusters.
📜 License
SHAA flies under the MIT License. Use it, tweak it, share it—just give a nod to the creators!

🙌 Shoutouts
JSBSim Team: For epic flight dynamics.
Stable Baselines3: RL made simple and strong.
PyQt6 & Matplotlib: Crafting our cockpit visuals.
You: For joining this AI-aviation adventure!

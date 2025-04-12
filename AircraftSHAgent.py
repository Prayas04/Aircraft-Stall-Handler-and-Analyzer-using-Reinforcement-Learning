import gymnasium as gym
import jsbsim
import numpy as np
from stable_baselines3 import PPO

class CustomStallRecoveryEnv(gym.Env):
    def __init__(self, aircraft='B747', dt=0.1):
        super(CustomStallRecoveryEnv, self).__init__()
        self.aircraft = aircraft
        self.dt = dt  # Time step in seconds

        # Initialize JSBSim simulation
        self.sim = jsbsim.FGFDMExec(None)
        self.sim.set_aircraft_path('aircraft')
        self.sim.set_engine_path('engine')
        self.sim.set_systems_path('systems')
        self.sim.load_model(self.aircraft)
        self.sim.set_dt(self.dt)

        # Define action and observation spaces
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)  # elevator, throttle
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32
        )  # alpha, vc, q, theta, h, throttle, roll

        # Task parameters
        self.critical_alpha = 15  # Critical angle of attack (degrees)
        self.safe_alpha = 10      # Safe angle of attack for recovery (degrees)
        self.recovery_counter = 0
        self.required_recovery_steps = 10  # Steps needed to consider recovered

        # Track previous altitude for reward calculation
        self.prev_alt = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Set initial conditions near stall
        self.sim.set_property_value('ic/alpha-deg', np.random.uniform(12, 18))
        self.sim.set_property_value('ic/vc-kts', np.random.uniform(40, 60))
        self.sim.set_property_value('ic/theta-deg', np.random.uniform(10, 20))
        self.sim.set_property_value('ic/h-sl-ft', 3280)  # ~1000m
        self.sim.set_property_value('ic/phi-deg', 0)
        self.sim.set_property_value('ic/psi-deg', 0)
        self.sim.run_ic()  # Initialize the simulation

        self.prev_alt = self.sim.get_property_value('position/h-sl-ft')
        self.recovery_counter = 0
        return self._get_observation(), {}

    def step(self, action):
        # Apply actions
        self.sim.set_property_value('fcs/elevator-cmd-norm', action[0])
        self.sim.set_property_value('fcs/throttle-cmd-norm', action[1])

        # Run simulation for one time step
        self.sim.run()

        # Get new observation
        obs = self._get_observation()

        # Compute reward
        alpha = self.sim.get_property_value('aero/alpha-deg')
        alt = self.sim.get_property_value('position/h-sl-ft')
        alt_gain = alt - self.prev_alt
        self.prev_alt = alt

        reward = 0
        if alpha > self.critical_alpha:
            reward -= (alpha - self.critical_alpha)  # Penalize high alpha
        reward += 0.1 * alt_gain  # Reward altitude preservation
        reward -= 0.01 * np.abs(action[0])  # Penalize large elevator inputs

        # Check termination conditions
        terminated = False
        if alt <= 0:  # Crash
            terminated = True
        elif alpha < self.safe_alpha:
            self.recovery_counter += 1
            if self.recovery_counter >= self.required_recovery_steps:
                terminated = True  # Successfully recovered
        else:
            self.recovery_counter = 0

        return obs, reward, terminated, False, {}

    def _get_observation(self):
        """
        Extract observation from the simulation state.
        
        Returns:
            np.ndarray: Observation array [alpha, vc, q, theta, h, throttle, roll].
        """
        alpha = self.sim.get_property_value('aero/alpha-deg')
        vc = self.sim.get_property_value('velocities/vc-kts')
        q = self.sim.get_property_value('velocities/q-rad_sec')
        theta = self.sim.get_property_value('attitude/theta-deg')
        h = self.sim.get_property_value('position/h-sl-ft')
        throttle = self.sim.get_property_value('fcs/throttle-cmd-norm') * 100  # Convert to percentage
        roll = self.sim.get_property_value('attitude/phi-deg')

        return np.array([alpha, vc, q, theta, h, throttle, roll])

    def close(self):
        """Clean up the simulation instance."""
        self.sim = None

def main():
    """Train and evaluate the stall recovery agent."""
    # Create environment
    env = CustomStallRecoveryEnv(aircraft='B747')
    
    # Initialize PPO agent
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./ppo_stall_recovery_tensorboard/")
    
    # Train the agent
    print("Training the stall recovery agent...")
    model.learn(total_timesteps=50000)
    
    # Save the trained model
    model.save('stall_recovery_agent')
    print("Model saved as 'stall_recovery_agent.zip'")
    
    # Evaluate the agent
    print("Evaluating the trained agent...")
    model = PPO.load('stall_recovery_agent')
    obs, _ = env.reset()
    terminated = False
    episode_reward = 0
    states_log = []  # For analysis
    
    while not terminated:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, _, info = env.step(action)
        episode_reward += reward
        states_log.append({
            'alpha_deg': obs[0],
            'altitude_ft': obs[4],
            'action': action
        })
    
    print(f"Episode reward: {episode_reward}")
    
    # Analyze stall events
    critical_alpha = 15
    stall_events = [s for s in states_log if s['alpha_deg'] > critical_alpha]
    print(f"Number of stall events during evaluation: {len(stall_events)}")
    if stall_events:
        avg_alt_loss = np.mean([s['altitude_ft'] - states_log[0]['altitude_ft'] for s in stall_events])
        print(f"Average altitude loss during stalls: {avg_alt_loss:.2f} ft")
    
    env.close()

if __name__ == "__main__":
    main()

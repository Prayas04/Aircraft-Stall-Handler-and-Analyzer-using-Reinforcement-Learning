import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO


class CustomStallRecoveryEnv(gym.Env):
    def __init__(self, dt=0.1):
        super(CustomStallRecoveryEnv, self).__init__()
        self.dt = dt  # Time step in seconds

        # Define action and observation spaces
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)  # elevator, throttle
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32
        )  # alpha, speed, pitch_rate, pitch_angle, altitude, throttle, roll

        # Task parameters
        self.critical_alpha = 15  # Critical angle of attack (degrees)
        self.safe_alpha = 10      # Safe angle of attack for recovery (degrees)
        self.recovery_counter = 0
        self.required_recovery_steps = 10  # Steps needed to consider recovered

        # Aircraft state variables
        self.state = None
        self.prev_alt = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Set initial conditions near stall
        self.state = np.array([
            np.random.uniform(12, 18),  # alpha (angle of attack)
            np.random.uniform(40, 60),  # speed (knots)
            np.random.uniform(-0.1, 0.1),  # pitch rate
            np.random.uniform(10, 20),  # pitch angle
            3280,  # altitude (feet)
            50,  # throttle (%)
            np.random.uniform(-5, 5)  # roll (degrees)
        ])
        self.prev_alt = self.state[4]
        self.recovery_counter = 0
        return self.state, {}

    def step(self, action):
        # Apply actions (elevator and throttle)
        elevator, throttle = action
        alpha, speed, pitch_rate, pitch_angle, altitude, _, roll = self.state

        # Update state based on simplified dynamics
        alpha += elevator * 0.5  # Elevator affects angle of attack
        speed += throttle * 0.1  # Throttle affects speed
        pitch_rate += elevator * 0.05  # Elevator affects pitch rate
        pitch_angle += pitch_rate * self.dt  # Pitch rate affects pitch angle
        altitude += speed * 0.1 * self.dt  # Speed affects altitude
        roll += elevator * 0.2  # Elevator slightly affects roll

        # Ensure state variables stay within reasonable bounds
        alpha = np.clip(alpha, -10, 20)
        speed = np.clip(speed, 0, 100)
        altitude = max(0, altitude)  # Altitude cannot go below 0
        roll = np.clip(roll, -30, 30)

        # Update the state
        self.state = np.array([alpha, speed, pitch_rate, pitch_angle, altitude, throttle * 100, roll])

        # Compute reward
        reward = 0
        if alpha > self.critical_alpha:
            reward -= (alpha - self.critical_alpha)  # Penalize high alpha
        reward += 0.1 * (altitude - self.prev_alt)  # Reward altitude preservation
        reward -= 0.01 * np.abs(elevator)  # Penalize large elevator inputs
        self.prev_alt = altitude

        # Check termination conditions
        terminated = False
        if altitude <= 0:  # Crash
            terminated = True
        elif alpha < self.safe_alpha:
            self.recovery_counter += 1
            if self.recovery_counter >= self.required_recovery_steps:
                terminated = True  # Successfully recovered
        else:
            self.recovery_counter = 0

        return self.state, reward, terminated, False, {}

    def close(self):
        """Clean up the environment."""
        self.state = None


def main():
    """Train and evaluate the stall recovery agent."""
    # Create environment
    env = CustomStallRecoveryEnv()
    
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
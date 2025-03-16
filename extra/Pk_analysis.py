import sys # Import the sys module
import os # Import the os module
from contextlib import contextmanager # Import the contextmanager class from the contextlib module
import numpy as np # Import the numpy module as np
import matplotlib.pyplot as plt # Import the matplotlib.pyplot module as plt

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'src'))

from functions import PatriotAirDefenseSystem # Import the PatriotAirDefenseSystem class from the functions module

# Context manager to suppress all console prints
@contextmanager
def suppress_stdout():
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout

# Override the class to disable file writes
class SilentPatriotSystem(PatriotAirDefenseSystem):
    def _write_results(self):
        pass  # Disable saving results
    
    def run_simulation(self):
        self.log_file = os.devnull  # Redirect logs to nowhere
        super().run_simulation()

if __name__ == "__main__":
    radar_data = 'radar_data.csv' # Define the name of the radar data file

    time_bool = False # Set the time_bool to True, so each time step is executed in 1 second

    rng_range = range(0, 10**4) # Set the range of random seeds to test
    Pk_range = np.arange(0.1,1.1,0.1) # Set the range of Pk values to test

    hostile_detected_array = np.zeros((len(rng_range),len(Pk_range))) # Initialize an array to store the number of detected hostiles
    hostile_identified_array = np.zeros((len(rng_range),len(Pk_range))) # Initialize an array to store the number of identified hostiles

    # Iterate over each random seed and Pk value to run simulations
    for Pk_index in range(len(Pk_range)):
        Pk = Pk_range[Pk_index] # Set the Probability of Kill (Pk) ratio to the current value
        for rng_index in range(len(rng_range)):
            rng_number = rng_range[rng_index] # Set the random seed to the current value
            patriot_system = SilentPatriotSystem(radar_data, Pk, time_bool, rng_number) # Create a new instance of the PatriotAirDefenseSystem class
            with suppress_stdout():
                patriot_system.run_simulation()
            
            hostile_detected_array[rng_index,Pk_index] = patriot_system.hostile_detected_count # Store the number of detected hostiles (all values are identical!)
            hostile_identified_array[rng_index,Pk_index] = patriot_system.hostile_identified_count # Store the number of identified hostiles

    simulated_pk_ratios = hostile_identified_array / hostile_detected_array # Calculate the simulated Pk ratios

    # Create histogram grid
    plt.figure(figsize=(14, 7))
    bins = np.arange(-0.05, 1.15, 0.1)  # Fixed bins for comparison
    
    # Plot histograms for each Pk value
    for idx, pk in enumerate(Pk_range):
        plt.subplot(2, 5, idx+1)  # 2x5 grid for 10 Pk values
        plt.hist(simulated_pk_ratios[:, idx], bins=bins, alpha=0.7)
        plt.axvline(pk, color='r', linestyle='--', linewidth=1.5)
        plt.title(f'Theoretical Pk: {pk:.2f}', fontsize=8)  
        plt.xlabel('Simulated Pk', fontsize=6) 
        plt.ylabel('Frequency', fontsize=6)
        plt.xlim(0, 1)
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.suptitle('Distribution of Simulated Pk Ratios vs Theoretical Values\n'
                 f'(Detection Count: {int(hostile_detected_array[0, 0])}, Trials per Pk: {len(rng_range)})', y=1.02,fontsize=10)
    plt.tight_layout()
    plt.savefig('extra/Pk_histograms.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Create summary statistics plot
    plt.figure(figsize=(7, 6))
    
    # Calculate distribution metrics
    means = np.mean(simulated_pk_ratios, axis=0)
    std_devs = np.std(simulated_pk_ratios, axis=0)
    
    # Plot theoretical vs simulated
    plt.errorbar(Pk_range, means, yerr=std_devs, fmt='o', 
                capsize=5, label='Simulated Pk ± 1σ')
    plt.plot([0, 1], [0, 1], 'r--', label='Perfect Agreement')
    plt.xlabel('Theoretical Pk')
    plt.ylabel('Simulated Pk')
    plt.title('Pk Verification: Theoretical vs Simulated Values\n'
             f'(Detection Count: {int(hostile_detected_array[0, 0])}, Trials per Pk: {len(rng_range)})')
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('extra/Pk_verification.png', dpi=300, bbox_inches='tight')
    plt.show()
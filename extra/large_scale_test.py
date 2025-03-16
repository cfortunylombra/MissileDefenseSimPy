import sys # Import the sys module
import os # Import the os module
import random # Import the random module

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'src'))

from functions import PatriotAirDefenseSystem # Import the PatriotAirDefenseSystem class from the functions module

class PatriotAirDefenseSystem(PatriotAirDefenseSystem):
    def __init__(self, radar_data_file, Pk, time_bool, rng_seed=None):
        """
        Initializes the PatriotAirDefenseSystem with the provided parameters.

        :param radar_data_file: Path to the radar data CSV file.
        :param pk: Probability of kill (identifying and neutralizing a detected hostile).
        :param time_bool: Boolean indicating whether to simulate each iteration in 1 second.
        :param rng_seed: Optional seed for the random number generator to ensure reproducibility.
        """
        random.seed(rng_seed)  # Set the random seed if provided for reproducibility
        
        self.Pk = Pk # Set the chance of a successful engagement, which is defined by the Probability of Kill (Pk) ratio
        self.time_bool = time_bool # Set the time_bool to True, so each time step is executed in 1 second
        self.rng_seed = rng_seed # Set the random seed to a specific value if rng_seed is provided
        self.hostiles_count = 0 # Initialize the count of total hostiles
        self.hostile_detected_count = 0 # Initialize the count of detected hostiles
        self.hostile_identified_count = 0 # Initialize the count of identified hostiles

        # Define the path to the radar_data.csv file
        self.radar_data_file = os.path.join(os.path.join('extra', radar_data_file))

        # Define paths for results and log files, incorporating the RNG seed if provided
        self.results_file = os.path.join('extra', f'large_scale_results_{rng_seed}.txt' if type(rng_seed)!= type(None) else 'large_scale_results.txt')
        self.log_file = os.path.join('extra', f'large_scale_log_{rng_seed}.txt' if type(rng_seed)!= type(None) else 'large_scale_log.txt')


# Generate random binary data
def generate_binary_line(num_strings=11, bits=7):
        """Generate a line of semicolon-separated binary strings"""
        return ";".join("".join(str(random.randint(0, 1)) for _ in range(bits)) for _ in range(num_strings))

if __name__ == "__main__":
    rng_number = 42 # Set the random seed to 42, so that the simulation is reproducible

    Pk = 0.8 # Set the chance of a successful engagement, which is defined by the Probability of Kill (Pk) ratio

    # Generate 10^4 lines of binary data
    number_lines = 10**4
    binary_data = [generate_binary_line() for _ in range(number_lines)]

    radar_data = 'binary_data.csv' # Define the name of the radar data file

    # To save to a file instead:
    with open(os.path.join('extra', radar_data), "w") as f:
        f.write("\n".join(binary_data))

    time_bool = False # Set the time_bool to True, so each time step is executed in 1 second

    # Call the simulation function
    patriot_system = PatriotAirDefenseSystem(radar_data, Pk, time_bool, rng_number)
    patriot_system.run_simulation()
import csv # Import the csv module in order to read the radar_data.csv file
import os # Import the os module in order to check if the radar_data.csv file exists
import random # Import the random module in order to generate random numbers
import time # Import the time module in order to measure the execution time of the simulation

class PatriotAirDefenseSystem:
    """
    Simulates a Patriot Air Defense System that processes radar data to detect and identify hostile targets.
    """

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
        self.radar_data_file = os.path.join(os.path.dirname(__file__), radar_data_file)

        # Define paths for results and log files, incorporating the RNG seed if provided
        self.results_file = os.path.join('output', f'results_{rng_seed}.txt' if type(rng_seed)!= type(None) else 'results.txt')
        self.log_file = os.path.join('output', f'log_{rng_seed}.txt' if type(rng_seed)!= type(None) else 'log.txt')

    def run_simulation(self):
        """
        Runs the simulation by reading radar data, processing each time step to detect and identify hostiles, and logging the results.
        """

        start_simulation_time = time.time() # Get the current time at the start of the simulation

        # Check if the radar data file exists
        if not os.path.exists(self.radar_data_file):
            print("ERROR: The radar_data.csv file does not exist!")
            return

        # Open the log file for writing
        with open(self.log_file, 'w') as log:
            message = "--CONSOLE LOG--"
            print(message)  # Print the header to the console
            print(message, file=log)  # Write header to the log file

            # Open and read the radar data file
            with open(self.radar_data_file, 'r') as file:
                reader = csv.reader(file, delimiter=';')  # Initialize CSV reader with ';' as delimiter

                # Iterate over each row in the radar data file, treating each as a time step
                for time_step, row in enumerate(reader, start=1):
                    start_time = time.time()  # Record the start time of the current time step

                    # Limit the simulation to 20 seconds
                    if time_step > 20:
                        break

                    self.hostiles_count += 1  # Increment the total number of hostiles processed
                    odd_count = 0  # Counter for odd decimal values
                    even_count = 0  # Counter for even decimal values

                    # Process each binary number in the current row
                    for binary_number in row:
                        binary_number = binary_number.strip()  # Remove any leading/trailing whitespace
                        # Check the last character to determine if the number is odd or even
                        if binary_number[-1] == '0':
                            even_count += 1
                        else:
                            odd_count += 1

                    # Determine if a hostile is detected based on the count of odd vs. even numbers
                    hostile_detected = odd_count > even_count
                    if hostile_detected:
                        self.hostile_detected_count += 1
                        # Determine if the detected hostile is identified based on the probability Pk
                        hostile_identified = random.uniform(0, 1) < self.Pk
                        if hostile_identified:
                            self.hostile_identified_count += 1

                    # Print the results of the current time step
                    message = f"\nTime step {time_step:2d}s: Radar data {row}"
                    print(message)  # Print the message to the console
                    print(message, file=log) # Write the message to the log file

                    if hostile_detected:
                        message = "Hostile detected & Missile launched! Engaging target..."
                        print(message)  # Print the message to the console
                        print(message, file=log)  # Write the message to the log file
                        if hostile_identified:
                            message = "Hostile identified & Missile neutralized the target."
                            print(message)  # Print the message to the console
                            print(message, file=log)  # Write the message to the log file
                        else:
                            message = "Hostile not identified."
                            print(message)  # Print the message to the console
                            print(message, file=log)  # Write the message to the log file
                    else:
                        message = "No hostile detected."
                        print(message)  # Print the message to the console
                        print(message, file=log)  # Write the message to the log file

                    # If time_bool is True, simulate real-time processing by delaying the loop
                    if self.time_bool:
                        time.sleep(0.995)  # Ensure each time step takes at least 1 second (slightly less to account for delay time)

            message = f"\n--Simulation completed in {round(time.time()-start_simulation_time,1)}s--"
            print(message)  # Print the total simulation time
            print(message, file=log)  # Write the total simulation time to the log file

        # After processing all time steps, write the summary results to the results file
        self._write_results()

    def _write_results(self):
        """
        Writes the summary of the simulation results to the results file.
        """
        with open(self.results_file, 'w') as results:
            print("--SIMULATION RESULTS--", file=results)
            print(f"Total Hostiles: {self.hostiles_count}", file=results)
            print(f"Hostiles Detected: {self.hostile_detected_count}", file=results)
            if self.hostiles_count > 0:
                detection_probability = (self.hostile_detected_count / self.hostiles_count) * 100
                print(f"Probability of Detection: {detection_probability:.2f}%", file=results)
            print(f"Hostiles Identified: {self.hostile_identified_count}", file=results)
            if self.hostiles_count > 0:
                identification_probability = (self.hostile_identified_count / self.hostiles_count) * 100
                print(f"Probability of Identification: {identification_probability:.2f}%", file=results)
            if self.hostile_detected_count > 0:
                simulated_pk_ratio = self.hostile_identified_count / self.hostile_detected_count
                print(f"Simulated Pk Ratio [#Identification/#Detection]: {simulated_pk_ratio:.2f}", file=results)

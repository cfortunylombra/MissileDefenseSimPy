import sys # Import the sys module
import os # Import the os module

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from functions import PatriotAirDefenseSystem # Import the PatriotAirDefenseSystem class from the functions module

if __name__ == "__main__":
    rng_number = 0 # Set the random seed to 0, so that the simulation is reproducible

    Pk = 0.8 # Set the chance of a successful engagement, which is defined by the Probability of Kill (Pk) ratio

    radar_data = 'radar_data.csv' # Define the name of the radar data file

    time_bool = True # Set the time_bool to True, so each time step is executed in 1 second

    # Call the simulation function
    patriot_system = PatriotAirDefenseSystem(radar_data, Pk, time_bool, rng_number)
    patriot_system.run_simulation()
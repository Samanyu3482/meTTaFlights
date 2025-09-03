def correct_flight_data(input_file_path, output_file_path):
    """
    Reads flight data from a file, corrects the month from 08 to 09 for the year 2025,
    and writes the corrected data to a new file.

    Args:
        input_file_path (str): The path to the input file (e.g., 'flights_updated.metta').
        output_file_path (str): The path to the output file where the corrected data will be saved.
    """
    try:
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            for line in infile:
                # Replace the specific occurrence of ' 08 ' after '2025'
                corrected_line = line.replace('(flight 2025 08 ', '(flight 2025 09 ')
                outfile.write(corrected_line)
        print(f"File successfully processed. Corrected data saved to: {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- How to use the script ---

# 1. Save this code as a Python file (e.g., 'correct_flights.py').
# 2. Make sure the 'flights_updated.metta' file is in the same directory as the script.
# 3. Run the script from your terminal using: python correct_flights.py

# Define the input and output file names
input_filename = 'flights_updated.metta'
output_filename = 'flights_corrected.metta'

# Call the function to perform the correction
correct_flight_data(input_filename, output_filename)
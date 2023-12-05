import os

def get_file_path(relative_path):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the desired file
    file_path = os.path.join(script_dir, relative_path)
    return file_path

get_file_path(relative_path='src_de_sample_data/10000_tracking.txt')
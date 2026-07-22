import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def setup_directories():
    """
    Creates the standardized directory structure for the project.
    Generates .gitkeep files to ensure empty directories are tracked.
    """
    directories = [
        "backend",
        "frontend",
        "ml",
        "data",
        "infra",
        "docs",
        "tests"
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        try:
            os.makedirs(dir_path, exist_ok=True)
            # Create a .gitkeep file so git tracks the empty directories
            gitkeep_path = os.path.join(dir_path, ".gitkeep")
            with open(gitkeep_path, "w") as f:
                pass
            logging.info(f"Successfully created directory and .gitkeep at: {dir_path}")
        except Exception as e:
            logging.error(f"Failed to create directory {dir_path}: {e}")

if __name__ == "__main__":
    logging.info("Starting directory setup...")
    setup_directories()
    logging.info("Directory setup completed.")

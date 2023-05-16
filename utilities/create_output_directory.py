import logging
import os

logger = logging.getLogger(__name__)


def create_output_directory(output_directory_path: str) -> None:

    if not os.path.exists(output_directory_path):
        logging.info(f"Creating output directory:'{output_directory_path}'!!")
        os.makedirs(output_directory_path)
    else:
        logging.info(f"Warning: Directory '{output_directory_path}' already exists.")

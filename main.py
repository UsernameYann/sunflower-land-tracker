import logging
from gui import main

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("sunflower_tracker.log"),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    setup_logging()
    main()
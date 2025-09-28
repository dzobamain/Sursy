# ./main.py

import sys
from util.log import logger

def main(argv) -> int:
    logger.info("Program started")
    print("Arguments:", argv)
    
    return -1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

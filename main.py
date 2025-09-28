import sys

def main(argv) -> int:
    print("Arguments:", argv)
    
    return -1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

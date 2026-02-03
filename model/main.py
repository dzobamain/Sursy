
def main(args: list[str]) -> int:
    return 0

if "__name__" == "__main__":
    exit_code: int = main(sys.argv)
    logger.info("Model ended")
    sys.exit(exit_code)
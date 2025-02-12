def get_version() -> str:
    """Returns the current version of the software."""
    version = "v0.0.1"
    return version

def main():
    """Main function to execute the program."""
    version = get_version()
    print(f"Current software version: {version}")

if __name__ == "__main__":
    main()

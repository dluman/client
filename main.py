import sys
import yaml
import pkg_resources

def reset_args() -> None:
    """ Resets command-line arguments from prior binaries """
    values = len(sys.argv) - 1
    while len(sys.argv) > 0:
        del sys.argv[values]
        values -= 1
    sys.argv.append("")

def load_config(filename: str = "config.yaml") -> dict:
    """ Loads the configuration file """
    with open("config.yaml", "r") as fh:
        config = yaml.safe_load(fh)
    return config

def discover_modules(modules: list = [], mod_group: str = "console_scripts") -> list[pkg_resources.EntryPoint]:
    """ Discovers entry points for system modules """
    # Provides a list of all modules with entry points
    pkgs = pkg_resources.iter_entry_points(group = mod_group)
    # Returns a list of the module entry point accompanied by args from config.yaml
    return [(pkg, modules[pkg.name]["args"]) for pkg in pkgs if pkg.name in modules]

def run_module(entry_point: pkg_resources.EntryPoint, arguments: list = []) -> None:
    """ Runs module based on reported entry point """
    # Apply any arguments provided in config
    for arg in arguments:
        if arg is not None:
            sys.argv.append(arg)
    # Load the entry point (removes need for importlib)
    entry = entry_point.load()
    # Run the program entry point
    entry()

def main():
    """ Main function """
    config = load_config()
    # Supply relevant modules to filter the list
    entry_points = discover_modules(modules = config["modules"])
    # For each discovered module, run the process
    for entry in entry_points:
        # Run the module by providing the module entry and the args
        run_module(entry_point = entry[0], arguments = entry[1])
        # Blast the previously-supplied args
        reset_args()

if __name__ == "__main__":
    main()

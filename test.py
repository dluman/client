import sys
import yaml
import types
import pkg_resources

def reset_args() -> None:
    values = len(sys.argv) - 1
    while len(sys.argv) > 0:
        del sys.argv[values]
        values -= 1
    sys.argv.append("")

def load_config(filename: str = "config.yaml") -> dict:
    modules = yaml.safe_load("config.yaml")
    with open("config.yaml", "r") as fh:
        config = yaml.safe_load(fh)
    for module in config["modules"]:
        config["modules"][module]["entry"] = ""
    return config

def discover_modules(modules: list = [], mod_group: str = "console_scripts") -> list[pkg_resources.EntryPoint]:
    pkgs = pkg_resources.iter_entry_points(group = mod_group)
    return [(pkg, modules[pkg.name]["args"]) for pkg in pkgs if pkg.name in modules]

def run_module(entry_point: pkg_resources.EntryPoint, arguments: list = []) -> None:
    for arg in arguments:
        if arg is not None:
            sys.argv.append(arg)
    entry = entry_point.load()
    entry()

def main():
    config = load_config()
    entry_points = discover_modules(modules = config["modules"])
    for entry in entry_points:
        print(entry)
        run_module(entry[0], entry[1])

if __name__ == "__main__":
    main()

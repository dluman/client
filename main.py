import yaml
import types
import pkg_resources

def load_config(filename: str = "config.yaml") -> dict:
    modules = yaml.safe_load("config.yaml")
    with open("config.yaml", "r") as fh:
        config = yaml.safe_load(fh)
    return config

def discover_modules(modules: list = [], mod_group: str = "console_scripts") -> list[pkg_resources.EntryPoint]:
    pkgs = pkg_resources.iter_entry_points(group = mod_group)
    return [pkg for pkg in pkgs if pkg.name in modules]

def run_module(module) -> None:
    entry = module.load()
    entry()

def main():
    config = load_config()
    entry_points = discover_modules(modules = config["modules"])
    for entry in entry_points:
        run_module(entry)

if __name__ == "__main__":
    main()

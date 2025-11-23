from config.config import Config
from system.xbrl_system import XBRLProcessingSystem

def main():
    config = Config.from_defaults()
    system = XBRLProcessingSystem(config)
    system.run()

if __name__ == "__main__":
    main()

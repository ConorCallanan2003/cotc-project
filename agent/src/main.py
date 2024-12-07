from agent.src.modules.StartUp.start_up import StartUp

def main():
    startUp = StartUp()
    logger = startUp.getLogger()
    logger.info("Agent has started successfully")

if __name__ == '__main__':
    main()

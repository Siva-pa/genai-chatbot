import logging

def get_logger():
    logger = logging.getLogger("chatbot")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("logs/app.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
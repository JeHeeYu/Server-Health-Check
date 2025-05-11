from dotenv import load_dotenv
import os

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')
SERVER_CODE = os.getenv('SERVER_CODE')

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD")
CONFIG_FILENAME = os.getenv("CONFIG_FILENAME", "config.js")

DSMC_BASE_PATH = os.getenv("DSMC_BASE_PATH")
DSMC_BASE_PORT = int(os.getenv("DSMC_BASE_PORT", 4000))

DSSNR_BASE_PATH = os.getenv("DSSNR_BASE_PATH")
DSSNR_BASE_PORT = int(os.getenv("DSSNR_BASE_PORT", 42000))

FEED_BASE_PATH = os.getenv("FEED_BASE_PATH")
FEED_BASE_PORT = int(os.getenv("FEED_BASE_PORT", 45000))
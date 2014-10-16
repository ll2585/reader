from gui import application

def main():
	try:
		application.run()
	finally:
		import os
		import app.constants as constants
		os.remove(constants.LOCK_FILE_PATH)

if __name__ == "__main__":
	main()
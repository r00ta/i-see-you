from iseeyou.application import Application
import os 

if __name__ == '__main__':
    appsettings_path = os.path.abspath("appsettings.json")
    application = Application(appsettings_path)
    application.main()

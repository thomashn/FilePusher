import sys

from app.main import Main

if __name__ == "__main__":
    m = Main()
    
    if len(sys.argv)>1:
        for arg in sys.argv[1:]:
            if arg == "setup":
                m.setup()
            else:
                print("Unknown option ("+arg+")! Options are: setup")
    else:
        m.run()

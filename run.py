import os
from app import app

# execute app__init__.py (development mode: debug=True)
if __name__ == "__main__":
        app.run(host=os.environ.get("IP"),
        port=os.environ.get("PORT"),
        debug=True)
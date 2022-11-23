import os
from app import create_app, mongo
from app.config import Config


app = create_app(Config)


# ------------------- #
#    Global Helper    #
# ------------------- #
@app.context_processor
def desserts_total():
    desserts_count = mongo.db.recipes.count
    return dict(desserts_count=desserts_count)


# execute app__init__.py
if __name__ == "__main__":
    app.run(
        host=os.getenv("IP"),
        port=os.getenv("PORT"),
        debug=os.getenv("DEBUG", False)
    )

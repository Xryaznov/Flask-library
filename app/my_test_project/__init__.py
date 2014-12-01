import os

from routes import app

app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data//mydb.db'

from models import db
db.init_app(app)

from admin import admin
admin.init_app(app)

import routes

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
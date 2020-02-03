from app.exts import app
from app.routes.insert import insert_route
from app.routes.export import export_route

app.register_blueprint(insert_route)
app.register_blueprint(export_route)
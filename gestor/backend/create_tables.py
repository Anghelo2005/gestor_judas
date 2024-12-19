from app import app, db

# Usar el contexto de la aplicación
with app.app_context():
    db.create_all()
    print("Tablas creadas exitosamente.")           
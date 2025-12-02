import os
from app import create_app, db

# Initialize database
app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Database tables created")

# Get port from Railway environment
port = int(os.environ.get("PORT", 5000))

# Start the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)

from Dev_BLOG import app, mongo_client

if __name__ == "__main__":
    try:
        # Test MongoDB connection
        mongo_client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Run Flask app
        app.run(debug=True)
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
from app import create_app

# Create application instance
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("  Osdag Structural Engineering Dashboard")
    print("  FOSSEE Screening Task 2026")
    print("=" * 60)
    print("\n  Starting server...")
    print("  Dashboard URL: http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    # Run the application
    app.run(debug=True, host='127.0.0.1', port=5000)

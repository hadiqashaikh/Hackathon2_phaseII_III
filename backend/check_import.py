print("Testing backend import...")
try:
    import main
    print("SUCCESS: Backend loaded!")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

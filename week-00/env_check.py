import os

key = os.environ.get("TRAINING_NAME", "(not set)")
print(f"TRAINING_NAME={key}")

import subprocess
import sys
import time
import requests

def run_streamlit():
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app/main.py"])

def run_fastapi():
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"])

def check_fastapi_health(retries=5, delay=2):
    for _ in range(retries):
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("FastAPI backend is running and healthy.")
                return True
        except requests.RequestException:
            pass
        time.sleep(delay)
    print("Failed to connect to FastAPI backend.")
    return False

if __name__ == "__main__":
    print("Starting FastAPI backend...")
    fastapi_process = run_fastapi()
    
    if check_fastapi_health():
        print("Starting Streamlit frontend...")
        run_streamlit()
    else:
        print("Error: FastAPI backend failed to start. Exiting.")
        fastapi_process.terminate()
        sys.exit(1)

    try:
        fastapi_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        fastapi_process.terminate()
        sys.exit(0)
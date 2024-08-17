import subprocess
import sys
import time
import requests
import os
import socket

def find_free_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
        port += 1

def run_streamlit(port):
    os.environ['STREAMLIT_SERVER_PORT'] = str(port)
    # Redirect stderr to suppress the warning
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app/main.py"], 
                            stderr=subprocess.DEVNULL)

def run_fastapi(port):
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", str(port)])

def check_fastapi_health(port, retries=5, delay=2):
    for _ in range(retries):
        try:
            response = requests.get(f"http://localhost:{port}/health")
            if response.status_code == 200:
                print(f"FastAPI backend is running and healthy on port {port}.")
                return True
        except requests.RequestException:
            pass
        time.sleep(delay)
    print(f"Failed to connect to FastAPI backend on port {port}.")
    return False

if __name__ == "__main__":
    fastapi_port = find_free_port(8000)
    streamlit_port = find_free_port(8501)

    # Set environment variables
    os.environ["PORT"] = str(fastapi_port)
    os.environ["BACKEND_URL"] = f"http://localhost:{fastapi_port}"

    print(f"Starting FastAPI backend on port {fastapi_port}...")
    fastapi_process = run_fastapi(fastapi_port)
    
    if check_fastapi_health(fastapi_port):
        print(f"Starting Streamlit frontend on port {streamlit_port}...")
        streamlit_process = run_streamlit(streamlit_port)
        
        print(f"Application is running.")
        print(f"Access FastAPI at http://localhost:{fastapi_port}")
        print(f"Access Streamlit at http://localhost:{streamlit_port}")
    else:
        print("Error: FastAPI backend failed to start. Exiting.")
        fastapi_process.terminate()
        sys.exit(1)

    try:
        fastapi_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        sys.exit(0)
        
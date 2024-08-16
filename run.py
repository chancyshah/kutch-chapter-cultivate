import subprocess
import sys

def run_streamlit():
    print("Starting Streamlit...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])

def run_fastapi():
    print("Starting FastAPI...")
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", "43093"])

if __name__ == "__main__":
    import threading

    fastapi_thread = threading.Thread(target=run_fastapi)
    streamlit_thread = threading.Thread(target=run_streamlit)

    fastapi_thread.start()
    streamlit_thread.start()

    fastapi_thread.join()
    streamlit_thread.join()

import subprocess
import sys

def run_fastapi():
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8001"])

def run_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])

if __name__ == "__main__":
    import threading

    fastapi_thread = threading.Thread(target=run_fastapi)
    streamlit_thread = threading.Thread(target=run_streamlit)

    fastapi_thread.start()
    streamlit_thread.start()

    fastapi_thread.join()
    streamlit_thread.join()

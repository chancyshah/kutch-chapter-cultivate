import subprocess
import sys

def run_streamlit():
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8002"])

def run_fastapi():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py", "--server.port", "8504", "--server.runOnSave", "false"])

if __name__ == "__main__":
    import threading

    fastapi_thread = threading.Thread(target=run_fastapi)
    streamlit_thread = threading.Thread(target=run_streamlit)

    fastapi_thread.start()
    streamlit_thread.start()

    fastapi_thread.join()
    streamlit_thread.join()

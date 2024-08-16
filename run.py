import subprocess
import sys

def run_streamlit():
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")

def run_fastapi():
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8001"])
    except subprocess.CalledProcessError as e:
        print(f"Error running FastAPI: {e}")


if __name__ == "__main__":
    import threading

    fastapi_thread = threading.Thread(target=run_fastapi)
    streamlit_thread = threading.Thread(target=run_streamlit)

    fastapi_thread.start()
    streamlit_thread.start()

    fastapi_thread.join()
    streamlit_thread.join()

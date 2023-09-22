import subprocess
import atexit

def start_redis():
    global redis_process
    redis_process = subprocess.Popen(["redis-server"])
    print("Redis server started.")

def stop_redis():
    global redis_process
    if redis_process:
        redis_process.terminate()
        print("Redis server stopped.")

atexit.register(stop_redis)
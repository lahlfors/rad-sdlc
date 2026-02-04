import sys
import subprocess
import json
import threading
import time

def read_output(process):
    for line in iter(process.stdout.readline, ''):
        if line.strip():
            try:
                msg = json.loads(line)
                print(f"Server sent: {json.dumps(msg, indent=2)}")
            except:
                print(f"Server sent (raw): {line.strip()}")
    print("Server output ended")

def main():
    cmd = [sys.executable, "skills/adk_cheatsheet/server.py"]
    print(f"Starting server: {' '.join(cmd)}")
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr, # Pass stderr through
        text=True,
        bufsize=1
    )
    
    # Start reader thread
    t = threading.Thread(target=read_output, args=(process,), daemon=True)
    t.start()
    
    # 1. Initialize
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "verifier", "version": "0.1.0"}
        }
    }
    print(f"Sending initialize: {json.dumps(init_req)}")
    process.stdin.write(json.dumps(init_req) + "\n")
    process.stdin.flush()
    
    time.sleep(1)
    
    # 2. Initialized notification
    initialized_notif = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    print(f"Sending initialized: {json.dumps(initialized_notif)}")
    process.stdin.write(json.dumps(initialized_notif) + "\n")
    process.stdin.flush()

    time.sleep(0.5)

    # 3. List Tools
    list_tools_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    print(f"Sending tools/list: {json.dumps(list_tools_req)}")
    process.stdin.write(json.dumps(list_tools_req) + "\n")
    process.stdin.flush()
    
    time.sleep(1)
    
    # Terminate
    print("Terminating server...")
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()

if __name__ == "__main__":
    main()

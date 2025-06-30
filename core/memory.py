# Simulated memory manager# memory_keeper.py
import json
import os
import time
import traceback

LOG_FILE = "memory_audit.log"
ERROR_LOG = "memory_errors.log"

def audit_agent_memory(self, agent):
    try:
        if not agent:
            raise ValueError("No agent provided to memory audit.")
        
        log(f"Auditing memory for agent: {agent.name}")

        if hasattr(agent, 'persona') and 'error' in agent.persona:
            log_warning(f"[Audit] Persona load error for {agent.name}: {agent.persona['error']}")

        if hasattr(agent, 'lessons') and not agent.lessons:
            log_warning(f"[Audit] No lessons found for {agent.name}.")

        # Future expansion: check persistent memory store
        # Example: verify SQLite, Chroma, or JSONL logs

    except Exception as e:
        log_error(f"[Memory Audit Failure] {str(e)}")
        log_error(traceback.format_exc())

def log(self, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | {message}\n")
    print(f"[MEMORY] {message}")

def log_warning(self, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | WARNING: {message}\n")
    print(f"[MEMORY][WARNING] {message}")

def log_error(self, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(ERROR_LOG, "a") as f:
        f.write(f"{timestamp} | ERROR: {message}\n")
    print(f"[MEMORY][ERROR] {message}")

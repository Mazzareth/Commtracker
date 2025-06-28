import os
import sys
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger("updater")
logging.basicConfig(level=logging.INFO)

def run_cmd(cmd, cwd=None):
    """Run a shell command, capture output, raise exception on failure."""
    logger.info(f"Running command: {cmd} (cwd={cwd or os.getcwd()})")
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode != 0:
        logger.error(f"Command failed: {cmd}\nstdout: {result.stdout}\nstderr: {result.stderr}")
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {cmd}\n{result.stderr}")
    logger.info(f"Command output: {result.stdout.strip()}")
    return result.stdout.strip()

def is_update_available():
    """Return True if remote HEAD differs from local HEAD, else False."""
    try:
        run_cmd("git fetch")
        local = run_cmd("git rev-parse HEAD")
        remote = run_cmd("git rev-parse @{u}")
        logger.info(f"Local HEAD: {local}, Remote HEAD: {remote}")
        return local != remote
    except Exception as e:
        logger.error(f"Failed to check for updates: {e}")
        return False

def perform_update():
    """
    If update available, performs:
    - git pull --rebase (falls back to merge if fails)
    - pip install -r requirements.txt (if exists)
    - python manage.py migrate
    - restarts process
    Logs robustly, propagates readable errors.
    """
    try:
        if not is_update_available():
            logger.info("No update available.")
            return "No update available."
        try:
            logger.info("Attempting git pull --rebase...")
            run_cmd("git pull --rebase")
        except Exception as rebase_err:
            logger.error(f"git pull --rebase failed: {rebase_err}, falling back to git pull (merge)...")
            run_cmd("git pull")

        reqs = Path("requirements.txt")
        if reqs.exists():
            logger.info("Installing requirements.txt...")
            run_cmd(f"{sys.executable} -m pip install -r requirements.txt")
        else:
            logger.info("requirements.txt not found, skipping pip install.")

        logger.info("Applying database migrations...")
        run_cmd(f"{sys.executable} manage.py migrate")

        logger.info("Restarting Python process to load new code...")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        logger.error(f"Update failed: {e}")
        raise RuntimeError(f"Update failed: {e}")
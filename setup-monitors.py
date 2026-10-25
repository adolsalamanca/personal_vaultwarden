#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "uptime-kuma-api==1.2.1",
# ]
# ///

"""
Creates Uptime Kuma monitors and Telegram notifications from monitors.json.
Reads credentials from .env. Safe to re-run: skips anything already configured.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path


def load_env(path=".env"):
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip()
    return env


def wait_for_uptime_kuma(url, retries=30, delay=2):
    for i in range(retries):
        try:
            urllib.request.urlopen(f"{url}/api/entry-page", timeout=3)
            return True
        except Exception:
            print(f"Waiting for Uptime Kuma... ({i + 1}/{retries})")
            time.sleep(delay)
    return False


def main():
    env = load_env()
    tailnet = env.get("TAILNET_DOMAIN", "")
    username = env.get("UPTIME_KUMA_USER", "")
    password = env.get("UPTIME_KUMA_PASSWORD", "")
    telegram_token = env.get("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = env.get("TELEGRAM_CHAT_ID", "")
    hc_ping_url = env.get("HC_PING_URL", "")

    if not username or not password:
        print("Error: UPTIME_KUMA_USER and UPTIME_KUMA_PASSWORD must be set in .env")
        sys.exit(1)

    url = "http://127.0.0.1:3001"

    if not wait_for_uptime_kuma(url):
        print("Uptime Kuma not reachable. Is it running?")
        sys.exit(1)

    with open("monitors.json") as f:
        config = json.load(f)

    from uptime_kuma_api import UptimeKumaApi, MonitorType, DockerType, NotificationType

    api = UptimeKumaApi(url)
    try:
        # First-time setup creates the admin account; login works on subsequent runs
        try:
            api.login(username, password)
            print("Logged in.")
        except Exception:
            api.setup(username, password)
            api.login(username, password)
            print("Admin account created and logged in.")

        # Set up Telegram notification
        if telegram_token and telegram_chat_id:
            existing_notifs = api.get_notifications()
            if any(n["name"] == "Telegram" for n in existing_notifs):
                print("Telegram notification already configured.")
            else:
                api.add_notification(
                    name="Telegram",
                    type=NotificationType.TELEGRAM,
                    isDefault=True,
                    applyExisting=True,
                    telegramBotToken=telegram_token,
                    telegramChatID=telegram_chat_id,
                )
                print("Telegram notification created.")
        else:
            print("Skipping Telegram: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")

        # Set up Docker host (needed for container monitors)
        docker_host_id = None
        existing_hosts = api.get_docker_hosts()
        local = next((h for h in existing_hosts if h["name"] == "Local Docker"), None)
        if local:
            docker_host_id = local["id"]
            print("Docker host already configured.")
        else:
            result = api.add_docker_host(
                name="Local Docker",
                dockerType=DockerType.SOCKET,
                dockerDaemon="/var/run/docker.sock",
            )
            docker_host_id = result["id"]
            print(f"Docker host created (id={docker_host_id}).")

        existing = {m["name"] for m in api.get_monitors()}

        for monitor in config["monitors"]:
            name = monitor["name"]
            if name in existing:
                print(f"Skipping (already exists): {name}")
                continue

            mtype = monitor["type"]

            if mtype == "http":
                resolved_url = (
                    monitor["url"]
                    .replace("${TAILNET_DOMAIN}", tailnet)
                    .replace("${HC_PING_URL}", hc_ping_url)
                )
                api.add_monitor(
                    type=MonitorType.HTTP,
                    name=name,
                    url=resolved_url,
                    interval=monitor.get("interval", 60),
                )
                print(f"Created HTTP monitor: {name} → {resolved_url}")

            elif mtype == "docker_container":
                api.add_monitor(
                    type=MonitorType.DOCKER,
                    name=name,
                    docker_container=monitor["container"],
                    docker_host=docker_host_id,
                    interval=monitor.get("interval", 30),
                )
                print(f"Created Docker monitor: {name}")

    finally:
        api.disconnect()


if __name__ == "__main__":
    main()

import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
QUEUE_DIR = ROOT / "queue"
STATE_DIR = ROOT / "state"
COMMANDS_PATH = QUEUE_DIR / "commands.json"
STATE_PATH = STATE_DIR / "latest_state.json"
HOST = "127.0.0.1"
PORT = 8765


def ensure_files() -> None:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    if not COMMANDS_PATH.exists():
        write_json(COMMANDS_PATH, {"commands": []})

    if not STATE_PATH.exists():
        write_json(
            STATE_PATH,
            {
                "lastHeartbeatUtc": None,
                "workspaceChildren": [],
                "workspaceChildCount": 0,
                "lastResults": [],
            },
        )


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "CodexRobloxBridge/0.1"

    def _send(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            return {}

        raw = self.rfile.read(content_length)
        if not raw:
            return {}

        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send(
                200,
                {
                    "ok": True,
                    "serverTimeUtc": utc_now(),
                },
            )
            return

        if self.path == "/commands":
            queue = read_json(COMMANDS_PATH)
            commands = queue.get("commands", [])
            write_json(COMMANDS_PATH, {"commands": []})
            self._send(
                200,
                {
                    "commands": commands,
                    "count": len(commands),
                },
            )
            return

        if self.path == "/state":
            self._send(200, read_json(STATE_PATH))
            return

        self._send(404, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:
        if self.path == "/enqueue":
            body = self._read_body()
            incoming = body.get("commands", [])

            if not isinstance(incoming, list):
                self._send(400, {"ok": False, "error": "commands_must_be_array"})
                return

            queue = read_json(COMMANDS_PATH)
            commands = queue.get("commands", [])
            commands.extend(incoming)
            write_json(COMMANDS_PATH, {"commands": commands})

            self._send(
                200,
                {
                    "ok": True,
                    "queued": len(incoming),
                    "pending": len(commands),
                },
            )
            return

        if self.path == "/state":
            body = self._read_body()
            current = read_json(STATE_PATH)
            current.update(body)
            current["lastHeartbeatUtc"] = utc_now()
            write_json(STATE_PATH, current)
            self._send(200, {"ok": True})
            return

        self._send(404, {"ok": False, "error": "not_found"})

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    ensure_files()
    server = ThreadingHTTPServer((HOST, PORT), BridgeHandler)
    print(f"Codex Roblox Bridge listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()

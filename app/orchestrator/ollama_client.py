import json
import urllib.request
import urllib.error


class OllamaClient:
    def __init__(self, base_url="http://localhost:11434/api"):
        self.base_url = base_url.rstrip("/")

    def chat(self, model, messages, temperature=0.2):
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))

            return result["message"]["content"]

        except urllib.error.URLError as error:
            raise RuntimeError(f"Ollama connection failed: {error}") from error

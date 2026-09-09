import sys
import json
from client import ORSetCRDT

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "test_or_set":
        s = ORSetCRDT()
        s.add("item1", "tag1")
        return {"items": s.read()}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == "__main__":
    main()

from http.server import BaseHTTPRequestHandler
import json
import os
import random
import time
import urllib.parse
from http import cookies

# Configuration
LOCK_DURATION_SECONDS = 30 * 60  # 30 minutes
COOKIE_NAME = "boa_session"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Load Answers
        # On Vercel, the file system is read-only. We need to find the absolute path.
        # This script is in /api/answer.py, so answers.json is in ../answers.json
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'answers.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                answers_data = json.load(f)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error loading answers: {str(e)}".encode())
            return

        # 2. Parse Query Params
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        author_only = query_params.get('author_only', ['false'])[0].lower() == 'true'

        # 3. Check Cookies for existing session
        cookie_header = self.headers.get('Cookie')
        current_answer = None
        current_timestamp = time.time()
        is_cached = False

        if cookie_header:
            c = cookies.SimpleCookie()
            c.load(cookie_header)
            if COOKIE_NAME in c:
                try:
                    # value format: "timestamp|json_string"
                    cookie_val = urllib.parse.unquote(c[COOKIE_NAME].value)
                    ts_str, ans_json = cookie_val.split('|', 1)
                    ts = float(ts_str)

                    # Check if lock is still valid
                    if current_timestamp - ts < LOCK_DURATION_SECONDS:
                        current_answer = json.loads(ans_json)
                        current_timestamp = ts # Keep original timestamp
                        is_cached = True
                except:
                    # Invalid cookie data, ignore
                    pass

        # 4. Generate new answer if needed
        if not current_answer:
            available_answers = answers_data
            if author_only:
                available_answers = [ans for ans in answers_data if 'author_en' in ans]
            
            if not available_answers:
                current_answer = {"zh": "...", "en": "...", "fr": "..."}
            else:
                current_answer = random.choice(available_answers)
            
            # Reset timestamp to now
            current_timestamp = time.time()

        # 5. Prepare Response
        response_data = {
            'answer': current_answer,
            'timestamp': current_timestamp,
            'is_cached': is_cached
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        
        # 6. Set/Update Cookie if it was a new answer (or to refresh expiry)
        # We store: "timestamp|json_dump"
        if not is_cached:
            val_to_store = f"{current_timestamp}|{json.dumps(current_answer)}"
            # URL encode to be safe in headers
            val_encoded = urllib.parse.quote(val_to_store)
            
            c = cookies.SimpleCookie()
            c[COOKIE_NAME] = val_encoded
            c[COOKIE_NAME]['path'] = '/'
            c[COOKIE_NAME]['max-age'] = LOCK_DURATION_SECONDS
            # samesite=Lax is good practice
            c[COOKIE_NAME]['samesite'] = 'Lax'
            
            # Write the Set-Cookie header
            # SimpleCookie.output() returns "Set-Cookie: name=value..."
            # We strip "Set-Cookie: " to pass just the value to send_header
            cookie_output = c.output(header='').strip()
            self.send_header('Set-Cookie', cookie_output)

        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

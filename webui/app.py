import re
import subprocess
import sys
from urllib.parse import urlparse

from flask import Flask, render_template, request

app = Flask(__name__)

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')
XSSTRIKE_PATH = '/app/xsstrike.py'


def is_valid_target(url):
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)


def run_scan(url):
    try:
        result = subprocess.run(
            [sys.executable, XSSTRIKE_PATH, '-u', url, '--skip'],
            capture_output=True,
            text=True,
            timeout=90,
        )
        return ANSI_ESCAPE.sub('', result.stdout + result.stderr)
    except subprocess.TimeoutExpired:
        return 'Scan timed out after 90 seconds.'


@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    target_url = ''
    if request.method == 'POST':
        target_url = request.form.get('target_url', '').strip()
        if not is_valid_target(target_url):
            output = 'Enter a valid http:// or https:// URL.'
        else:
            output = run_scan(target_url)
    return render_template('index.html', output=output, target_url=target_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

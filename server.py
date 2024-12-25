# server.py

from flask import Flask, request, jsonify, send_from_directory
import subprocess
import tempfile
import json
import ast
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/api/lint', methods=['POST'])
def lint_code():
    data = request.get_json()
    code = data.get('code', '')

    # Write code to a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        # Run PyLint on the temporary file with JSON output
        result = subprocess.run(['pylint', tmp_path, '--output-format=json'], capture_output=True, text=True)
        lint_output = result.stdout

        # Parse JSON output
        errors = json.loads(lint_output) if lint_output else []

        # Format errors and warnings
        formatted_errors = []
        for item in errors:
            formatted_errors.append({
                'message': item.get('message'),
                'line': item.get('line'),
                'type': item.get('type'),  # 'convention', 'refactor', 'warning', 'error', 'fatal'
            })

        return jsonify({
            'errors': [e for e in formatted_errors if e['type'] == 'error'],
            'warnings': [w for w in formatted_errors if w['type'] == 'warning']
        })
    except Exception as e:
        return jsonify({'errors': [], 'warnings': [], 'exception': str(e)}), 500
    finally:
        # Clean up the temporary file
        os.remove(tmp_path)

@app.route('/api/validate', methods=['POST'])
def validate_code():
    data = request.get_json()
    code = data.get('code', '')
    messages = []
    success = True

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return jsonify({'success': False, 'messages': [f'Syntax Error: {e.msg} (Line {e.lineno})']})

    # Initialize flags
    has_return_five = False
    has_return_ten = False

    # Traverse the AST to find function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == 'return_five':
                # Check if the function returns 5
                for stmt in node.body:
                    if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Constant) and stmt.value.value == 5:
                        has_return_five = True
            elif node.name == 'return_ten':
                # Check if the function returns 10
                for stmt in node.body:
                    if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Constant) and stmt.value.value == 10:
                        has_return_ten = True

    if not has_return_five:
        success = False
        messages.append('Function "return_five" that returns 5 is missing or incorrect.')

    if not has_return_ten:
        success = False
        messages.append('Function "return_ten" that returns 10 is missing or incorrect.')

    return jsonify({'success': success, 'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)

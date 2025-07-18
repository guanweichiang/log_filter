from flask import Flask, render_template, request, jsonify
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'log', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return jsonify({"success": True, "content": content})
    return jsonify({"success": False, "message": "Invalid file"})

@app.route('/filter', methods=['POST'])
def filter_content():
    import re

    data = request.get_json()
    full_text = data.get('content', '')
    filters = data.get('filters', [])
    case_sensitive = data.get('case_sensitive', False)

    flags = 0 if case_sensitive else re.IGNORECASE

    try:
        regexes = [re.compile(f, flags) for f in filters]
    except re.error as e:
        return jsonify({"success": False, "message": f"Regex Error: {e}"})

    result_lines = []

    for idx, line in enumerate(full_text.splitlines(), start=1):
        if all(r.search(line) for r in regexes):
            result_lines.append({'line_number': idx, 'text': line})

    return jsonify({"success": True, "filtered": result_lines})


if __name__ == '__main__':
    app.run(debug=True)
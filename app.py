from flask import Flask, render_template, request, jsonify
import os

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
    data = request.get_json()
    full_text = data.get('content', '')
    filters = data.get('filters', [])

    result_lines = []
    if filters:
        def line_match(line):
            return all(f in line for f in filters)

        for idx, line in enumerate(full_text.splitlines(), start=1):
            if line_match(line):
                result_lines.append({'line_number': idx, 'text': line})
    else:
        for idx, line in enumerate(full_text.splitlines(), start=1):
            result_lines.append({'line_number': idx, 'text': line})

    return jsonify({"filtered": result_lines})

if __name__ == '__main__':
    app.run(debug=True)
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
    # 取得 filter 陣列，預期為字串列表
    filters = data.get('filters', [])
    if filters:
        def line_match(line):
            # 若行中至少包含其中一個 filter，即回傳 True
            return all(f in line for f in filters)
        filtered_lines = "\n".join(line for line in full_text.splitlines() if line_match(line))
    else:
        filtered_lines = full_text
    return jsonify({"filtered": filtered_lines})

if __name__ == '__main__':
    app.run(debug=True)

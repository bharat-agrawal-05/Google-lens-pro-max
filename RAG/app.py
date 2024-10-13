from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.json
    query = data['query']
    
    try:
        # Run the main.py script with the query as an argument
        result = subprocess.check_output(['python', 'RAGpipeline.py', query], universal_newlines=True)
        return jsonify({'result': result.strip()})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
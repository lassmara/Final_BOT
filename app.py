from flask import Flask, request, jsonify, render_template
import train_qa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('run.html')

@app.route('/guide')
def guide():
    return render_template('guidePage.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    answer = train_qa.Q_A(question)
    return jsonify({'result': answer})

if __name__ == '__main__':
    app.run(debug=True)

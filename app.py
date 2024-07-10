from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    input_text = request.form['inputText']
    
    output_text = run_python_script(input_text)
    return output_text

@app.route('/process_discourse', methods=['POST'])
def process_discourse():
    simplified_text = request.form['output']
    
    try:
        save_simplified_text(simplified_text)
        result_text, relation_list = run_discourse_script(simplified_text)
        output_data = {
            'result_text': result_text,
            'relation': relation_list
        }
        return jsonify(output_data)
    except Exception as e:
        return str(e), 500

    # return jsonify(output_data)

def save_simplified_text(simplified_text):
    try:
        with open('sentence_output.txt', 'w') as file:
            file.write(simplified_text)
    except Exception as e:
        raise Exception(f"Error saving simplified text: {e}")

def run_python_script(input_text):  
    script_path = 'sentence_subparts.py'

    with open('sentence_input.txt', 'w') as result_file:
        result_file.write(input_text)

    result = subprocess.run(['/usr/bin/python3', script_path, input_text], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Subprocess failed with error: {result.stderr}")

    with open('sentence_output.txt', 'r') as result_file:
        result_text = result_file.read()

    return result_text

def run_discourse_script(input_text):
    script_path = 'discourse_Sent.py'

    with open('sentence_output.txt', 'w') as result_file:
        result_file.write(input_text)

    result_process = subprocess.run(['/usr/bin/python3', script_path], capture_output=True, text=True)

    if result_process.returncode != 0:
        raise Exception(f"Subprocess failed in discourse with error: {result_process.stderr}")

    with open('relation.txt', 'r') as result_file:
        relation = result_file.read()
    
    with open('sentence_output.txt', 'r') as result_file:
        result_text = result_file.read()

    relation_list = relation.split(',')
    return result_text, relation_list

@app.route('/run_discourse_sent', methods=['POST'])
def run_discourse_sent():
    # Run the discourse_sent.py script
    script_path = 'discourse_Sent.py'
    result = subprocess.run(['/usr/bin/python3', script_path], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Subprocess failed in discourse_sent with error: {result.stderr}")

    # Read and return the output of the script
    with open('output_discource.txt', 'r') as result_file:
        result_text = result_file.read()

    return result_text

@app.route('/save_to_file', methods=['POST'])
def save_to_file():
    data = request.json
    modified_text = data.get('text', '')

    with open('output_discource.txt', 'w') as file:
        file.write(modified_text)

    return jsonify({'message': 'Text saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)

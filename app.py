from flask import Flask, request, jsonify
import json
from discource_sent_2 import process_discourse,parse_output
from re_code import create_dynamic_regex
# Initialize Flask app
app = Flask(__name__)

@app.route('/discourse_process', methods=['POST'])
def process_json():
    try:
        # Parse input JSON
        input_data = request.json
        sentences = input_data.get("sentences", [])
        
        if not sentences:
            return jsonify({"error": "No sentences provided"}), 400
        
        # Convert JSON to the required format
        line = '\n'.join([f"{sentence['sentence_id']} {sentence['sentence']}" for sentence in sentences])
        all_ids=[sentence['sentence_id'] for sentence in sentences]
        regex_pattern = create_dynamic_regex(all_ids)
        project_id = sentences[0]["project_id"]
        lines = line.split('\n')
        
        # Process discourse
        output, hindi_dict = process_discourse(lines,regex_pattern)
        # print(output,'output')
        # Final parsing
        output_string = " ".join(output)
        final_output = parse_output(hindi_dict, output_string, project_id)
        print(final_output,'final')
        # Return the result
        return jsonify(final_output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
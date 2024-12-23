import re
import json
# Provided output string
output_string = ' <S_id=1> गांव मे दो भाई थे </S_id> णण् <S_id=2b> सब परेशान हो जाते था </S_id> [ आवश्यकतापरिणाम <S_id=2a> गांव मे कुछ भी घटित होता </S_id> ] परिणाम <S_id=3> उनके माता पिता उनसे बहत नाराज रहते थे </S_id> '
# # Discourse marker dictionary
discourse_marker_dict = {'5b': 'तो', '3': 'लेकिन', '4': 'इसके विपरीत', '6': 'इस कारण', '7': 'जबकि'}

# List of discourse markers
discourse_markers = ['समुच्चय.अतिरिक्त','समुच्चय.अलावा','समुच्चय.BI_1','समुच्चय.समावेशी','समुच्चय.nahIM_1','समुच्चय x',"समुच्चय", 'विरोधी_द्योतक',"विरोधी", 'समुच्चय', 'अन्यत्र', 'व्यभिचार', 'कार्यकारण', 'आवश्यकतापरिणाम', 'परिणाम', 'उत्तर्काल']

# Create a regex pattern dynamically from the list of discourse markers
discourse_pattern = r'(' + '|'.join(map(re.escape, discourse_markers)) + ')'

# Regular expression pattern to match sentence IDs with any format
sentence_id_pattern = r'<S_id=([^>]+)>'  # Match everything inside <S_id= >


def find_left_part(relation_parts):
    for segmt in relation_parts:
        if '[' in segmt:
            return segmt 

# Parsing function to create the desired output format
def parse_output(discourse_marker_dict, output_string,project_id):
    # print(output_string,'strrrrrrr')
    result = []
    
    # Extract all sentences with their IDs
    sentences = re.findall(r'<S_id=([^>]+)>(.*?)</S_id>', output_string)
    sentence_dict = {sent_id.strip(): sent_text.strip() for sent_id, sent_text in sentences}

    # Update discourse_marker_dict with any missing IDs, setting them to "None"
    for sent_id in sentence_dict.keys():
        if sent_id not in discourse_marker_dict:
            discourse_marker_dict[sent_id] = "None"

    # Replace 'णण्' with 'समुच्चय' for processing
    output_string = output_string.replace('णण्', 'समुच्चय')

    # Now split based on the discourse markers
    relation_parts = re.split(discourse_pattern, output_string)
    
    # Loop through relations to form output
    for i in range(len(relation_parts) - 1):
        left_part = relation_parts[i].strip()
        # print(left_part,'partt')
        if ']' in left_part:
            left_part = find_left_part(relation_parts)
        relation = relation_parts[i + 1].strip()  # Get the relation marker
        right_part = relation_parts[i + 2].strip() if (i + 2) < len(relation_parts) else ""

        # Extract sentence IDs from left and right parts
        left_sent_ids = re.findall(sentence_id_pattern, left_part)
        right_sent_ids = re.findall(sentence_id_pattern, right_part)

        # Handling different relations
        if left_sent_ids and right_sent_ids:
            sent_1_id = left_sent_ids[-1]  # Last ID from left part
            sent_2_id = right_sent_ids[0]   # First ID from right part
            sent_1 = sentence_dict.get(sent_1_id, '')
            sent_2 = sentence_dict.get(sent_2_id, '')

            # Determine discourse marker and relation type
            # if 'आवश्यकतापरिणाम' in relation:
            #     discourse_marker = discourse_marker_dict.get(sent_1_id, "None")
                # discourse_marker = 'अगर/यदि/यद्यपि'
            # else:
            discourse_marker = discourse_marker_dict.get(sent_2_id, "None")
            relation_type = "समुच्चय" if 'समुच्चय' in relation else "विरोधी" if 'विरोधी' in relation else "व्यभिचार"

            # Append to the result list
            if discourse_marker == 'तो' and relation=='समुच्चय':
                discourse_marker='None'
            elif discourse_marker in ("णोने","None") and relation=='आवश्यकतापरिणाम':
                discourse_marker = discourse_marker.replace('णोने','अगर')
            elif discourse_marker in ("णोने"):
                discourse_marker = discourse_marker.replace('णोने','None')
            # print(relation,type(relation),'rrrrrrrrrr')
            
            if 'आवश्यकतापरिणाम' != relation and 'व्यभिचार' !=relation:
                result.append({
                    "project_id": project_id,
                    "discourse_marker": discourse_marker,
                    "discourse_relation": relation,
                    "sent_1": sent_1,
                    "sent_1_id": sent_1_id,  # Keep as string
                    "sent_2": sent_2,
                    "sent_2_id": sent_2_id,  # Keep as string
                    "head_sent_id": "None",
                    "dependent_sent_id": "None"
                })
            else:
                result.append({
                    "project_id": project_id,
                    "discourse_marker": discourse_marker,
                    "discourse_relation": relation,
                    "sent_1": sent_1,
                    "sent_1_id": sent_1_id,  # Keep as string
                    "sent_2": sent_2,
                    "sent_2_id": sent_2_id,  # Keep as string
                    "head_sent_id":sent_1_id,
                    "dependent_sent_id": sent_2_id
                })
            
        elif left_sent_ids and not right_sent_ids:
            sent_1_id = left_sent_ids[-1]
            sent_1 = sentence_dict.get(sent_1_id, '')

            # Handle dependent sentences with discourse markers
            head_sent_id = sent_1_id  # Use last sent ID from left as head
            dependent_sent_id = sent_1_id  # The same since there's no right sentence
            result.append({
                "project_id": project_id,
                "discourse_marker": discourse_marker_dict.get(dependent_sent_id, "None"),
                "discourse_relation": relation,  # Assumed as default for left alone
                "head_sent": sent_1,
                "head_sent_id": head_sent_id,
                "dependent_sent": "None",
                "dependent_sent_id": "None"
            })

    return result

# Generate output
# parsed_output = parse_output(discourse_marker_dict, output_string)
# parsed_output = parse_output(discourse_marker_dict, output_string)

# # Write the parsed output to a JSON file
# with open('parsed_output.json', 'w', encoding='utf-8') as json_file:
# print(json.dumps(parsed_output, ensure_ascii=False, indent=4))
# # Print the parsed output
# if parsed_output:  # Check if the output is not empty
#     print(parsed_output,'output')
#     # for item in parsed_output:
#     #     print(item)
# else:
#     print("No output generated.")

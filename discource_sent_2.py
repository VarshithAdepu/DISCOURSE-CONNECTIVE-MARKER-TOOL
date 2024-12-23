from discourse_mapped_rel import discourseMarkerParser
from discourse_mapped_rel import USR
import json
from wxconv import WXC
import re
from api_output_3 import *
# Create an instance of the USR class
usr_instance = USR()
updated_list = []
hindi_dict = {}
# Now you can access multi_word_markers, markers, and discourse_relation dictionaries
multi_word_markers = usr_instance.multi_word_markers
markers = usr_instance.markers
discourse_relation = usr_instance.discourse_relation

def combine_lines_with_prefix(lines):
    # Example usage
    # combine_lines_with_prefix('sentence_output.txt', "कि")
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     lines = file.readlines()
    # print("ast",lines)
    new_lines = []

    current_id = ""
    current_text = ""

    for line in lines:
        columns = line.split(maxsplit=1)
        if len(columns) >= 2:
            current_id, current_text = columns
            current_text = current_text.strip()  
            # print(current_id)
        else:
            current_text += line.strip() 

        if current_text.startswith('कि') and 'अगर' not in current_text:
            previous_line = new_lines[-1].rstrip(" ।")
            # print(previous_line)
            if ('इतना'or'इतनी'or'इतने') not in previous_line:
            # if "a " in previous_line:
                # mod_previous_line = previous_line.replace("a", "")
                new_lines[-1] = previous_line.rstrip(' ।\n') + " " + current_text.strip() + "\n"
            else:
                new_lines.append(f"{current_id} {current_text}\n")
        else:
            new_lines.append(f"{current_id} {current_text}\n")
    # print(parse_discourse_lines(new_lines),'parseeeeee')
    print(new_lines,'newlines')
    return parse_discourse_lines(new_lines)


def convert_to_hindi(input_text):
    wx = WXC(order='wx2utf', lang='hin')
    hindi_text = wx.convert(input_text)
    return hindi_text

def convert_to_eng(input_text):
    if not isinstance(input_text, str):
        input_text = str(input_text)
    wx = WXC(order='utf2wx', lang='hin')
    hindi_text = wx.convert(input_text)
    return hindi_text
def read_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()
    
def get_ids(sent):
    
    pattern1 = re.compile(r'(\w+_\w+_\w+_\w+-\w+_\d+[a-zA-Z]?)')
    match1 = re.search(pattern1, sent)
    
    pattern2 = re.compile(r"(\d+[a-z]?)")
    match2 = re.search(pattern2, sent)

    if match1:
        return match1.group(1)
    elif match2:
        return match2.group(1)
    else:
        return None

def to_check_same_ids(sent):
    # if '=' and'>' in sent.split()[0]:
    #     pattern = r'=(.*?)[a-zA-Z]?>'
    #     match1 = re.search(pattern, sent)
    #     if match1:
    #         return match1.group(1)
    #     else:
    #         return None
    # else:
    #     pattern = r'(.*?)[a-zA-Z]?'

    #     # Find the match for string1
    #     match1 = re.search(pattern, sent)
    #     if match1:
    #         return match1.group(1)
    #     else:
    #         return None
    pattern1 = r"(\w+_\w+_\w+_\w+-\w+_\d+)"
    match1 = re.search(pattern1, sent)
    pattern2 = r"(\d+)"
    match2 = re.search(pattern2, sent)

    if match1:
        return match1.group(1)
    elif match2:
        return match2.group(1)
    else:
        return None

def find_conjunction(sentence):
    conjunctions = ["अगर", "यदि", "यद्यपि"]
    for conj in conjunctions:
        if conj in sentence:
            return conj
    return None  # Return None if no conjunction is found

list1=[]
def parse_discourse_lines(lines):
    l1 = []
    l2 = []
    store = []
    # i=0
    # while i<len(lines)-1:
    for i in range(len(lines)-1):
        # print(i)
        sent1 = lines[i].strip()
        sent2 = lines[i + 1].strip()
        
        id1 = to_check_same_ids(sent1)
        id2 = to_check_same_ids(sent2)
        
        id_1 = get_ids(sent1)
        id_2 = get_ids(sent2)
        

        if id1==id2:
            # Check if "अगर" is present in sent2
            if ('कि अगर') not in sent2 and "अगर" in sent1 or "यदि" in sent1 or "यद्यपि" in sent1 :

                m = i
                sent1=lines[m].strip()
                sent2=lines[m+1].strip()
                if "तो" not in sent2 :
                    discourseMarkerParser.replaced_words_dict[id_1]= str(find_conjunction(sent1))
                    output_line=process_sentences(sent1, sent2, id_1, id_2).replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
                    lines = replace_values_in_list(lines,sent1, sent2,output_line)
                    return process_discourse(lines)
                    
                elif "तो" in sent2 :
                    return if_to(lines)
                
            elif ("अगर" in sent2 or "यदि" in sent2 or "यद्यपि" in sent2) :
                # Process sentences until "तो" is encountered
                sent3 = lines[i + 2].strip() if i + 2 < len(lines) else None
                # print("varSh",sent3)

                if sent3 and "तो" not in sent3 :
                    # print("2")
                    print(sent2)
                    id1 = to_check_same_ids(sent2)
                    id2 = to_check_same_ids(sent3)
                    
                    id_1 = get_ids(sent2)
                    id_2 = get_ids(sent3)
                    
                    if id1 == id2:
                        discourseMarkerParser.replaced_words_dict[id_1]= str(find_conjunction(sent1))
                        # print(discourseMarkerParser.replaced_words_dict,'ciiiiiiiiii')
                        output_line = process_sentences(sent2, sent3, id_1, id_2).replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
                        lines = replace_values_in_list(lines,sent2, sent3,output_line)
                        return process_discourse(lines)
                        
                elif sent3 and  "तो" in sent3 :
                    # print("nn")
                    return if_to(lines)
                
            elif "तो" in lines[i+1] :
                return if_to(lines)
            # discourseMarkerParser.replaced_words_dict[id_1]= str(find_conjunction(sent1))
            output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '').replace("यद्यपि ",'').replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
            lines = replace_values_in_list(lines,sent1,sent2,output_line)
            if len(lines) > 2:
                return process_discourse(lines)
            else:
                output_line=output_line.replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
                output_line = process_output_line(output_line)
            
        # i+=1
    i=0
    while i<len(lines)-1:
        sent1 = lines[i].strip()
        sent2 = lines[i + 1].strip()
        # print(sent1)
        # print("vv")
        if not sent2:
            continue
        
        id_1 = get_ids(sent1)
        id_2 = get_ids(sent2)

        # Check if "अगर" is present in sent2
        if "अगर" in sent2 or "यदि" in sent2 or "यद्यपि" in sent2 :
            # Process with the next sentence
            sent3 = lines[i + 2].strip() if i + 2 < len(lines) else None
            discourseMarkerParser.replaced_words_dict[id_2]= str(find_conjunction(sent1))
            output_line_next = process_sentences(sent2, sent3, id_2, get_ids(sent3)) if sent3 else None
            lines = replace_values_in_list(lines,sent2,sent3,output_line_next)

            # Process with the current sentence and the next one
            discourseMarkerParser.replaced_words_dict[id_1]= str(find_conjunction(sent1))
            output_line_current = process_sentences(sent1, output_line_next , id_1, get_ids(output_line_next)) if output_line_next else None
            lines = replace_values_in_list(lines,sent1,output_line_next,output_line_current)

            return process_discourse(lines)

    # Normal processing if "अगर" is not present in sent2
        # discourseMarkerParser.replaced_words_dict[id_1]= str(find_conjunction(sent1))
        output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '').replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
        lines = replace_values_in_list(lines,sent1,sent2,output_line)
        if len(lines) > 2:
            if i == 0:
                output_line = output_line.replace('अगर ', '').replace('यदि ', '').replace("यद्यपि ",'')
                lines = replace_values_in_list(lines,sent1,sent2,output_line)
                return process_discourse(lines)
            else:
                output_line = output_line.strip().replace('अगर ', '').replace('यदि ', '')
                lines = replace_values_in_list(lines,sent1,sent2,output_line)
                return process_discourse(lines)
        else:
            output_line = output_line.replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
            lines = replace_values_in_list(lines,sent1,sent2,output_line)
    # return lines
        
def replace_values_in_list(lines, value1, value2, output):
    """
    Replaces two consecutive values in a list with a specified output, handling newlines.
    
    Parameters:
        lst (list): The list to search through.
        value1 (str): The first value to search for.
        value2 (str): The second value to search for.
        output (str): The output value to replace the two values with.
    
    Returns:
        list: The modified list with the values replaced, if found.
    """
    global updated_list
    # Strip whitespace and newlines from value1 and value2 for correct comparison
    value1 = value1.strip()
    value2 = value2.strip()
    
    i = 0
    while i < len(lines) - 1:  # Ensure there's a next element to compare to
        if lines[i].strip() == str(value1) and lines[i+1].strip() == str(value2):
            lines[i:i+2] = [output]
            # del lines[i+1]
            print(lines,'lines')
            updated_list = lines
            break
        i += 1  # Move to the next element
    return lines

def if_to(lines):
    store = []
    l1 = []
    l2 = []
    # with open(file_path, 'r') as file:
    #     lines = file.readlines()
    # print(lines)
    for i in range(len(lines)):
        
        sent3 = lines[i].strip()
        if "तो" in sent3:
            print("Processing sentence with 'तो' at line:", i)
            b = i + 1
            while b < len(lines):
                sent4 = lines[b].strip() if b<len(lines) else None
                if sent4 and 'तो' not in sent4 and to_check_same_ids(sent3) == to_check_same_ids(sent4):
                    # print("Processing sentences following 'तो' until IDs match at line:", b)
                    discourseMarkerParser.replaced_words_dict[get_ids(sent3)] = str(find_conjunction(sent3))
                    output_line_current = process_sentences(sent3, sent4,get_ids(sent3),get_ids(sent4)).replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
                    lines = replace_values_in_list(lines,sent3,sent4,output_line_current)
                    return process_discourse(lines)
                    #     return process_discourse(file_path)
                else:
                    a = i - 1
                    sent1 = lines[a].strip()
                    sent2 = lines[a + 1].strip()
                    id1 = to_check_same_ids(sent1)
                    id2 = to_check_same_ids(sent2)
                    # print("Processing sentences preceding 'तो' until IDs match at line:", a)
                    while a >= 0 and id1 == id2:
                        # print("pk")
                        # print(lines[a])
                        
                        id_1 = get_ids(sent1)
                        id_2 = get_ids(sent2)
                        discourseMarkerParser.replaced_words_dict[id_1] = str(find_conjunction(sent1))
                        output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '').replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
                        lines = replace_values_in_list(lines, sent1, sent2, output_line)
                        return process_discourse(lines)
                    else:
                        break
            
            else:
                a = i - 1
                print("Processing sentences preceding 'तो' until IDs match at line:", a)
                while a >= 0:
                    # print("kk")
                    # print(lines[a])
                    sent1 = lines[a].strip()
                    sent2 = lines[a + 1].strip()
                    id1 = to_check_same_ids(sent1)
                    id2 = to_check_same_ids(sent2)
                    id_1 = get_ids(sent1)
                    id_2 = get_ids(sent2)
                    if id1 == id2:
                        discourseMarkerParser.replaced_words_dict[id_1] = str(find_conjunction(sent1))
                        output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '').replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>', ' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]')
                        lines = replace_values_in_list(lines,sent1,sent2,output_line)
                        return process_discourse(lines)
                    else:
                        break        
                b += 1
                
    
        
def process_output_line(output_line):
    
    modified_lines = [output_line.replace(' </S_id> </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id>', ' </S_id>').replace(' </S_id> </S_id> ] </S_id> </S_id>',' </S_id> ]').replace(' </S_id> ] </S_id>',' </S_id> ]').replace('णण् ', '\n')]
    return modified_lines
    # with open(file_path_1, 'w', encoding='utf-8') as output_file:
    #     output_file.writelines(modified_lines)

        
def get_discourse_from_word(sentence):
       
       sent=convert_to_eng(sentence)
       sent = sent.split()
    #    print('ss',sent)
       s = sent[0]

       for i in range(len(sent) - 1):
           if s in markers or s in multi_word_markers:
                # print(s)
                return discourse_relation[s]
           else:
               s += ' ' + sent[i+1]
       return "-1"


def process_sentences(sent1, sent2, id_1, id_2):
    global hindi_dict
    try:
        parser = discourseMarkerParser(sent1, sent2)
    except IndexError:
        return None

    results = parser.get_results()
    hindi_sent1 = convert_to_hindi(results[0]).strip()
    disc_relation = convert_to_hindi(results[1]).strip()
    hindi_sent2 = convert_to_hindi(results[2]).strip()
    relation = results[3]
    wx_converter = WXC(order='wx2utf', lang='hin')
    hindi_dict = {key: wx_converter.convert(value) for key, value in relation.items()}
    print(hindi_dict,'relation')
    h1 = sent1.split()
    h2 = sent2.split()
    # print(disc_relation)
    # print(hindi_sent1,'kkk')
    # print(hindi_sent2)
    # print(id_2)

    if ('इतना'or'इतनी'or'इतने') in hindi_sent1:
        disc_relation='परिणाम'
        # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation} <S_id={id_2}> {hindi_sent2} </S_id>"
        output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + " " + ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
    
    elif 'ना केवल' in hindi_sent1 and 'बल्कि' in hindi_sent2:
        disc_relation='समुच्चय'
        discourseMarkerParser.replaced_words_dict[id_2] = 'ना केवल'
        hindi_sent1 = hindi_sent1.replace('ना केवल ','')
        hindi_sent2 = hindi_sent2.replace('बल्कि ','')
        # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.BI_1 <S_id={id_2}> {hindi_sent2} </S_id>"
        output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".BI_1" + ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        
    elif h2[1]=='नहीं' and h2[2]=='तो':
        # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.nahIM_1 <S_id={id_2}> {hindi_sent2} </S_id>"
        output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".nahIM_1" + ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '

    elif results[1] in parser.discourse_pos and parser.discourse_pos[results[1]] == "0":
        output_line = ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> ' + '[ ' + disc_relation + ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> '+'] '
        # output_line=output_line.replace(' </S_id> </S_id> ] </S_id> </S_id> ]',' </S_id> ]')
        # print('oo',output_line)

    elif results[1] =="samuccaya x"  and parser.discourse_pos[results[1]] == 'x':
        if h2[1]=='इसके' and h2[2]=='अलावा' and '?' not in hindi_sent2 and 'नहीं' not in hindi_sent2:
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.BI_1 <S_id={id_2}> {hindi_sent2} </S_id>"
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".BI_1" + ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        elif h2[1]=='इसके' and (h2[2]=='साथ-साथ' or h2[2]=='साथ' and h2[3]=='साथ'):
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.समावेशी <S_id={id_2}> {hindi_sent2} </S_id>"
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".समावेशी" + ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        elif h2[1]=='इसके' and (h2[2]=='अतिरिक्त'):
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.समावेशी <S_id={id_2}> {hindi_sent2} </S_id>"
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".अतिरिक्त" + ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        elif h2[1]=='इसके' and (h2[2]=='अलावा'):
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.समावेशी <S_id={id_2}> {hindi_sent2} </S_id>"
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".अलावा" + ' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        elif results[1] == "samuccaya x":
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.x <S_id={id_2}> {hindi_sent2} </S_id>"
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".x" +' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        else:
            # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.x <S_id={id_2}> {hindi_sent2} </S_id>"
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".x" +' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
    else:
        if h2[1]=='इसके' and h2[2]=='विपरीत':
            # output_line = f"<S_id={id_1}> {hindi_sent1} </S_id> {disc_relation}.विपरीत <S_id={id_2}> {hindi_sent2} </S_id>"
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation + ".विपरीत" +' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '

        elif h2[1]=='तथा':
            disc_relation=convert_to_hindi(get_discourse_from_word(hindi_sent2))
            if disc_relation!='-1':
                output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation +' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        
            else:
                output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation +' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        else:
            output_line = ' <S_id='+id_1+'>' + " " + hindi_sent1 + ' </S_id> ' + disc_relation +' <S_id='+id_2+'>' + " " + hindi_sent2 + ' </S_id> '
        
    return output_line

def convert_json_to_discourse_input(json_input):
    sentences = json_input["sentences"]
    discourse_input = ""
    project_id = json_input["sentences"][0]["project_id"]
    for sentence in sentences:
        sentence_id = sentence["sentence_id"]
        text = sentence["sentence"]
        discourse_input += f"{sentence_id}\"{text}\"\n"

    return discourse_input.strip(),project_id

def process_discourse(lines):
    # lines = read_lines(file_path)
    if len(lines) < 2:
        line = lines[0].split()
        id_val = get_ids(lines[0].strip())
        hindi_sent = convert_to_hindi(lines[0].strip())
        # print(f"<S_id={id_val}> {hindi_sent} </S_id>")
        print(hindi_sent,'hindiiiiiii')
        return hindi_sent
    else:
        combine_lines_with_prefix(lines)
        return updated_list,hindi_dict

if __name__ == "__main__":
    # file_path='sentence_output.txt'
    # file_path_1='output_discource.txt'
    # wx = WXC(order='wx2utf', lang='hin')
#     input = '''1 मनु ने एक दिन बनारस से दिल्ली तक पैदल जाने की योजना बनाई ।
# 2a पर उसे ये मालूम नहीं था ।
# 2b कि उस दिन बारिश होगी ।
# 2c या नहीं होगी ।
# 3 इसलिये उसने एक दस ईंच का छाता ले लिया ।
# 4a मनु सुबह सात बजे चलना शुरू किया तभी अचानक तुफान आ गया ।
# 4b और छाता उड़ गया ।'''
    input = {
    "sentences": [
        {
            "project_id": 1,
            "sentence_id": "1",
            "sentence": "मनु ने एक दिन बनारस से दिल्ली तक पैदल जाने की योजना बनाई ।"
        },
        {
            "project_id": 1,
            "sentence_id": "2a",
            "sentence": "पर उसे ये मालूम नहीं था ।"
        },
        {
            "project_id": 1,
            "sentence_id": "2b",
            "sentence": "कि उस दिन बारिश होगी ।"
        },
        {
            "project_id": 1,
            "sentence_id": "2c",
            "sentence": "या बारिश नहीं होगी ।"
        },
        {
            "project_id": 1,
            "sentence_id": "3",
            "sentence": "इसलिये उसने एक दस ईंच का छाता ले लिया ।"
        },
        {
            "project_id": 1,
            "sentence_id": "4a",
            "sentence": "मनु सुबह सात बजे चलना शुरू किया |"
        },
        {
            "project_id": 1,
            "sentence_id": "4b",
            "sentence": "तभी अचानक तुफान आ गया ।"
        },
        {
            "project_id": 1,
            "sentence_id": "4c",
            "sentence": "और छाता उड़ गया ।"
        }
    ]
}
    # lines = input.split('\n')
    # Convert JSON to the string format used by process_discourse
    line = '\n'.join([f"{sentence['sentence_id']} {sentence['sentence']}" for sentence in input['sentences']])
    # Assuming all sentences belong to the same project_id
    project_id = input["sentences"][0]["project_id"]
    # lines,project_id = convert_json_to_discourse_input(input)
    print(line,'llllll')
    lines = line.split('\n')
    output,hindi_dict = process_discourse(lines)
    print("Final output from the last call:", output,hindi_dict)
    output_string = " ".join(output)
    final = parse_output(hindi_dict,output_string,project_id)
    with open('parsed_output.json', 'w', encoding='utf-8') as json_file:
        json.dump(final, json_file, ensure_ascii=False, indent=4)
    print(final,'output')
    print(output,'output')
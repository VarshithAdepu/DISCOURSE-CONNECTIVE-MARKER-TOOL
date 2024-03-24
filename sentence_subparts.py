import string
import CONSTANTS
import sys
import re
import os
from wxconv import WXC

def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    # Format for log message
    print(f'[{logtype}] : {mssg}')
    if logtype == 'ERROR':
        sys.exit()

def read_input(file_path):
    '''Returns dict with key - sentence_id and value - sentence for data given in file'''
    log(f'File ~ {file_path}')
    try:
        with open(file_path, 'r') as file:
            input_data = {}
            lines = file.readlines()
            for i in range(len(lines)):
                lineContent = lines[i].strip()
                if lineContent == '':
                    break
                else:
                    sentence_info = lineContent.split(' ', 1)
                    key = sentence_info[0]
                    value = sentence_info[1].strip()
                    input_data[key] = value
            log('File data read.')
    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    return input_data


def clean(word, inplace=''):
    """
    Clean concept words by removing numbers and special characters from it using regex.
    >>> clean("kara_1-yA_1")
    'karayA'
    >>> clean("kara_1")
    'kara'
    >>> clean("padZa_1")
    'pada'
    >>> clean("caDZa_1")
    'caDa'

    """
    newWord = word
    if 'dZ' in word:  # handling words with dZ/jZ -Kirti - 15/12
        newWord = word.replace('dZ', 'd')
    elif 'jZ' in word:
        newWord = word.replace('jZ', 'j')
    elif 'DZ' in word:
        newWord = word.replace('DZ', 'D')

    return newWord

def validate_sentence(sentence):
    #sentence not empty - return True
    #Regular expression pattern to match any non-digit character
    pattern = r'\D'
    if not len(sentence) or not re.search(pattern, sentence):
        return False

    return True

def sanitize_input(sentence):

    wx_format = WXC(order="utf2wx", lang="hin")
    generate_wx_text = wx_format.convert(sentence)
    clean_wx_text = ""
    tokens = generate_wx_text.strip().split()
    for word in tokens:
        clean_wx_text = clean_wx_text + clean(word) + " "

    clean_wx_text.strip()
    hindi_format = WXC(order="wx2utf", lang="hin")
    clean_hindi_text = hindi_format.convert(clean_wx_text).strip()

    if clean_hindi_text.endswith('.'):
        clean_hindi_text = clean_hindi_text[:-1] + " " + "।"

    return clean_hindi_text

def write_output(dictionary, file_path, manual_evaluation):
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            line = f""
            letter = ''
            for i in range(len(value)):
                item = value[i]
                # if item in manual_evaluation:
                #     TAG = 'Manual evaluation'
                # else:
                #     TAG = 'None'
            
                if len(value) > 1:
                    letter = string.ascii_lowercase[i]
                    
                if len(item) > 0:
                    if item.endswith(',') or item.endswith('।'):
                        line += key + letter + "  " + item[:-1] + " ।" + "\n"  # add poornaviram
                    elif item.endswith('?'):
                        line += key + letter + "  " + item[:-1] + " ?" + "\n"  # add '?' in the output
                    elif item.endswith('!'):
                        line += key + letter + "  " + item[:-1] + " !" + "\n"  # add '!' in the output
                    else:
                        line += key + letter + "  " + item + " ।" + "\n"
            
            file.write(line)
    log("Output file written successfully")

def is_prev_word_verb(parser_output, index):
    try:
        with open(parser_output, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if i == index:
                    lineContent = lines[i].strip().split()
                    if len(lineContent) > 0 and (lineContent[3] == 'VM' or lineContent[3] == 'VAUX'):
                        return True

    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    return False

def get_index_of_word(words, value):
    index = -1
    for i in range(len(words)):
        if words[i] == value:
            index = i
            break
    return index

def get_word_at_index(words, index):
    word = ""
    for i in range(len(words)):
        if i == index:
            word = words[i]
            break
    return word

def get_POS_by_index(parser_output, index):
    tag = ''
    try:
        with open(parser_output, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                row = lines[i].strip().split()
                if len(row) == 10 and row[0] == str(index + 1):
                    tag = row[3]
                    break
            return tag

    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()

def get_dep_by_index(parser_output, index):
    dep = ''
    try:
        with open(parser_output, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                row = lines[i].strip().split()
                if len(row) == 10 and row[0] == str(index+1):
                    dep = row[7]
                    break
            return dep

    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()

import CONSTANTS  # Assuming CONSTANTS is the name of your module

def breakPairConnective(sentence, manual_evaluation):
    # This function return list of sentences if a paired connective is found else returns an empty list
    simpler_sentences = []
    BREAK_SENTENCE = False

    # Tokenize the sentence by splitting it into words
    tokens = sentence.split()
    # token = tokens[0]

    # Iterate through the tokens to find connectives and split the sentence
    for i in range(len(tokens)-1):
        token = tokens[i]
        # Check if the token is a paired-connective
        if token in CONSTANTS.COMPLEX_CONNECTIVES:
            pair_value_lst = CONSTANTS.COMPLEX_CONNECTIVES[token]
            for pair_value in pair_value_lst:
                if pair_value in sentence:
                    pair_value = pair_value.strip().split()[0]
                    index_of_pair_value = get_index_of_word(tokens, pair_value)
                    if not (index_of_pair_value == -1):
                        get_parser_output(sentence)
                        
                        # Replace "तब" with "तो" if it is present along with "अगर" or "यदि"
                        if (token == 'अगर' or token == 'यदि') and 'तब' in tokens:
                            tokens[tokens.index('तब')] = 'तो'
                            sent1 = tokens[:index_of_pair_value]
                            sent2 = tokens[index_of_pair_value+i:]

                        # elif (token == 'ना केवल') and 'बल्कि' in tokens:
                        #     sent1 = tokens[:index_of_pair_value]
                        #     sent2 = tokens[index_of_pair_value:]

                        if is_prev_word_verb(CONSTANTS.PARSER_OUTPUT, index_of_pair_value - 1):
                            # if token=='ना केवल':
                            #     index_of_pair_value = index_of_pair_value
                            #     sent1 = tokens[:index_of_pair_value]
                            #     sent2 = tokens[index_of_pair_value:]
                            #     simpler_sentences.append(" ".join(sent1))
                            #     simpler_sentences.append(" ".join(sent2))
                            # else:
                            # tokens.pop(i)
                            index_of_pair_value = index_of_pair_value
                            sent1 = tokens[:index_of_pair_value]
                            sent2 = tokens[index_of_pair_value:]
                            simpler_sentences.append(" ".join(sent1))
                            simpler_sentences.append(" ".join(sent2))
                            BREAK_SENTENCE = True
                            break
                        else:
                            manual_evaluation.append(sentence)
            if BREAK_SENTENCE:
                break
    return simpler_sentences


def breakSimpleConnective(sentence, manual_evaluation):
    # This function returns a list of sentences if a simple connective is found, else returns an empty list
    simpler_sentences = []
    # Tokenize the sentence by splitting it into words
    tokens = sentence.split()
    for i in range(len(tokens)):
        token = tokens[i]

        # 'नहीं तो' is a simple connective
        if token == 'नहीं':
            following_word = get_word_at_index(tokens, i + 1)
            if following_word == 'तो':
                token = 'नहीं तो'
        if token == 'फिर':
            following_word = get_word_at_index(tokens, i + 1)
            if following_word == 'भी':
                token = 'फिर भी'

        # Check if the token is a connective
        if token in CONSTANTS.SIMPLE_CONNECTIVES:
            if token in ('और', 'एवं','या'):
                get_parser_output(sentence)
                token_POS = get_POS_by_index(CONSTANTS.PARSER_OUTPUT, i)
                token_dep = get_dep_by_index(CONSTANTS.PARSER_OUTPUT, i)
                get_parser_output(sentence)

                if token_POS == 'CC' and (token_dep == 'main' or token_dep== 'ccof') and is_prev_word_verb(CONSTANTS.PARSER_OUTPUT, i - 1):
                    if tokens[0]=='अगर' :
                        sent1 = tokens[:i]
                        tokens.insert(i+1,'अगर')
                        sent2 = tokens[i:]  # Fixed the indexing issue here
                    else:
                        sent1 = tokens[:i]
                        sent2 = tokens[i:]

                    # Check for the condition
                    # if ('इतना'or'इतनी'or'इतने') in sent1 and 'कि' in sent2:
                    #     manual_evaluation.append(sentence)
                    # else:
                    simpler_sentences.append(" ".join(sent1))
                    simpler_sentences.append(" ".join(sent2))
                    break
                elif i > 1:
                    manual_evaluation.append(sentence)
            elif token == 'कि':
                get_parser_output(sentence)
                token_POS = get_POS_by_index(CONSTANTS.PARSER_OUTPUT, i)
                token_dep = get_dep_by_index(CONSTANTS.PARSER_OUTPUT, i)
                tags = get_parser_output(sentence)

                if (token_POS == 'CC' and (token_dep == 'k2' or token_dep == 'rs') and is_prev_word_verb(CONSTANTS.PARSER_OUTPUT, i - 1)):
                    sent1 = tokens[:i]
                    sent2 = tokens[i:]

                    # Check for the condition
                    # if ('इतना'or'इतनी'or'इतने') in sent1:
                    #     manual_evaluation.append(sentence)
                    # else:
                    if 'VM' in tags and ('इतना'or'इतनी'or'इतने') not in sent1:
                        vm_index = tags.index('VM')
                        if 'यह' not in sent1:  # Check if "यह" is already in the sentence
                            sent1.insert(vm_index, 'यह')
                    elif 'VAUX' and ('इतना'or'इतनी'or'इतने') not in sent1:
                        prev_vm_index = get_index_of_word(sent1, 'VAUX')
                        if 'यह' not in sent1:  # Check if "यह" is already in the sentence
                            sent1.insert(prev_vm_index, 'यह')
                    sent1.append('।')  # Add Poornaviram at the end
                    simpler_sentences.append(" ".join(sent1))
                    simpler_sentences.append(" ".join(sent2))
                    break
                elif i > 1:
                    manual_evaluation.append(sentence)
            elif token in ('बल्कि','लेकिन','किंतु','परंतु','वरन्'):
                get_parser_output(sentence)
                token_POS = get_POS_by_index(CONSTANTS.PARSER_OUTPUT, i)
                token_dep = get_dep_by_index(CONSTANTS.PARSER_OUTPUT, i)
                if is_prev_word_verb(CONSTANTS.PARSER_OUTPUT, i - 1):
                    if tokens[0]=='अगर':
                        sent1 = tokens[:i]
                        tokens.insert(i+1,'अगर')
                        sent2 = tokens[i:]  # Fixed the indexing issue here
                    else:
                        sent1 = tokens[:i]
                        sent2 = tokens[i:]
                    # Check for the condition
                    # if ('इतना'or'इतनी'or'इतने') in sent1 and 'कि' in sent2:
                    #     manual_evaluation.append(sentence)
                    # else:
                    simpler_sentences.append(" ".join(sent1))
                    simpler_sentences.append(" ".join(sent2))
                    break
                elif i > 1:
                    manual_evaluation.append(sentence)

            else:
                get_parser_output(sentence)
                #print(token)
                if is_prev_word_verb(CONSTANTS.PARSER_OUTPUT, i - 1):
                    sent1 = tokens[:i]
                    sent2 = tokens[i:]

                    # Check for the condition
                    # if ('इतना'or'इतनी'or'इतने') in sent1 and 'कि' in sent2:
                    #     manual_evaluation.append(sentence)
                    # else:
                    simpler_sentences.append(" ".join(sent1))
                    simpler_sentences.append(" ".join(sent2))
                    break
                elif i > 1:
                    manual_evaluation.append(sentence)

    return simpler_sentences

def write_input_in_parser_input(file_path, sentence):
    with open(file_path, 'w') as file:
        file.truncate()
        file.write(sentence)
        file.close()
    
    
def get_parser_output(sentence):
    parser_input_file = CONSTANTS.PARSER_INPUT
    write_input_in_parser_input(parser_input_file, sentence)
    with open(CONSTANTS.PARSER_OUTPUT, 'w') as file:
        file.truncate()
    os.system("isc-parser -i p_parser_input.txt -o p_parser_output.txt")
    with open(CONSTANTS.PARSER_OUTPUT, 'r') as file:
        lines = file.readlines()
        tags = [line.strip().split()[3] for line in lines if line.strip()]
        # index = [line.strip().split()[0] for line in lines if line.strip()]


    return tags

def breakAllPairedConnective(sentence, allPairedConnectiveList, manual_evaluation):
    simpler_sentences = breakPairConnective(sentence, manual_evaluation)
    if len(simpler_sentences) == 0:
        allPairedConnectiveList.append(sentence)
        return

    for s in simpler_sentences:
        breakAllPairedConnective(s, allPairedConnectiveList, manual_evaluation)

    return

def breakAllSimpleConnective(sentence, allSimpleConnectiveList, manual_evaluation):
    simpler_sentences = breakSimpleConnective(sentence, manual_evaluation)
    if len(simpler_sentences) == 0:
        allSimpleConnectiveList.append(sentence)
        return

    for s in simpler_sentences:
        breakAllSimpleConnective(s, allSimpleConnectiveList, manual_evaluation)

    return

if __name__ == '__main__':
    input_data = read_input(CONSTANTS.INPUT_FILE)
    output_data = {}
    manual_evaluation = []
    for key, value in input_data.items():
        if validate_sentence(value):
            value = sanitize_input(value)
            # First break the sentence by pair connectives
            allPairedConnectiveList = []
            breakAllPairedConnective(value, allPairedConnectiveList, manual_evaluation)
            allSimpleConnectiveList = []
            for s in allPairedConnectiveList:
                breakAllSimpleConnective(s, allSimpleConnectiveList, manual_evaluation)
        else:
            allSimpleConnectiveList = ['Invalid input']

        output_data[key] = allSimpleConnectiveList
    write_output(output_data, CONSTANTS.OUTPUT_FILE, manual_evaluation)

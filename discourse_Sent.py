from discourse_mapped_rel import discourseMarkerParser
from discourse_mapped_rel import USR
from wxconv import WXC
import re
# Create an instance of the USR class
usr_instance = USR()

# Now you can access multi_word_markers, markers, and discourse_relation dictionaries
multi_word_markers = usr_instance.multi_word_markers
markers = usr_instance.markers
discourse_relation = usr_instance.discourse_relation


def combine_lines_with_prefix(file_path):
    # Example usage
    # combine_lines_with_prefix('sentence_output.txt', "कि")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
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
            print(previous_line)
            if ('इतना'or'इतनी'or'इतने') not in previous_line:
            # if "a " in previous_line:
                # mod_previous_line = previous_line.replace("a", "")
                new_lines[-1] = previous_line.rstrip(' ।\n') + " " + current_text.strip() + "\n"
            # print(new_lines)
            # else:
            #     new_lines[-1] = previous_line.rstrip(' ।\n') + " " + current_text.strip() + "\n"
            else:
                new_lines.append(f"{current_id} {current_text}\n")
        else:
            new_lines.append(f"{current_id} {current_text}\n")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    

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

                # print("a",sent1)
                # print(i)
                m = i
                # print("qqq",len(lines))
                
                # print(m)
                sent1=lines[m].strip()
                sent2=lines[m+1].strip()
                print('jj',sent2,i)
            
                if "तो" not in sent2 :
                    output_line=process_sentences(sent1, sent2, id_1, id_2)
                    
                    print("v",output_line)
                    if i == 0:
                        output_line = output_line.strip()
                        store.append(output_line)

                        for k in range(i + 2, len(lines)):
                            l2.append(lines[k])

                        for n in range(0, len(l2)):
                            store.append(l2[n])
                        # print("s",store)

                        with open(file_path, 'w') as file:
                            for n in range(len(store)):
                                file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]').replace("यद्यपि ",'') + '\n')
                        return process_discourse(file_path)
                    else:
                        for j in range(0, i):
                            l1.append(lines[j])

                        for k in range(i + 2, len(lines)):
                            l2.append(lines[k])

                        for m in range(0, len(l1)):
                            store.append(l1[m])

                        output_line= output_line.strip()

                        store.append(output_line)

                        for n in range(0, len(l2)):
                            store.append(l2[n])
                        m += 1
                        with open(file_path, 'w') as file:
                            for n in range(len(store)):
                                file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]').replace("यद्यपि ",'') + '\n')
                        return process_discourse(file_path)
                            
                    
                        # l1.append(output_line)
                elif "तो" in sent2 :
                    return if_to(file_path)
                
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
                        output_line = process_sentences(sent2, sent3, id_1, id_2)
                        # if "अगर" in output_line:
                        #     output_line=output_line.replace('अगर ', '')
                        # else:
                        #     output_line=output_line.replace('यदि ', '')
                        if i == 0:
                            store.append(lines[0])
                            output_line = output_line.strip()

                            store.append(output_line)

                            for k in range(i + 3, len(lines)):
                                l2.append(lines[k])

                            for n in range(0, len(l2)):
                                store.append(l2[n])

                            with open(file_path, 'w') as file:
                                for n in range(len(store)):
                                    file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                            return process_discourse(file_path)
                        else:
                            for j in range(0, i+1):
                                l1.append(lines[j])

                            for k in range(i + 3, len(lines)):
                                l2.append(lines[k])

                            for m in range(0, len(l1)):
                                store.append(l1[m])

                            output_line= output_line.strip()
                            store.append(output_line)

                            for n in range(0, len(l2)):
                                store.append(l2[n])

                            with open(file_path, 'w') as file:
                                for n in range(len(store)):
                                    file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                            return process_discourse(file_path)
                        
                elif sent3 and  "तो" in sent3 :
                    # print("nn")
                    return if_to(file_path)
                
            elif "तो" in lines[i+1] :
                return if_to(file_path)
            
                # continue
            # Normal processing if "अगर" is not present in sent2
            # print("4")
            output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '').replace("यद्यपि ",'')
            # print("o",output_line)
            # print("s2",sent2)
            # output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '')
            if len(lines) > 2:

                if i == 0:
                    output_line = output_line.strip()
                    store.append(output_line)

                    for k in range(i + 2, len(lines)):
                        l2.append(lines[k])

                    for n in range(0, len(l2)):
                        store.append(l2[n])

                    with open(file_path, 'w') as file:
                        for n in range(len(store)):
                            file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                    return process_discourse(file_path)
                else:
                    for j in range(0, i):
                        l1.append(lines[j])

                    for k in range(i + 2, len(lines)):
                        l2.append(lines[k])

                    for m in range(0, len(l1)):
                        store.append(l1[m])

                    output_line= output_line.strip()
                    store.append(output_line)

                    for n in range(0, len(l2)):
                        store.append(l2[n])

                    with open(file_path, 'w') as file:
                        for n in range(len(store)):
                            file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                    return process_discourse(file_path)
            else:
                output_line=output_line.replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]')
                with open(file_path, 'w') as file:
                    file.write(
                        output_line.replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]').replace('णण् ', '\n'))
                return process_output_line(output_line)
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
            output_line_next = process_sentences(sent2, sent3, id_2, get_ids(sent3)) if sent3 else None
            
            # Process with the current sentence and the next one
            output_line_current = process_sentences(sent1, output_line_next , id_1, get_ids(output_line_next)) if output_line_next else None

            if i == 0:
                store.append(lines[0])
                output_line_current = output_line_current.replace('अगर ', '').replace('यदि ', '').replace("यद्यपि ",'')
                store.append(output_line_current)

                for k in range(i + 3, len(lines)):
                    l2.append(lines[k])

                for n in range(0, len(l2)):
                    store.append(l2[n])

                with open(file_path, 'w') as file:
                    for n in range(len(store)):
                        file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                return process_discourse(file_path)
            else:
                for j in range(0, i):
                    l1.append(lines[j])

                for k in range(i + 3, len(lines)):
                    l2.append(lines[k])

                for m in range(0, len(l1)):
                    store.append(l1[m])

                output_line_current = output_line_current.strip().replace('अगर ', '').replace('यदि ', '')

                store.append(output_line_current)

                for n in range(0, len(l2)):
                    store.append(l2[n])
                i+=1
                with open(file_path, 'w') as file:
                    for n in range(len(store)):
                        file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                return process_discourse(file_path)

    # Normal processing if "अगर" is not present in sent2
        output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '')
        if len(lines) > 2:
            
            if i == 0:
                output_line = output_line.replace('अगर ', '').replace('यदि ', '').replace("यद्यपि ",'')
                store.append(output_line)

                for k in range(i + 2, len(lines)):
                    l2.append(lines[k])

                for n in range(0, len(l2)):
                    store.append(l2[n])

                with open(file_path, 'w') as file:
                    for n in range(len(store)):
                        file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                return process_discourse(file_path)
            else:
                for j in range(0, i):
                    l1.append(lines[j])

                for k in range(i + 2, len(lines)):
                    l2.append(lines[k])

                for m in range(0, len(l1)):
                    store.append(l1[m])

                output_line = output_line.strip().replace('अगर ', '').replace('यदि ', '')

                store.append(output_line)

                for n in range(0, len(l2)):
                    store.append(l2[n])
            
                with open(file_path, 'w') as file:
                    for n in range(len(store)):
                        file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                return process_discourse(file_path)
        else:
            output_line=output_line.replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]')
            with open(file_path, 'w') as file:
                file.write(
                    output_line.replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]').replace('णण् ', '\n'))
            return process_output_line(output_line)
        
        
def if_to(file_path):
    store = []
    l1 = []
    l2 = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # print(lines)
    for i in range(len(lines)):
        
        sent3 = lines[i].strip()
        if "तो" in sent3:
            # print("Processing sentence with 'तो' at line:", i)
            b = i + 1
            while b < len(lines):
                sent4 = lines[b].strip() if b<len(lines) else None
                if sent4 and 'तो' not in sent4 and to_check_same_ids(sent3) == to_check_same_ids(sent4):
                    # print("Processing sentences following 'तो' until IDs match at line:", b)
                    output_line_current = process_sentences(sent3, sent4,get_ids(sent3),get_ids(sent4))
                    if i == 0:
                        output_line_current = output_line_current.strip().replace('अगर ', '').replace('यदि ', '')
                        store.append(output_line_current)
                        for k in range(b + 1, len(lines)):
                            l2.append(lines[k])
                        for n in range(len(l2)):
                            store.append(l2[n])
                        with open(file_path, 'w') as file:
                            for n in range(len(store)):
                                file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                        return process_discourse(file_path)
                    else:
                        for j in range(0, i):
                            l1.append(lines[j])
                        for k in range(b + 1, len(lines)):
                            l2.append(lines[k])
                        for m in range(len(l1)):
                            store.append(l1[m])
                        output_line_current = output_line_current.strip().replace('अगर ', '').replace('यदि ', '')
                        store.append(output_line_current)
                        for n in range(len(l2)):
                            store.append(l2[n])
                        # print(store)
                        b += 1
                        with open(file_path, 'w') as file:
                            for n in range(len(store)):
                                file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                        return process_discourse(file_path)
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
                        
                        output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '')
                        # if "अगर" in output_line:
                        #     output_line = output_line.replace('अगर ', '')
                        # else:
                        #     output_line = output_line.replace('यदि ', '')
                        if i == 0:
                            store.append(lines[0])
                            output_line = output_line.strip()
                            store.append(output_line)
                            for k in range(i + 2, len(lines)):
                                l2.append(lines[k])
                            for n in range(len(l2)):
                                store.append(l2[n])
                            with open(file_path, 'w') as file:
                                for n in range(len(store)):
                                    file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>') + '\n')
                            return process_discourse(file_path)
                        else:
                            for j in range(0, a):
                                l1.append(lines[j])
                            for k in range(i + 1, len(lines)):
                                l2.append(lines[k])
                            for m in range(len(l1)):
                                store.append(l1[m])
                            output_line = output_line.strip()
                            store.append(output_line)
                            for n in range(len(l2)):
                                store.append(l2[n])
                            # print("aaa",store)
                            a -= 1
                            # print(a)
                            with open(file_path, 'w') as file:
                                for n in range(len(store)):
                                    file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                            return process_discourse(file_path)
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
                        output_line = process_sentences(sent1, sent2, id_1, id_2).replace('अगर ', '').replace('यदि ', '')
                        
                        if i == 0:
                            store.append(lines[0])
                            output_line = output_line.strip()
                            store.append(output_line)
                            for k in range(i + 2, len(lines)):
                                l2.append(lines[k])
                            for n in range(len(l2)):
                                store.append(l2[n])
                            with open(file_path, 'w') as file:
                                for n in range(len(store)):
                                    file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                            return process_discourse(file_path)
                        else:
                            for j in range(0, a):
                                l1.append(lines[j])
                            for k in range(i + 1, len(lines)):
                                l2.append(lines[k])
                            for m in range(len(l1)):
                                store.append(l1[m])
                            output_line = output_line.strip()
                            store.append(output_line)
                            for n in range(len(l2)):
                                store.append(l2[n])
                            a -= 1
                            with open(file_path, 'w') as file:
                                for n in range(len(store)):
                                    file.write(store[n].replace('\n', '').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>', '<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]') + '\n')
                            return process_discourse(file_path)
                    else:
                        break        
                b += 1
                
    
        
def process_output_line(output_line):
    
    modified_lines = [output_line.replace('<<o>/S_id> <<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id>', '<<o>/S_id>').replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id>','<<o>/S_id> ]').replace('<<o>/S_id> ] <<o>/S_id>','<<o>/S_id> ]').replace('णण् ', '\n')]
    
    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(modified_lines)

        
def get_discourse_from_word(sentence):
       
       sent=convert_to_eng(sentence)
       sent = sent.split()
       print('ss',sent)
       s = sent[0]

       for i in range(len(sent) - 1):
           
           if s in markers or s in multi_word_markers:
                print(s)
               
                return discourse_relation[s]
           else:
               s += ' ' + sent[i+1]
       return "-1"


def process_sentences(sent1, sent2, id_1, id_2):
    try:
        parser = discourseMarkerParser(sent1, sent2)
    except IndexError:
        return None

    results = parser.get_results()
    hindi_sent1 = convert_to_hindi(results[0]).strip()
    disc_relation = convert_to_hindi(results[1]).strip()
    hindi_sent2 = convert_to_hindi(results[2]).strip()
    h1 = sent1.split()
    h2 = sent2.split()
    # print(disc_relation)
    # print(hindi_sent1)
    # print(hindi_sent2)
    # print(id_2)

    if ('इतना'or'इतनी'or'इतने') in hindi_sent1:
        disc_relation='परिणाम'
        # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation} <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
        output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + " " + ' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
    
    elif h1[0]=='ना' and h1[1]=='केवल' and 'बल्कि' in hindi_sent2:
        disc_relation='समुच्चय'
        hindi_sent1 = hindi_sent1.replace('ना केवल ','')
        hindi_sent2 = hindi_sent2.replace('बल्कि ','')
        # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation}.BI_1 <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
        output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + ".BI_1" + ' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
        
    elif h2[1]=='नहीं' and h2[2]=='तो':
        # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation}.nahIM_1 <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
        output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + ".nahIM_1" + ' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '

    elif results[1] in parser.discourse_pos and parser.discourse_pos[results[1]] == "0":
        output_line = ' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> ' + '[ ' + disc_relation + ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> '+'] '
        # output_line=output_line.replace('<<o>/S_id> <<o>/S_id> ] <<o>/S_id> <<o>/S_id> ]','<<o>/S_id> ]')
        print('oo',output_line)

    elif results[1] =="samuccaya x"  and parser.discourse_pos[results[1]] == 'x':
        if h2[1]=='इसके' and h2[2]=='अलावा' and '?' not in hindi_sent2 and 'नहीं' not in hindi_sent2:
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation}.BI_1 <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
            output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + ".BI_1" + ' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
        elif h2[1]=='इसके' and (h2[2]=='साथ-साथ' or h2[2]=='साथ' and h2[3]=='साथ'):
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation}.समावेशी <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
            output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + ".समावेशी" + ' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
        elif results[1] == "samuccaya x":
            h2 = disc_relation.split()
            disc_relation = h2[0]
            # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation}.x <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
            output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + ".x" +' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
        else:
            # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation}.x <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
            output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + ".x" +' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
    else:
        if h2[1]=='इसके' and h2[2]=='विपरीत':
            # output_line = f"<S_id={id_1}> {hindi_sent1} <<o>/S_id> {disc_relation}.विपरीत <S_id={id_2}> {hindi_sent2} <<o>/S_id>"
            output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation + ".विपरीत" +' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '

        elif h2[1]=='तथा':
            disc_relation=convert_to_hindi(get_discourse_from_word(hindi_sent2))
            if disc_relation!='-1':
                output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation +' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
        
            else:
                output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation +' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
        else:
            output_line = ' <<'+'o'+'>S_id='+id_1+'>' + " " + hindi_sent1 + ' <<'+'o'+'>/S_id> ' + disc_relation +' <<'+'o'+'>S_id='+id_2+'>' + " " + hindi_sent2 + ' <<'+'o'+'>/S_id> '
        
    return output_line

def process_discourse(file_path):
    lines = read_lines(file_path)

    if len(lines) < 2:
        line = lines[0].split()
        id_val = get_ids(lines[0].strip())
        hindi_sent = convert_to_hindi(lines[0].strip())
        # print(f"<S_id={id_val}> {hindi_sent} <<o>/S_id>")
        return
    else:
        combine_lines_with_prefix(file_path)

if __name__ == "__main__":
    file_path='sentence_output.txt'
    # wx = WXC(order='wx2utf', lang='hin')
    process_discourse(file_path)
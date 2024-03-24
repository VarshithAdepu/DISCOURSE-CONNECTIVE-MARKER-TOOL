SIMPLE_CONNECTIVES = ['और', 'एवं', 'इसलिए', 'क्योंकि', 'जबकि', 'तथा', 'ताकि', 'मगर', 'लेकिन', 'किंतु', 'परंतु', 'फिर भी', 'या', 'तथापि',
                      'नहीं तो', 'व', 'चूंकि', 'चूँकि', 'वरना','अन्यथा', 'बशर्तें', 'हालाँकि', 'इसीलिये', 'इसीलिए' , 'इसलिए', 'अथवा', 'अतः', 'अर्थात्', 'जब', 'तो', 'परन्तु', 'कि','बल्कि','पर']

COMPLEX_CONNECTIVES = {'चूँकि' : ['अतः'],
                    #    'जब' : ['तब', 'तो'],
                       'अगर' : ['तो', 'तब'],
                       'यदि' : ['तो', 'तब'],
                       'यद्यपि' : ['फिर भी'],
                    #    'ना केवल':['बल्कि'],
                       }
#INPUT_FILE = "parallel_corpus_verified_data - data2.tsv"
INPUT_FILE = "sentence_input.txt"
PARSER_INPUT = "p_parser_input.txt"
PARSER_OUTPUT = "p_parser_output.txt"
OUTPUT_FILE = "sentence_output.txt"
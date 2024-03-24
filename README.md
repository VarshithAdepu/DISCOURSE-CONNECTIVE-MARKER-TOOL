
# DISCOURSE CONNECTIVE MARKER TOOL

- Input file has unique sentence id for each input
- Input file has : sentence_id "space one or more" sentence
- Each word in the sentence is also space separated. For eg. - 
1. Correct - ग्लोब स्थिर नहीं होते हैं।
2. Incorrect - सूर्य की ओर वाले भाग में दिन होता **है,जबकि** दूसरा भाग जो सूर्य से दूर होता है वहाँ रात होती है। -> Though the sentence has जबकि as connective but it will not be simplified as space is missing. So, "है,जबकि" will be identified as one complete term.
3. Correct - पक्की सड़कें, सीमेंट, कंक्रीट व तारकोल द्वारा निर्मित होती है, **अतः** ये बारहमासी सड़कें हैं ।
- Input file can have many sentences
- Input sentences are in hindi language

## Steps of execution -
- "sentence_input.txt" - Input file with one or more sentences with unique sentence_Id. Sentences are separated by newline character.
- Run this script by executing sentence_subparts.py file.
- "sentence_output.txt" - Output file

## Prerequisite - 
- The isc tagger should be set up in the same project
- Update the file paths in CONSTANTS.py as per your directory

## Next version Todos -
- For input sentences with a connective but, if the prev term of connective is not a VM or VAUX we flag the sentence for manual evaluation

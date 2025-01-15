import re
import os

def create_dynamic_regex(ids):
    global regex_pattern
    """
    Creates a regular expression pattern dynamically based on the root of the IDs.
    
    Args:
        ids (list): List of IDs as strings.
        
    Returns:
        str: A regular expression pattern to match the IDs.
    """
    if not ids:
        return ""
    
    # Find the common root of the IDs
    common_root = os.path.commonprefix(ids)
    
    # Extract unique suffixes (part after the common root)
    suffixes = [id[len(common_root):] for id in ids]
    
    # Create regex for the suffixes
    escaped_suffixes = [re.escape(suffix) for suffix in suffixes]
    suffix_pattern = "|".join(escaped_suffixes)
    
    # Combine root and suffix pattern
    regex_pattern = f"{re.escape(common_root)}(?:{suffix_pattern})"
    print(type(regex_pattern))
    return regex_pattern

def remove_trailing_alphabet(id_string):
    # Regex to match a trailing alphabet at the end of the string
    result = re.sub(r'[a-zA-Z]$', '', id_string)
    return result

# Example usage:
# id_1 = "12345A"
# id_2 = "67890"
# print(remove_trailing_alphabet(id_1))  # Output: "12345"
# print(remove_trailing_alphabet(id_2))  # Output: "67890"


# Example usage
ids = ["HD_hin_target_034", "HD_hin_target_035", "HD_hin_target_036",'HD_hin_target_01','Hk_hin_target_01']
regex_pattern = create_dynamic_regex(ids)
#print(f"Generated Regex Pattern: {regex_pattern}")

# Test the pattern
text = "HD_hin_target_034 and HD_hin_target_035 are valid. HD_hin_target_037 is not."
matches = re.findall(regex_pattern, text)
#print("Matches:", matches)

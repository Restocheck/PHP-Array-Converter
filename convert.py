"""
Converts old arrays to new php 5.4 arrays
"""
import sys

INCORRECT_STRINGS = {'is_array(' : -3, 'in_array(' : -3}

def check_args():
    """
    checks the arguments
    """
    if len(sys.argv) != 2:
        print("Error: One Argument Please")
        print(sys.argv)
        return False
    return True

def all_array_occurences(text):
    """
    Returns all the start indices of array( in given text file
    """

    searchstart = 0
    searchpos = text.find('array(', searchstart)
    indices = []

    while searchpos != -1:
        searchstart = searchpos + 1
        indices.append(searchpos)
        searchpos = text.find('array(', searchstart)

    return indices


def check_occurences(text, indices):
    """
    return a corrected list of indices
    """

    for indice in indices:
        incorrect = False
        for incorrect_match, offset in INCORRECT_STRINGS.items():
            #print(text[indice+offset:indice+6])
            if text[indice+offset:indice+6] == incorrect_match:
                incorrect = True
        if incorrect:
            indices.remove(indice)

    return indices

def find_closing_brace(start, text):
    """
    finds the matching closing
    """
    end = start

    depth = 1
    while depth != 0 and end < len(text):
        if text[end] == '(':
            depth += 1
        elif text[end] == ')':
            depth -= 1
        end += 1

    if depth != 0:
        raise Exception('Unbalanced braces in file')

    return end-1

def find_closing_array_braces(indices, text):
    """
    find the closing braces for the arrays
    """
    brace_indices = []

    for indice in indices:
        brace_indices.append(find_closing_brace(indice+6, text))

    return brace_indices

def convert(file_name):
    """
    Searches for php 4 arrays and converts them
    """
    #read file
    try:
        array_file = open(file_name, 'r+')
        text = array_file.read()
        array_file.close()
    except Exception:
        print("Error: ", sys.exc_info()[0])
        return

    indices = all_array_occurences(text)
    if indices == 0:
        print("Error: No occurences found.")
        return

    indices = check_occurences(text, indices)
    if indices == 0:
        print("Error: No occurences found.")
        return

    try:
        closing_braces = find_closing_array_braces(indices, text)
    except Exception:
        print('Error: Unbalanced braces')
        return

    new_string = text

    for closing_brace in closing_braces:
        new_string = new_string[:closing_brace] + ']' + new_string[closing_brace+1:]


    indices.sort()
    indices.reverse()

    for indice in indices:
        new_string = new_string[:indice] + '[' + new_string[indice+6:]
        text[indice:indice+6].replace('array(', '[')

    print(new_string)

    #write file
    try:
        array_file = open(file_name, 'w')
        array_file.write(new_string)
        array_file.close()
    except Exception:
        print("Error: ", sys.exc_info()[0])
        return
    return

if __name__ == "__main__":
    if check_args():
        convert(sys.argv[1])

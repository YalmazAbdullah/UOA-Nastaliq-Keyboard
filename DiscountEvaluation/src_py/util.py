# STL
import csv
import json

'''
Simple evaluation function that returns percentage of tokens removed from dataset.
'''
def eval(input_size, output_size):
    ratio = float(output_size)/input_size
    print("Loss:    "+str(round((1-ratio) *100,6))+"%")

'''
Read .tsv file, seperate into native and roman.
'''
def read_tsv(file_name):
    # Read the .tsv file
    with open('./DiscountEvaluation/data/'+file_name+'.tsv', 'r', encoding='utf-8') as file:
        native = []
        roman = []

        for line in file:
            # Split the line into two parts based on the tab character
            parts = line.strip().split('\t')
            
            # Check if the line has exactly two parts
            if len(parts) == 2:
                native.append(parts[0])
                roman.append(parts[1])

    # Print the resulting dictionary
    return native,roman

'''
Read .tsv file, seperate into native and roman.
'''
def read_json(adress):
    file = open("./DiscountEvaluation/"+adress+".json")
    data = json.load(file)
    file.close()
    return data

'''
Write the arrays as .tsv file
'''
def write_tsv(native, roman, file_name):
    # write to headless .tsv
    with open('./DiscountEvaluation/data/'+ file_name +'.tsv', 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
    
        for val1, val2 in zip(native, roman):
            writer.writerow([val1, val2])
import re # built-in library for regex
import os # built-in library for os-dependent functions
import pandas as pd # library for tabular data and exporting tsv

#write list of rows in tsv
def write_tsv(rows, column_list, path):

    #convert list of rows into dataframe
    df= pd.DataFrame(rows, columns=column_list)

    #exporting the dataframe to tsv without including the index colunm
    df.to_csv(path, sep="\t", index=False)

#define folder
folder= "../articles"

#setting path for loading gazatteer tsv file
path = "../gazetteers/geonames_gaza_selection.tsv"

#reading the file
with open(path, encoding="utf-8") as file:
    data = file.read()

#building dictionary of patterns for place names and a count of matches
patterns = {}

#split the gazatteer data into different rows using newline character
rows = data.split("\n")

for row in rows[1:]:          #skipping the header
    columns = row.split("\t") #separating the columns using tab    
    if len(columns) < 6:
        continue              # skip the row if it dooes not have atleast 6 colunms

    asciiname = columns[0]
    alternatenames = columns[5].strip()
    detailed_list=[asciiname]  #starting to add the first column to the larger list
    #split column[5] by comma and add various spellings from col[5] to larger list
    if alternatenames:
        ## split the alternate names by comma, remove any surrounding whitespace, and add them to the list of possible spellings
        detailed_list.extend ([alternate.strip() for alternate in alternatenames.split(",")])#help from ChatGPT(Script 1)
            
    
    #build a single regex pattern that matches any alternate using '|' for alterations
    regex_pattern = r"\b("+"|".join(detailed_list) + r")\b"

    patterns[asciiname] = {"pattern": regex_pattern, "count":0}

#creating a dictionary to count the number of each name occurred per month
name_frequency_by_month = {}

#set the starting date of war to filter articles with names occured after that
war_begin_date= "2023-10-07"

#looping through each file to count the occurrences of each pattern across entire folder
for filename in os.listdir(folder):

    #extracting the date from the filename(as the format is YYYY-MM-DD
    date_str = filename.split("_")[0]

#skip the file if it is before the start of the war
    if date_str < war_begin_date:                                                                                                                                 
       continue
    
#build filepath for the current articles
    file_path = os.path.join(folder, filename)   

   #open and read the articles
    with open(file_path, encoding="utf-8")as file:
     text = file.read()
     
   #looping through places to search for matches in the text
    for place, pattern_data in patterns.items():
        pattern = pattern_data["pattern"]                #getting regex pattern
        matches = re.findall(pattern, text, re.IGNORECASE)
        count = len(matches)                              #number of times the place is occured

        if count==0: #took help from ChatGPT(script 1)
            continue

        #adding the number of times places found to the total frequency
        patterns[place]["count"]+=count

       #extracting the month from the string for dates
        month_str= date_str[:7]

       #initializing place and month in name_frequency_by_month dictionary
        if place not in name_frequency_by_month:
           name_frequency_by_month[place]={}
        if month_str not in name_frequency_by_month[place]:
           name_frequency_by_month[place][month_str]=0


       #adding the new matches on the place names to the number of times it was found that month
        name_frequency_by_month[place][month_str] += count


#loop through each place in the name_frequency_by_month dictionary
for place in name_frequency_by_month:    
    print(f'"{place}":{{')

    #get a list of all the months in which the place names are mentioned         
    month_list = list(name_frequency_by_month[place].keys())
    #loop through each month to print the corresponding mention count for month in month_list
    for month in month_list:
        count = name_frequency_by_month[place][month]#find count for that month 
 
        #display the output by a comma except for the last item to keep it clean
        if month!= month_list[-1]:
            print(f' "{month}":{count},')
        else:
            print(f' "{month}":{count}')
        
    print("},") #close the dictionary block and print the output

#converting the name_frequency_by_month dictionary to a list containing rows for output

rows =[]

#looping through each place again to prepare structured data in order to export
for place in name_frequency_by_month:

#looping through each month and find the number of times the place is found
    for month in name_frequency_by_month[place]:
        count= name_frequency_by_month[place][month]

        #append a tuple(place, month, count) to the rows list
        rows.append((place, month,count))

#write the final result to tsv for external use
write_tsv(rows,["placename","month","count"],"regex_counts.tsv")

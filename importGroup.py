import pandas as pd
import sys
import json
import math
import re

def isnan(x):
    try:
        return math.isnan(x)
    except TypeError:
        return False

userInput = ''

#make sure arguments are correct
if len(sys.argv) != 2:
    sys.exit("Incorrect number of arguments: importGroup.py <moduleX>")

pd.set_option("display.max_colwidth", 100000)

fileString = './' + sys.argv[1] + '/uploadGrading/'
try:
	canvasDF = pd.read_csv(fileString + 'canvas.csv')
except:
	sys.exit(f"Please check file structure, could not find folder for {sys.argv[1]}")
originalColumnNames = canvasDF.columns
canvasDF.columns = map(str.lower, canvasDF.columns)
googleDF = pd.read_csv(fileString + 'googleGroup.csv', encoding ='latin1')
googleDF.columns = map(str.lower, googleDF.columns)
googleDF.columns = googleDF.columns.map(lambda x: x.strip() if type(x) is str else x)
student1IDColumnName = list(googleDF)[1]
student2IDColumnName = list(googleDF)[2]
canvasDF = canvasDF.drop([0])

print(canvasDF.iloc[:, 2])
canvasDF.iloc[:, 2] = canvasDF.iloc[:, 2].astype(int)
gradedStudents = googleDF.iloc[:,1].tolist()
gradedStudents.extend(googleDF.iloc[:,2].tolist())
gradedStudents = [int(x) for x in gradedStudents if not isnan(x)]

#check for duplicates
duplicates = set([x for x in gradedStudents if gradedStudents.count(x) > 1])
if len(duplicates) != 0:
    print("Duplicate ID numbers detected")
    for duplicate in duplicates:
        duplicateRow = googleDF.loc[googleDF.iloc[: , 1] == duplicate]
        if duplicateRow.empty:
            duplicateRow = googleDF.loc[googleDF.iloc[:, 2] == duplicate]
        for index, row in duplicateRow.iterrows():
            print("TA: " + row["ta name"] + "\t ID Numbers: " + str(row.iloc[1]) + ", " + str(row.iloc[2]))
        
    while userInput != 'remove' and userInput != 'quit':
        userInput = input("Type 'remove' to remove duplicates, type 'quit' to quit \n")
        
if userInput == 'remove':
    print("Removing............")
    #10/10/20: added inplace param, previously wasn't removing dupes at all?
    googleDF.drop_duplicates(subset = [student1IDColumnName, student2IDColumnName], inplace=True)
if userInput == 'quit':
    sys.exit("Aborting script")


#check for missing grades
# ungraded = canvasDF.drop([index for index, row in canvasDF.iterrows() if row["sis user id"] in list(gradedStudents)])
# if len(ungraded) != 0:
#     ungradedDict = {}
#     with open(fileString + 'groupAssignments.txt', 'r', encoding = 'utf-8') as myfile:
#         data = myfile.read().replace('\n', '')
#     graderStudentJson = json.loads(data)
#     for x in graderStudentJson["Message"]:
#         ungradedDict[x] = ""

#     print("\nUngraded Module detected")
#     for index, row in ungraded.iterrows():
# #		print("Student Name: " + row.iloc[0] + "\t ID Number: " + str(row.iloc[2]))
#         for x in graderStudentJson["Message"]:
#             for y in graderStudentJson["Message"][x]:
#                 if str(row.iloc[2]) in y:
#                     if str(row.iloc[2]) not in ungradedDict[x]:
#                         output = re.findall(r"(?<!\d)\d{6}(?!\d)", y)
#                         ungradedDict[x] += str(output) + ", "
#     for key, value in ungradedDict.items():
#         if value != "":
#             print(key, value)

#     userInput = input("Type 'continue' to continue, or type 'quit' to quit \n")

while userInput != 'continue' and userInput != 'quit':
    userInput = input("Type 'continue' to continue, or type 'quit' to quit \n")

if userInput == 'quit':
    sys.exit("Aborting script")


#populate canvas spreadsheet with graded values and notes
moduleNumber = [col for col in canvasDF.columns if (sys.argv[1]) in col.replace(" ", "")]
if len(moduleNumber) > 1:
    sys.exit(f"Error: more than one module named {sys.argv[1]}")

if len(moduleNumber) == 0:
    sys.exit(f"Error: no module named {sys.argv[1]}")

for index, row in canvasDF.iterrows():
    if row["sis user id"] in list(gradedStudents):
        rowToPopulate = googleDF.loc[googleDF.iloc[:, 1] == int(row["sis user id"])]
        if not rowToPopulate.empty:
            canvasDF.loc[index, moduleNumber] = float(rowToPopulate['total score'])
            canvasDF.loc[index, "notes"] = rowToPopulate["explanations"].to_string(index = False)
        else:
            rowToPopulate = googleDF.loc[googleDF.iloc[:, 2] == int(row["sis user id"])]
            canvasDF.loc[index, moduleNumber] = float(rowToPopulate['total score'])
            canvasDF.loc[index, "notes"] = ""
            canvasDF.loc[index, "notes"] = rowToPopulate["explanations"].to_string(index = False)


#export grades to csv
canvasDF.columns = originalColumnNames
columnsToKeep = ['Student', 'ID', 'SIS User ID', 'SIS Login ID', 'Section', 'Notes']
moduleNumber = [name for name in originalColumnNames if name.lower() == moduleNumber[0]]
columnsToKeep.append(moduleNumber[0])
canvasDF = canvasDF.drop(columns = [column for column in originalColumnNames if column not in columnsToKeep])
canvasDF.to_csv(sys.argv[1] + '/uploadGrading/' + sys.argv[1] + 'GroupOut.csv', encoding='utf-8', index = False)
print("CSV file outputted")

import pandas as pd
import sys
import json

userInput = ''

#make sure arguments are correct
if len(sys.argv) != 2:
	sys.exit("Incorrect number of arguments: importIndividual.py <moduleX>")

pd.set_option("display.max_colwidth", 100000)

fileString = './' + sys.argv[1] + '/uploadGrading/'
try:
	canvasDF = pd.read_csv(fileString + 'canvas.csv')
except:
	print (f"Error: {sys.execInfo()[0]}")
	sys.exit(f"Please check file structure, could not find folder for {sys.argv[1]}")
originalColumnNames = canvasDF.columns
canvasDF.columns = map(str.lower, canvasDF.columns)
googleDF = pd.read_csv(fileString + 'googleIndividual.csv')
googleDF.columns = map(str.lower, googleDF.columns)
googleDF.columns = googleDF.columns.map(lambda x: x.strip() if type(x) is str else x)
studentIDColumnName = list(googleDF)[1]
canvasDF = canvasDF.drop([0])
#print(canvasDF.columns)
#print(googleDF.columns)
#print(canvasDF.iloc[:,2])
canvasDF.iloc[:, 2] = canvasDF.iloc[:, 2].astype(int)
googleDF.iloc[:, 1] = googleDF.iloc[:, 1].astype(int) 
gradedStudents = googleDF.iloc[:,1]

#check for duplicates
duplicates = googleDF[gradedStudents.isin(gradedStudents[gradedStudents.duplicated()])].sort_values(by=[studentIDColumnName])
if len(duplicates != 0):
	print("Duplicate ID numbers detected")
	# for index, row in duplicates.iterrows():
		# print("TA: " + row["ta name"] + "\t ID Number: " + str(row.iloc[1]))
	userInput = input("Type 'remove' to remove duplicates, type 'quit' to quit \n")
	while userInput != 'remove' and userInput != 'quit':
		userInput = input("Type 'remove' to remove duplicates, type 'quit' to quit \n")

if userInput == 'remove':
	print("Removing...........")
	googleDF = googleDF.drop_duplicates(subset = [studentIDColumnName])
if userInput == 'quit':
	sys.exit("Aborting script")


# # check for missing grades
# ungraded = canvasDF.drop([index for index, row in canvasDF.iterrows() if row["sis user id"] in list(gradedStudents)])
# if len(ungraded) != 0:
# 	ungradedDict = {}
# 	with open(fileString + 'individualAssignments.txt', 'r', encoding = 'utf-8') as myfile:
# 		data = myfile.read().replace('\n', '')
# 	print(data)
# 	graderStudentJson = json.loads(data)
# 	for x in graderStudentJson["Message"]:
# 		ungradedDict[x] = ""

# 	print("\nUngraded Module detected")
# 	for index, row in ungraded.iterrows():
# #		print("Student Name: " + row.iloc[0] + "\t ID Number: " + str(row.iloc[2]))
# 		for x in graderStudentJson["Message"]:
# 			for y in graderStudentJson["Message"][x]:
# 				if str(row.iloc[2]) in y:
# 					ungradedDict[x] += str(row.iloc[2]) + " "
# 	for key, value in ungradedDict.items():
# 		if value != "":
# 			print(key, value)

# 	userInput = input("Type 'continue' to continue, or type 'quit' to quit \n")

# 	while userInput != 'continue' and userInput != 'quit':
# 		userInput = input("Type 'continue' to continue, or type 'quit' to quit \n")

# 	if userInput == 'quit':
# 		sys.exit("Aborting script")


#populate canvas spreadsheet with graded values and notes
for i in range(len(canvasDF.columns)):
		print (f"original: {originalColumnNames[i]} | canvas: {canvasDF.columns[i]}")

moduleNumber = [col for col in canvasDF.columns if (sys.argv[1]) in col.replace(" ", "")]
if len(moduleNumber) > 1:
	print("moduleNumber: ")
	print(moduleNumber)
	sys.exit(f"Error: more than one module named {sys.argv[1]}")

if len(moduleNumber) == 0:
	sys.exit(f"Error: no module named {sys.argv[1]} in canvas import")

for index, row in canvasDF.iterrows():
	if row["sis user id"] in list(gradedStudents):
		canvasDF.loc[index, moduleNumber] = int(googleDF.loc[googleDF.iloc[:, 1] == int(row["sis user id"])]['total score'])
		canvasDF.loc[index, "notes"] = ""
		canvasDF.loc[index, "notes"] = googleDF.loc[googleDF.iloc[:, 1] == int(row["sis user id"])]["explanations"].to_string(index = False).replace('\n', " ")



#export grades to csv
print((originalColumnNames))
print((canvasDF.columns))
canvasDF.columns = originalColumnNames
#columnsToKeep = ['Student', 'ID', 'SIS User ID', 'SIS Login ID', 'Section', 'Notes']
columnsToKeep = ['Student', 'ID', 'SIS User ID', 'SIS Login ID', 'Section', 'Notes']
moduleNumber = [name for name in originalColumnNames if name.lower() == moduleNumber[0]]
columnsToKeep.append(moduleNumber[0])
canvasDF = canvasDF.drop(columns = [column for column in originalColumnNames if column not in columnsToKeep])
canvasDF.to_csv(sys.argv[1] + '/uploadGrading/' + sys.argv[1] + 'IndividualOut.csv', encoding='utf-8', index = False)
print("CSV file outputted")

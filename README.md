# 330grading

### Basic usage

1. For each assignment, create an additional directory in the root of this repo containing enough characters of an assignment from the Canvas gradebook to be unique.
  * For module 1, I called the directory "module1". For module 2 individual, I called the directory "module2in", and for the group, "module2gr". Note that "module2i" would also have been acceptable, since that's unique.
2. Inside that directory, create a new directory called "grading".
3. In google sheets, create a new column titled "total score", and calculate the total score for each student using `=SUM(Bx, By)`.
4. Download it as .csv, and name the file either `googleIndividual.csv` or `googleGroup.csv` accordingly. Then, put it inside the "grading" directory created in step 2.
5. Export the canvas gradebook, and rename it to `canvas.csv`.
  * Create a new column and call it `notes`.
  * Delete any test student (Usually called Student, Test).
  * Place it in the "grading" directory.
6. Run the corresponding python script.
  * Usage is `python3 [importIndividual.py | inportGroup.py] <unique_assignment_directory_name>`
  * e.g. to grade module3 individual, `python3 ./importIndividual.py module3in`
7. Import the outputted .csv file to Canvas(should end with Out.csv)
 

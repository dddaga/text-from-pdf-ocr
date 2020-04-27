
custom_config = r'-l hin --psm 6'

# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 

# Path of the pdf 
PDF_file = "/home/naresh/Tesseract/Languagefiles/Hindi/law_commisionofindia/law_commisionofindia.pdf"

''' 
Part #1 : Converting PDF to images 
'''

# Store all the pages of the PDF in a variable 
pages = convert_from_path(PDF_file, 500) 

# Counter to store images of each page of PDF to image 
image_counter = 1

for page in pages: 
 
	filename = "/home/naresh/Tesseract/PDF_Images/Hindi/"+"law_commisionofindia"+str(image_counter)+".jpg"
	
	# Save the image of the page in system 
	page.save(filename, 'JPEG') 

	# Increment the counter to update filename 
	image_counter = image_counter + 1

''' 
Part #2 - Recognizing text from the images using OCR 
'''
# Variable to get count of total number of pages 
filelimit = image_counter-1

outfile = "/home/naresh/Tesseract/tesseract_result/Hindi/law_commisionofindia.txt"

f = open(outfile, "a") 
# Iterate from 1 to total number of pages 
for i in range(1, filelimit + 1): 

	# Set filename to recognize text from 
	# Again, these files will be: 
	# page_1.jpg 
	# page_2.jpg 
	# .... 
	# page_n.jpg 
	filename = "/home/naresh/Tesseract/PDF_Images/Hindi/"+"law_commisionofindia"+str(i)+".jpg"
		
	# Recognize the text as string in image using pytesserct 
	text = str(((pytesseract.image_to_string(Image.open(filename),lang='tam+hin')))) 
        
	text = text.replace('-\n', '')	 
	f.write(text) 






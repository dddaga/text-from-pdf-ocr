
# Import libraries 
from PIL import Image 
import pytesseract 
import sys
import cv2
from pdf2image import convert_from_path 
import os 
from table import TableRepositories
import tesserocr
import io
from pytesseract import Output
from tesserocr import PyTessBaseAPI, RIL, iterate_level


PDF_path = "/home/naresh/Tesseract/Languagefiles/Hindi/law_commisionofindia/law_commisionofindia.pdf"
img_save_path =  "/home/naresh/Tesseract/PDF_Images/Hindi/"+"law_commisionofindia"


def font_details(req_image):
	with tesserocr.PyTessBaseAPI() as api:
		#image = Image.open(io.BytesIO(req_image))
		#image = req_image
		api.SetImageFile(req_image)
		api.Recognize()  # required to get result from the next line
		iterator = api.GetIterator()
		info = iterator.WordFontAttributes()
		print(info)
	return info["bold"],info["font_name"],info["pointsize"]



def get_font(image_path):
    with PyTessBaseAPI() as api:
        api.SetImageFile(image_path)
        api.Recognize()
        ri = api.GetIterator()
        level = RIL.SYMBOL
        print(ri)
        for r in iterate_level(ri, level):
            symbol = r.GetUTF8Text(level)
            word_attributes = r.WordFontAttributes()
            print(word_attributes)
            if symbol:
                 print(u'symbol {}, font: {}'.format(symbol, word_attributes['font_name']))


def line_bbox(img,line_text_dict,page_no):
	d = pytesseract.image_to_data(img, output_type=Output.DICT)
	n_boxes = len(d['level'])
	for i in range(n_boxes):
	    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	    
	    if int(d['conf'][i])==-1 and h<=150:
	        dict1={}
	        dict1["x"]=x
	        dict1["y"]=y
	        dict1["page_no"]=page_no #,dict1["font-size"]=pointsize,dict1["is_bold"]=bold,dict1["node_index"]=x
	        #dict1["font-family"]=font_name
	        if dict1 in line_text_dict:
	            pass
	        else:
	            line_text_dict.append(dict1)
	return line_text_dict


def line_extract(PDF_path,img_save_path):
	pages = convert_from_path(PDF_path, 500) 
	line_text_dict = []
	for page_no,page in enumerate(pages):
		filename = img_save_path+'_'+str(page_no)+".jpg"
		# Save the image of the page in system 
		page.save(filename, 'JPEG')
		img=cv2.imread(filename)
               #To get font details
		#bold,font_name,pointsize = get_font(filename)
		#Extract table in image
		TableRepo = TableRepositories(filename)
		tables = TableRepo.response

		if len(tables["response"]["tables"])!=0:
		    #img=cv2.imread(filename)
		    x = tables["response"]["tables"][0]['x']
		    y = tables["response"]["tables"][0]['y']
		    w = tables["response"]["tables"][0]['w']
		    h = tables["response"]["tables"][0]['h']
		    img[y:y+h,x:x+w]=255
		    line_text_dict = line_bbox(img,line_text_dict,page_no)


		else:
		    line_text_dict = line_bbox(img,line_text_dict,page_no)
	
	return line_text_dict
		
	
output = line_extract(PDF_path,img_save_path)

print(output)
print(len(output))


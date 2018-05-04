import time
#fore num_results
import requests
from bs4 import BeautifulSoup
#for click
import win32api, win32con
#for screen_shot
import mss
import mss.tools
#for check_questions
from PIL import Image
#for get str_of_image
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
#for box wisker
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"


def num_results(s):
   print(s, "searched")
   search = s

   
   r = requests.get("https://www.google.com/search", params={'q':search})
   
   soup = BeautifulSoup(r.text, "lxml")
   res = soup.find("div", {"id": "resultStats"})
   if res.text:
      pos_r = res.text.find('r')
      if res.text[0] == 'A':
         num_text = res.text[6:pos_r].replace(",", "")
         return int(num_text)
      else:
         num_text = res.text[0:pos_r].replace(",", "")
         print(int(num_text), "results")
         return int(num_text)
   else:
      print("0 results")
      return 0
   
def click(x,y):
   print("clicked: (" + str(x) + ", " + str(y) + ")")
   win32api.SetCursorPos((x,y))
   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
def screen_shot():
   print("screen shot taken")
   with mss.mss() as sct:
       # The screen part to capture
       monitor = {'top': 115, 'left': 1377, 'width': 1086, 'height': 1927}
       output = "screen_shot.png".format(**monitor)
   
       # Grab the data
       sct_img = sct.grab(monitor)
   
       # Save to the picture file
       mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

perma_num = 0

def perma_screen_shot():
   with mss.mss() as sct:
       # The screen part to capture
       monitor = {'top': 115, 'left': 1377, 'width': 1086, 'height': 1927}

       #monitor = {'top': 0, 'left': 0, 'width': 3850, 'height': 2200}
       global perma_num
       output = (str(perma_num) + ".png").format(**monitor)
       perma_num += 1
       # Grab the data
       sct_img = sct.grab(monitor)
       print("perma screen shot taken", perma_num - 1)

       # Save to the picture file
       mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
       
#emulator = True
##i_phone screen shot
#corner_1 = 100, 170
#corner_2 = 650, 170
#corner_3 = 100, 900
#corner_4 = 650, 900
#choice_a = 120, 590
#choice_b = 120, 710
#choice_c = 120, 830
#question_box =  (40, 250, 710, 490)
#a_box = (90, 530, 520, 590)
#b_box = (90, 660, 520, 720)
#c_box = (90, 780, 520, 840)

#emulator
#if emulator:
corner_1 = 50, 415
corner_2 = 50, 715
corner_3 = 1030, 415
corner_4 = 1030, 715
choice_a = 115, 490
choice_b = 120, 585
choice_c = 120, 690
question_box =  (40, 170, 1040, 410)
a_box = (75, 440, 830, 490)
b_box = (75, 535, 830, 585)
c_box = (75, 630, 830, 680)


to_check = [corner_1, corner_2, corner_3, corner_4, choice_a, choice_b, choice_c]

def check_question_asked(file_name):
   im = Image.open(file_name) #Can be many different formats.
   pix = im.load()
   asking = True
   for pixel in range(0, len(to_check)):
      rbg = pix[to_check[pixel][0], to_check[pixel][1]]
      if rbg[0] < 230 and rbg[1] < 230 and rbg[2] < 230:
         asking = False
   if asking:
      print("checked: asking")
   else:
      print("checked: not asking")
   return asking

def crop(file_name):
   total = Image.open(file_name) #Can be many different formats.
   question_image = total.crop(question_box)
   a_image = total.crop(a_box)
   b_image = total.crop(b_box)
   c_image = total.crop(c_box)
   
   question_image.save("question.png")
   a_image.save("a.png")
   b_image.save("b.png")
   c_image.save("c.png")
   
   print("cropped into parts")

def str_of_image(file_name):
   print("reading image to string")
   return pytesseract.image_to_string(Image.open(file_name))

   
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False   

def condense_question(question):
   words = []
   while(question.find("“") != -1):
      first_quote = question.find("“")
      first_part = question[0:first_quote]
      
      words = words + first_part.split(" ")      
      second_quote = question.find("”")
      
      words.append(question[first_quote: second_quote+1])
      question = question[second_quote + 1:]
         
   words = words + question.split(" ")
   
   words = [x for x in words if len(x) > 3 or is_int(x) or (len(x) > 0 and x[0].isupper())]
   to_delete = []
   for i in range(0, len(words) - 1):
      if words[i][0].isupper():
         j = i + 1
         while j < len(words) and words[j][0].isupper():
            to_delete.append(j)
            j += 1
         for k in range(i + 1, j):
            words[i] += " " + words[k]
   to_delete = list(set(to_delete))
   for i in range(len(to_delete) - 1, -1, -1):
      del words[to_delete[i]]
   return words

def print_images_str():
   print(str_of_image("question.png").replace('\n', " "))
   print(str_of_image("a.png"))
   print(str_of_image("b.png"))
   print(str_of_image("c.png"))
   
   
def get_correlations(question, a, b, c):
   q_word_list = condense_question(question)

   
   data_a = []
   data_b = []
   data_c = []
   
   for i in range(0, len(q_word_list)):
      data_a.append(num_results(a + " " + q_word_list[i]))
      
   for i in range(0, len(q_word_list)):
      data_b.append(num_results(b + " " + q_word_list[i]))
      
   for i in range(0, len(q_word_list)):
      data_c.append(num_results(c + " " + q_word_list[i]))
   
   n, bins, patches = plt.hist(data_a, 50, density=True, facecolor='g', alpha=0.75)

   plt.show()
   
def get_best_ratio(question, a, b, c):
   results_a = num_results(a)
   results_b = num_results(b)
   results_c = num_results(c)

   results_qa = num_results(question + " " + a)
   results_qb = num_results(question + " " + b)
   results_qc = num_results(question + " " + c)
   
   ratio_a = results_qa / results_a
   ratio_b = results_qb / results_b
   ratio_c = results_qc / results_c

   
   answer = 0
   if ratio_a < ratio_b:
      answer = 1
   if results_b < ratio_c:
      answer = 2
   
   print("answer is " + chr(97 + answer))
   return answer

def get_most_search(question, a, b, c):
   results_qa = num_results(question + " " + a)
   results_qb = num_results(question + " " + b)
   results_qc = num_results(question + " " + c)
   
   answer = 0
   if results_qa < results_qb:
      answer = 1
   if results_qb < results_qc:
      answer = 2
   
   print("answer is " + chr(97 + answer))
   return answer

def get_top_link(s):
   print(s, "searched")
   search = s

   
   r = requests.get("https://www.google.com/search", params={'q':search})

   soup = BeautifulSoup(r.text, "lxml")
   mydivs = soup.findAll("h3", {"class": "r"})
   for div in mydivs:
      result_links = div.find_all("a")
      for link in result_links:
         print(link['ping'])



def search_pages(q, a, b, c):
   question = condense_question(q)
   

delay = 2
def play_game():
   while True:
      time.sleep(delay)
      screen_shot()
      if check_question_asked("screen_shot.png"):
         crop("screen_shot.png")
         question = str_of_image("question.png").replace("\n", " ")
         a = str_of_image("a.png")
         b = str_of_image("b.png")
         c = str_of_image("c.png")
         print(get_most_search(question, a, b, c))











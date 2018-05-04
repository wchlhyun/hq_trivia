import data
import hq_trivia as h

question_data = data.get_data()
#---------
#test ratio
#----------
ratio_num_correct = 0
ratio_num_tested = 0
def test_ratio():
   global ratio_num_correct
   global ratio_num_tested
   for datum in question_data:
      q = datum[0]
      a = datum[1][0]
      b = datum[1][1]
      c = datum[1][2]
      answer = datum[2]
      if answer == h.get_best_ratio(q, a, b, c):
         ratio_num_correct += 1
      ratio_num_tested += 1
      
#----------------
#test most search
#----------------
most_num_correct = 0
most_num_tested = 0
def test_most_search():
   global most_num_correct
   global most_num_tested
   for datum in question_data:
      q = datum[0]
      a = datum[1][0]
      b = datum[1][1]
      c = datum[1][2]
      answer = datum[2]
      if answer == h.get_most_search(q, a, b, c):
         most_num_correct += 1
      most_num_tested += 1

import twitter
api = twitter.Api(consumer_key = "9c7dbJxyExyCic3YemrwPUdcT",
                  consumer_secret="7LATQKMg2Jg64D8ScpsL8pdQv0Vmo6G6M8lo81REYIPTeC9qxJ",
                  access_token_key= "908527052315389952-LJLFfBf8n4zIVS3mZMbnHZui0vi2QyQ",
                  access_token_secret="Eim1y1wQyX1VVZ7V5fH8fDS2bV2mFFp2yrtt9VJzHcQeZ",
                  tweet_mode = 'extended')

hq_scribe_id = 959113914045911045
statuses = api.GetUserTimeline(hq_scribe_id)

def update_data():
   id_file = open("ids.txt", "r")
   ids = {}
   for line in id_file:
      ids[hash(str(line))] = line
   id_file.close()
   id_file = open("ids.txt", "a")
   data_file = open("data.txt", "a")
   statuses = api.GetUserTimeline(hq_scribe_id, count=200, exclude_replies = True)
   print("length", len(statuses))
   for status in statuses:
      if not (hash(str(status.id) + "\n") in ids):
         split = status.full_text.split("\n")
         if (len(split) != 4):
            print(status.id)
            print(status.full_text)
            raise Exception("Split into " + str(len(split)) + " instead of 4") 
         question = split[0]
         answer = 0;
         for i in range(1, 4):
            if split[i].find('✓') != -1:
               answer = i - 1
         choice_a = split[1].replace('✓', "")[3:]
         choice_b = split[2].replace('✓', "")[3:]
         choice_c = split[3].replace('✓', "")[3:]
         
         data_file.write(question + "\n")
         data_file.write(choice_a + "\n")
         data_file.write(choice_b + "\n")
         data_file.write(choice_c + "\n")
         data_file.write(str(answer) + "\n")
         
         id_file.write(str(status.id) + "\n")
         
   id_file.close()
   data_file.close()
   
def get_data():
   data = []
   data_file = open("data.txt", "r")
   for line in data_file:
      temp_q = line
      question = temp_q[0:len(temp_q) -1]
      temp_a = next(data_file)
      choice_a = temp_a[0:len(temp_a) -1]
      temp_b = next(data_file)
      choice_b = temp_b[0:len(temp_b) -1]
      temp_c = next(data_file)
      choice_c = temp_c[0:len(temp_c) -1]
      temp_answer = next(data_file)
      answer = int(temp_answer)
      data.append([question, [choice_a, choice_b, choice_c], answer])

   return data
   
   
   
   
   
   
   
   
   
import requests 
from bs4 import BeautifulSoup 
import os,pandas,numpy

output={
		"URL ID":[],
		"URL":[],
		"POSITIVE SCORE":[],
		"NEGATIVE SCORE":[],
		"POLARITY SCORE":[],
		"SUBJECTIVITY SCORE":[],
		"AVG SENTENCE LENGTH":[],
		"PERCENTAGE OF COMPLEX WORDS":[],
		"FOG INDEX":[],
		"AVG NUMBER OF WORDS PER SENTENCE":[],
		"COMPLEX WORD COUNT":[],
		"WORD COUNT":[],
		"SYLLABLE PER WORD":[],
		"PERSONAL PRONOUNS":[],
		"AVG WORD LENGTH":[]
		}
stop_word,n,p=[],numpy.array(pandas.read_csv(f"MasterDictionary/negative-words.txt",names=["neg"], encoding='latin-1').dropna()).reshape(-1),numpy.array(pandas.read_csv(f"MasterDictionary/positive-words.txt",names=["neg"], encoding='latin-1').dropna()).reshape(-1)
d_input=numpy.array(pandas.read_excel("Input.xlsx"))
for i in os.listdir("StopWords"):
	if i=="StopWords_Currencies.txt":
		stop_word=stop_word+list(numpy.array(pandas.read_csv(f"StopWords/{i}", sep='|',names=["currencies","contry"], encoding='latin-1')).reshape(-1))
	else:
		stop_word=stop_word+open(f"StopWords/{i}","r").read().split("\n")

class analysis:
	def __new__(self,data):
		sentence=[[[i for i in i.split(" ")if i!="" and i not in stop_word] for i in i.split(". ")] for i in data.split("\n") if i!=""]
		sentence=sentence[1:len(sentence)-1]
		return analysis.p_n_spliter(sentence)
	def p_n_spliter(sentence):
		n_,p_,word_count,sentence_,complex_word,syllable,pronouns,sum_words=[],[],0,0,0,0,0,0
		for i in sentence:
			for j in i:
				sentence_+=1
				for z in j:
					if z in ['I','we','my','ours','us']:
						pronouns+=1
					if z[len(z)-2:len(z)]!="es"or z[len(z)-2:len(z)]!="ed":
						syllable+=len([l for l in z if l.lower() in ['a','e','i','o','u']])
					sum_words+=len(z)
					d = {}.fromkeys('aeiou',0)
					haslotsvowels=False
					for x in z.lower():
						if x in d:
							d[x]+=1
					for q in d.values():
						if q>2:
							haslotsvowels=True
					if haslotsvowels:
						complex_word+=1
					word_count+=1
					if z in p:
						p_.append(z)
					elif z in n:
						n_.append(z)

		return (len(n_),len(p_),(len(n_)-len(p_))/((len(n_)+len(p_))+0.000001),
		(len(n_)+len(p_))/(word_count+0.000001),word_count/sentence_,complex_word/word_count,0.4*(word_count/sentence_+complex_word/word_count),
		word_count/sentence_,complex_word,word_count,syllable/word_count,pronouns,sum_words/word_count)

for i in d_input:
	print(i[0],i[1])
	r=requests.get(i[1]) 
	soup=BeautifulSoup(r.content, 'html5lib')
	o=soup.find("div", class_="td-post-content tagdiv-type")
	if o!=None:
		data=o.text
	else:
		try:
			data=[i.text for i in soup.find_all("div", class_="tdb-block-inner td-fix-index")if i.text!="" and len(i.text)>150][0]
		except:
			continue
	a_=analysis(data)


	output["URL ID"].append(i[0]),output["URL"].append(i[1]),output["POSITIVE SCORE"].append(a_[0]),output["NEGATIVE SCORE"].append(a_[1]),output["POLARITY SCORE"].append(a_[2]),
	output["SUBJECTIVITY SCORE"].append(a_[3]),output["AVG SENTENCE LENGTH"].append(a_[4]),output["PERCENTAGE OF COMPLEX WORDS"].append(a_[5]),
	output["FOG INDEX"].append(a_[6]),output["AVG NUMBER OF WORDS PER SENTENCE"].append(a_[7]),output["COMPLEX WORD COUNT"].append(a_[8]),
	output["WORD COUNT"].append(a_[9]),output["SYLLABLE PER WORD"].append(a_[10]),output["PERSONAL PRONOUNS"].append(a_[11]),output["AVG WORD LENGTH"].append(a_[12])
pandas.DataFrame(output).to_excel("output.xlsx")
	
#tdb-block-inner td-fix-index"""
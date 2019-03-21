import requests
import re
import datetime
import time
import calendar


def get_time(text):
	first = text.find("-")
	second = text.find("-",first+1)
	day = text[:first]
	month = text[first+1:second]
	year = text[second+1:]
	day_int = int(day)
	month_int = int(list(calendar.month_abbr).index(month))
	year_int = int(year)
	x = datetime.datetime(year_int, month_int, day_int)
	y =time.mktime(x.timetuple())
	out = str(y)
	return y

days=[]
days_data=[]
creds=[
		["u1603033","160348"],
		["u1603012","160340"],
		["u1603071","160745"],
		["u1603038","160096"],
		["u1603062","160180"],
		["u1603008","160134"],
		["u1603013","160529"],
		["u1603021","160751"],
		["u1603039","160839"],
		["u1603040","160185"],
		["u1603069","160011"],
		["u1603054","160142"],
		["u1603055","160205"],
		["u1603048","160719"],
		["u1603020","160380"],
		["u1603030","160766"],
		["u1603019","160278"],
		["u1603025","160606"],
		["u1603063","160151"],
		["u1603066","160143"],
		["u1603046","160395"],
		["u1603005","160183"],
		["u1603018","160613"],
		["u1603070","160768"],
		["u1603011","160113"],
		["u1603026","160525"],
		["u1603053","160172"],
		["u1603065","160442"],
		["u1603032","160188"],
		["u1603044","160216"],
		["u1603045","160003"],
		["u1603041","160564"],
		["u1603052","160218"],
		["u1603001","160546"],
		["u1603022","160536"],
		["u1603057","160824"],
		["u1603050","160124"],
		["u1603009","160461"],
		["u1603004","160316"],
		["u1603016","160025"],
		["u1603010","160194"],
		["u1603061","160300"],
		["u1603023","160241"],
		["u1603064","160138"],
		["u1603006","160201"],
		["u1603067","160209"],
		["u1603034","160792"],
		["u1603056","160746"],
		["u1603003","160817"],
		["u1603059","160811"],
		["u1603068","160718"],
		["u1603036","160526"],
		["u1603027","160644"],
		["u1603037","160169"],
		["u1603029","160744"],
		["u1603047","160517"],
		["u1603042","160439"],
		["u1603051","160154"],
		["u1603024","160592"],
		["u1603028","160501"],
		["u1603017","160176"]]
#creds=[["u1503162","15584"],["u1503145","15399"]]
local_electives=["2019S6CS-A-CS334","2019S6CS-A-CS368","2019S6CS-A-CS372","2019S6CS-A-CS366"]
global_electives = []
subjects=[]
x=0
while(x<len(creds)):
	payload = {'user': creds[x][0], 'pass': creds[x][1]}
	x+=1
	session = requests.Session()
	r = session.get('https://www.rajagiritech.ac.in/stud/Parent/varify.asp', data=payload)
	##print(r.text)
	#get cookies
	#here the session_cookies dictionary contains only one entry
	#it is the session ID
	session_cookies = session.cookies.get_dict()
	#go to attendance page
	r = requests.post('https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp', cookies=session_cookies)
	##print(r.text)
	#this is the page which displays the dropdown containing the list of semesters
	#the semester code is required to create the url to the page where attendance data is displayed
	#that url is of the form "https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp?code=2019S8CS-C" ...
	#... where 2019S8CS-C is the semester code obtained from the dropdown
	#the last entry in the dropdown is the current semester
	dropdown_page = r.text
	dropdown_list=[]
	#in the html soucrce, every entry in the dropdown is of the form <option value="2015CS-C-S1">2015CS-C-S1</option>
	while(dropdown_page.find("<option value=")!=-1):
			startIndex = dropdown_page.find("<option value=") + len("<option value=")
			endIndex = dropdown_page.find("</option>")
			dropdown_entry=dropdown_page[startIndex:endIndex]
			##print(dropdown_entry)
			dropdown_entry = dropdown_entry[dropdown_entry.find(">")+1:]
			##print("--|"+dropdown_entry+"|--")
			dropdown_list.append(dropdown_entry)
			dropdown_page = dropdown_page[endIndex+1:]
			#print(dropdown_page)

	##print(dropdown_list)
	no_of_semesters = len(dropdown_list)
	current_sem = dropdown_list[no_of_semesters-1]
	#succesfully obtained valid semester codes

	#now we can navigate to the attendance page
	attendance_page_url = "https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp?code="
	#append the current semester code to the url
	attendance_page_url += current_sem
	##print(attendance_page_url)
	#obtain souce of attendance_page_url
	semid_payload = {'code': current_sem}
	r = requests.post('https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp', cookies=session_cookies, data=semid_payload)
	attendance_page = r.text
	##print(attendance_page)

	#collect all useful data from attendance page
	#get the user name
	USERNAME = "Jane Doe"
	name_startIndex = attendance_page.find("Logged In User :")
	if(name_startIndex!=-1):
		focus = attendance_page[name_startIndex:]
		name_startIndex = focus.find("Logged In User :")+len("Logged In User :")
		name_endIndex = focus.find("</div>")
		USERNAME = focus[name_startIndex:name_endIndex]
		#remove leading and trailing whitespaces
		USERNAME = USERNAME.strip()
		#remove multiple spaces
		USERNAME = re.sub(' +', ' ', USERNAME)
		#convert to title case
		USERNAME = USERNAME.title()
		print("--|"+USERNAME+"|--")

	#get index of first entry in table_view
	startIndex = attendance_page.find("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\"")
	endIndex = attendance_page.find("<!-- Detailed Ends***************** -->")
	focus = attendance_page[startIndex:endIndex]
	##print (focus)


	#loop to extract data from table
	startIndex = focus.find("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\" Height=\"35\" Width=\"8%\">")
	while (startIndex!=-1):
		startIndex=startIndex+len("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\" Height=\"35\" Width=\"8%\">")
		endIndex = focus.find("</TD>")
		day=focus[startIndex:endIndex]
		#print(day)
		temp_focus = focus[endIndex+9:focus.find("</TR>")]
		#print(temp_focus)

		start = temp_focus.find("font color")
		day_data=[]
		day_data.append(get_time(day))

		first = day.find("-")
		day_text = day[:first]
		day_int = int(day_text)
		if(day_int<10):
			day="0"+day

		day_data.append(day)

		while(start != -1):
			end = temp_focus.find("</font></TD>")
			line = temp_focus[start:end]
			line = line[line.find(">")+1:]
			'''
			if(line==""):
				line = "-----"
			if(line in local_electives):
				line = "L_ELE"
			else:
				if (line not in subjects):
					subjects.append(line)
			'''
			if(line==""):
				line = "-----"
			if(line in local_electives):
				line = "L_ELE"
			if (line not in subjects):
				subjects.append(line)
			#print(line)
			day_data.append(line)
			temp_focus = temp_focus[end+13:]
			start = temp_focus.find("font color")


		focus = focus[focus.find("</TR>")+10:]
		startIndex = focus.find("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\" Height=\"35\" Width=\"8%\">")

		if(day_data not in days_data):
			days.append(day)
			days_data.append(day_data)
	##sort the days_data
	from operator import itemgetter
	sorted_days_data = sorted(days_data,key=itemgetter(0))

	#display the data
	i = 0
	while(i<len(sorted_days_data)):
		print(sorted_days_data[i])
		i=i+1
	print("--|"+USERNAME+"|--")




#clean the data
clean=[]
i = 0
print("\n\n")


#total array will contain total class data of all subjects
#yay!

total = []
for z in range (len(subjects)):
	total.append(0)

print ("NON_ELECTIVES are :",subjects)
print ("LOCAL_ELECTIVES are :",local_electives)
print ("GLOBAL_ELECTIVES are :",global_electives)
print ("\nALL :",subjects,"\n")

while(i<len(sorted_days_data)):
	#for each entry in sorted_days_data...
	focus_group=[]
	focus_group.append(sorted_days_data[i])
	#find entries with same day info and add it to focus_group
	j=i+1
	while(True):
		if (j >= len(sorted_days_data)):
			break
		if(sorted_days_data[j][1]==sorted_days_data[i][1]):
			focus_group.append(sorted_days_data[j])
			j=j+1
		else:
			break

	out = focus_group[0]
	if(len(focus_group)==1):
		donothing=0
		##print(">>>FOCUS GROUP for "+sorted_days_data[i][1]+" is ")
		##print("\t",focus_group[0])
	else:
		##print("---FOCUS GROUP for "+sorted_days_data[i][1]+" is ")
		missing=[]
		for k in range (len(focus_group)):
			##print("\t",focus_group[k])
			if(k == 0):
				for a, b in enumerate(focus_group[k]):
					if (b == '-----'):
						missing.append(int(a))
				##print("missing elements are ",missing)
			else:
				for l in range (len(missing)):
					if (focus_group[k][missing[l]]!="-----"):
						out[missing[l]] = focus_group[k][missing[l]]

	print("OUT IS->",out)
	#add to total class of each class in out
	p=2
	while (p<len(out)):
		ind = subjects.index(out[p])
		total[ind] = total[ind] + 1
		p = p + 1

	clean.append(out)
	i=j

print("\n")

#writing final details of hour count into a file
count_file = open("ttcount.txt","w")

for i in range (len(subjects)):
	print (subjects[i],"--",total[i])
	count_file.write("%s %s\n" %(subjects[i], total[i]))

count_file.close()
#closing the previously opened file

timetable = [
	['CS302', 'CS332', 'CS332', 'CS332', 'L_ELE', 'HS300', 'S_EPM'],
	['L_ELE', 'HS300', 'CS308', 'CS302', 'CS334', 'CS334', 'CS334'],
	['CS306', 'CS304', 'CS302', 'CS306', 'LIBRY', 'CS304', 'CS302'],
	['L_ELE', 'CS306', 'CS308', 'PT_PT', 'CS308', 'HS300', 'CS308'],
	['CS302', 'CS302', 'CS306', 'CS308', 'CS352', 'CS352', 'AH_AH']
	]

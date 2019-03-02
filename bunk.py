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
u_id="u1603033"
pass_word="160348"



print("\n .______    __    __  .__   __.  __  ___      ___      .______    __       _______\n |   _  \\  |  |  |  | |  \\ |  | |  |/  /     /   \\     |   _  \\  |  |     |   ____|\n |  |_)  | |  |  |  | |   \\|  | |  '  /     /  ^  \\    |  |_)  | |  |     |  |__   \n |   _  <  |  |  |  | |  . `  | |    <     /  /_\\  \\   |   _  <  |  |     |   __|  \n |  |_)  | |  `--'  | |  |\\   | |  .  \\   /  _____  \\  |  |_)  | |  `----.|  |____ \n |______/   \\______/  |__| \\__| |__|\\__\\ /__/     \\__\\ |______/  |_______||_______|")


print("  _______ .__   __.  _______       _______      ___      .___  ___.  _______\n |   ____||  \\ |  | |       \\     /  _____|    /   \\     |   \\/   | |   ____| \n |  |__   |   \\|  | |  .--.  |   |  |  __     /  ^  \\    |  \\  /  | |  |__ \n |   __|  |  . `  | |  |  |  |   |  | |_ |   /  /_\  \   |  |\/|  | |   __|\n |  |____ |  |\\   | |  '--'  |   |  |__| |  /  _____  \\  |  |  |  | |  |____\n |_______||__| \\__| |_______/     \\______| /__/     \\__\\ |__|  |__| |_______|")
print("\n***************************** AUTHOR : AMAL DINESH *****************************")



print("\n")
u_id=input("\t\t\t   \tENTER UID: ")
pass_word=input("\t\t\t   \tENTER PASSWORD: ")

creds=[
		[u_id,pass_word]]
#creds=[["u1503162","15584"],["u1503145","15399"]]
local_electives=["2019S6CS-A-CS334","2019S6CS-A-CS368","2019S6CS-A-CS372","2019S6CS-A-CS366"]
global_electives = []
subjects=[]
subjects_new=[]
total_new=[]
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
		print("\n\t\t\t\t--|"+USERNAME+"|--\n")

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
	#print("\t\t\t\t--|"+USERNAME+"|--")




#clean the data
clean=[]
i = 0
#print("\n\n")


#total array will contain total class data of all subjects
#yay!

total = []
for z in range (len(subjects)):
	total.append(0)

#print ("NON_ELECTIVES are :",subjects)
#print ("LOCAL_ELECTIVES are :",local_electives)
#print ("GLOBAL_ELECTIVES are :",global_electives)
#print ("\nALL :",subjects,"\n")

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

	#print("OUT IS->",out)
	#add to total class of each class in out
	p=2
	while (p<len(out)):
		ind = subjects.index(out[p])
		total[ind] = total[ind] + 1
		p = p + 1

	clean.append(out)
	i=j

#print("\n")

#writing the absent hour count of a single person to a file
count_file_one = open("single_one_count.txt","w")

for i in range (len(subjects)):
	count_file_one.write("%s %s %s\n" %(subjects[i], "--", total[i]))

count_file_one.close()
#closing the previously opened file - single-one-count

splitted=[]
hour_count_file = open("ttcount.txt","r")

hour_count = hour_count_file.readlines()
for i in range(13):
	splitted.append(hour_count[i].split(" "))
for i in range(13):
	splitted[i][1]=splitted[i][1].replace("\n", "")
hour_count_file.close()
#closing the previously opened file - ttcount

print ("\n")
print("----------------------------------ATTENDANCE----------------------------------")

print("\n\t\t\t       WELCOME "+USERNAME+"   \n")
print("** You have 100% attendance for the subject which are not displayed below ** ")
print("** Attendance of Elective subjects will not be available here ** \n")
for i in range(len(subjects)):
	for j in range(13):
		if subjects[i] == splitted[j][0] :
			percent = 100-((total[i]/int(splitted[j][1]))*100)
			if subjects[i] != "-----" and subjects[i] != "CS362" and subjects[i] != "CS368" and subjects[i] != "CS372" and subjects[i] != "CS366" :
				if subjects[i] == "CS302":
					print("DAA", "-->", "%.2f" %percent)
				if subjects[i] == "CS304":
					print("CD", "-->", "%.2f" %percent)
				if subjects[i] == "CS306":
					print("CN", "-->", "%.2f" %percent)
				if subjects[i] == "CS308":
					print("SEPM", "-->", "%.2f" %percent)
				if subjects[i] == "HS300":
					print("POM", "-->", "%.2f" %percent)
				if subjects[i] == "CS332":
					print("MP LAB", "-->", "%.2f" %percent)
				if subjects[i] == "CS334":
					print("NW LAB", "-->", "%.2f" %percent)
				if subjects[i] == "CS352":
					print("COMPREHENSIVE", "-->", "%.2f" %percent)


timetable = [
	['CS302', 'CS332', 'CS332', 'CS332', 'L_ELE', 'HS300', 'S_EPM'],
	['L_ELE', 'HS300', 'CS308', 'CS302', 'CS334', 'CS334', 'CS334'],
	['CS306', 'CS304', 'CS302', 'CS306', 'LIBRY', 'CS304', 'CS302'],
	['L_ELE', 'CS306', 'CS308', 'PT_PT', 'CS308', 'HS300', 'CS308'],
	['CS302', 'CS302', 'CS306', 'CS308', 'CS352', 'CS352', 'AH_AH']
	]

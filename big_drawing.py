from turtle import color
import matplotlib.pyplot as plt
import mysql.connector


mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database = "pszproject"
        #password="mypassword"
    )
mycursor = mydb.cursor()


#a - 10 lokacija sa najvise automobila 
mycursor.execute("select DISTINCT lokacija FROM big_kola")
locations = mycursor.fetchall()
locations_names_and_counters = []
for location in locations:
    if(location[0]==""):
        continue
    #code to include the unknown location
    # location_name = ""
    # if(location[0]==""):
    #     location_name ="Nepoznato"
    # else:
    #     location_name =(location[0])
    mycursor.execute("select COUNT(*) from big_kola where lokacija ='"+location[0]+"'")
    locations_car_counter = mycursor.fetchone()[0]
    locations_names_and_counters.append((locations_car_counter, location[0] )) #location_name - use this one instead of 
    #location[0] if counting the unknown ones

#now sort the array and pop the rest
locations_names_and_counters = sorted(locations_names_and_counters, key=lambda tup: tup[0], reverse=True)
while len(locations_names_and_counters) > 10:
    locations_names_and_counters.pop()
#draw them
fig = plt.figure(figsize = (10, 5))
location_names = []
location_counters = []
for tuple in locations_names_and_counters:
    location_counters.append(tuple[0])
    location_names.append(tuple[1])

plt.bar(location_names, location_counters, color ='lightgreen',
        width = 0.4)
plt.xlabel("Lokacije")
plt.ylabel("Broj automobila")
plt.title("Broj ponudjenih automobila po lokacijama")
plt.show()

#b BROJ AUTOMOBILA, ZNACI LEN od nizova printas
under50k = 0
under100k = 0
under150k = 0
under200k = 0
under250k = 0
under300k = 0
over300k = 0
#50k
mycursor.execute("select count(*) from big_kola where kilometraza < 50000")
under50k = mycursor.fetchone()[0]
#100k
mycursor.execute("select  count(*) from big_kola where kilometraza between 50000 and 100000")
under100k = mycursor.fetchone()[0]
#150k
mycursor.execute("select  count(*) from big_kola where kilometraza between 100000 and 150000")
under150k = mycursor.fetchone()[0]
#200k
mycursor.execute("select  count(*) from big_kola where kilometraza between 150000 and 200000")
under200k = mycursor.fetchone()[0]
#250k
mycursor.execute("select  count(*) from big_kola where kilometraza between 200000 and 250000")
under250k = mycursor.fetchone()[0]
#300k
mycursor.execute("select count(*) from big_kola where kilometraza between 250000 and 300000")
under300k = mycursor.fetchone()[0]
#300k+
mycursor.execute("select  count(*) from big_kola where kilometraza > 300000")
over300k = mycursor.fetchone()[0]
#draw them

values = []
values.append(under50k)
values.append(under100k)
values.append(under150k)
values.append(under200k)
values.append(under250k)
values.append(under300k)
values.append(over300k)
keys = []
keys.append("Under 50")
keys.append("50-100")
keys.append("100-150")
keys.append("150-200")
keys.append("200-250")
keys.append("250-300")
keys.append("over 300")

plt.bar(keys, values, color ='blue',
        width = 0.9)
plt.xlabel("Opsezi predjene kilometraze")
plt.ylabel("Broj automobila")
plt.title("Broj ponudjenih automobila po predjenom broju kilometara [1000]")
plt.show()


#c broj automobila po godinama
before60s = 0
before70s = 0
before80s = 0
before90s = 0
before00s = 0
before05 = 0
before10s = 0
before15 = 0
before20 = 0
after20s = 0
#50s
mycursor.execute("select count(*) from big_kola where godiste < 1960")
before60s = mycursor.fetchone()[0]
#60s
mycursor.execute("select count(*) from big_kola where godiste between 1961 and 1970")
before70s = mycursor.fetchone()[0]
#70s
mycursor.execute("select count(*) from big_kola where godiste between 1971 and 1980")
before80s = mycursor.fetchone()[0]
#80s
mycursor.execute("select count(*) from big_kola where godiste between 1981 and 1990")
before90s = mycursor.fetchone()[0]
#90s
mycursor.execute("select count(*) from big_kola where godiste between 1991 and 2000")
before00s = mycursor.fetchone()[0]
#00-05
mycursor.execute("select count(*) from big_kola where godiste between 2001 and 2005")
before05 = mycursor.fetchone()[0]
#05-10
mycursor.execute("select count(*) from big_kola where godiste between 2006 and 2010")
before10s = mycursor.fetchone()[0]
#10-15
mycursor.execute("select count(*) from big_kola where godiste between 2011 and 2015")
before15 = mycursor.fetchone()[0]
#15-20
mycursor.execute("select count(*) from big_kola where godiste between 2016 and 2020")
before20 = mycursor.fetchone()[0]
#after 2020
mycursor.execute("select count(*) from big_kola where godiste > 2020")
after20s = mycursor.fetchone()[0]
#draw them
values = []
values.append(before60s)
values.append(before70s)
values.append(before80s)
values.append(before90s)
values.append(before00s)
values.append(before05)
values.append(before10s)
values.append(before15)
values.append(before20)
values.append(after20s)
keys = []
keys.append("Old")
keys.append("60s")
keys.append("70s")
keys.append("80s")
keys.append("90")
keys.append("00-05")
keys.append("05-10")
keys.append("10-15")
keys.append("15-20")
keys.append("New")

plt.bar(keys, values, color ='red',
        width = 0.4)
plt.xlabel("Vremenski periodi")
plt.ylabel("Broj automobila")
plt.title("Broj ponudjenih automobila po periodu proizvodnje")
plt.show()

#d - brojevi i procentualni odnos automatskog i manuelnog menjaca


mycursor.execute("select count(*) from big_kola where menjac = 'manuelni'")
cnt_manual = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where menjac = 'automatski'")
cnt_auto = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where menjac like '%oluautomatski'")
cnt_semi_auto = mycursor.fetchone()[0]
mycursor.execute("SELECT count(*) from big_kola")
cnt_all = mycursor.fetchone()[0]
#draw it
values = []
values.append(cnt_manual)
values.append(cnt_auto)
values.append(cnt_semi_auto)
keys = []
keys.append("Manuelni")
keys.append("Automatski")
keys.append("Poluautomatski")

plt.bar(keys, values, color ='grey',
        width = 0.4)
bar_labels = []
bar_labels.append(str(round(cnt_manual*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(cnt_auto*100/cnt_all, 2))+"%")
bar_labels.append(str(round(cnt_semi_auto*100/cnt_all, 2))+"%")
bar_container = plt.barh(values, keys, height=0)
iterator = 0
for bar in bar_container.patches:
    plt.text(bar.get_width()-0.1, bar.get_y() +1,
        bar_labels[iterator], fontsize = 8, color='black'
    )
    iterator+=1
#plt.bar_label(container=bar_container) #,labels=bar_labels
plt.xlabel("Vrste menjaca")
plt.ylabel("Broj automobila")
plt.title("Broj i procenat ponudjenih automobila po tipu menjaca")
plt.show()


#e - broj i procenat automobila po opsegu cena
mycursor.execute("select count(*) from big_kola where cena < 2000")
below2k = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where cena between 2000 and 4999")
below5k = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where cena between 2000 and 9999")
below10k = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where cena between 10000 and 14999")
below15k = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where cena between 15000 and 19999")
below20k = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where cena between 20000 and 24999")
below25k = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where cena between 25000 and 29999")
below30k = mycursor.fetchone()[0]
mycursor.execute("select count(*) from big_kola where cena >= 30000")
over30k = mycursor.fetchone()[0]
mycursor.execute("SELECT count(*) from big_kola")
cnt_all = mycursor.fetchone()[0]
#draw them
values = []
values.append(below2k)
values.append(below5k)
values.append(below10k)
values.append(below15k)
values.append(below20k)
values.append(below25k)
values.append(below30k)
values.append(over30k)
keys = []
keys.append("Ispod 2")
keys.append("2-5")
keys.append("5-10")
keys.append("10-15")
keys.append("15-20")
keys.append("20-25")
keys.append("25-30")
keys.append("Preko 30")


plt.bar(keys, values, color ='orange',
        width = 0.4)
bar_labels = []
bar_labels.append(str(round(below2k*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(below5k*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(below10k*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(below15k*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(below20k*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(below25k*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(below30k*100/cnt_all, 2)) +"%")
bar_labels.append(str(round(over30k*100/cnt_all, 2)) +"%")


bar_container = plt.barh(values, keys, height=0)
iterator = 0
for bar in bar_container.patches:
    plt.text(bar.get_width()-0.2, bar.get_y() +1,
        bar_labels[iterator], fontsize = 8, color='brown'
    )
    iterator+=1
#plt.bar_label(container=bar_container) #,labels=bar_labels
plt.xlabel("Cena automobila [1000]")
plt.ylabel("Broj automobila")
plt.title("Broj i procenat ponudjenih automobila po ceni izrazeno u hiljadama evra")
plt.show()

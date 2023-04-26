import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import mysql.connector
import random

#connect to the db
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database = "pszproject"
        #password="mypassword"
    )
mycursor = mydb.cursor()

#shall be called only once
def complete_the_data():
    #postavljam najzastupljenije boje
    mycursor.execute("Select id from big_kola where boja = ''")
    result_set = mycursor.fetchall()
    for result in result_set:
        id = result[0]
        color = ""
        n = random.randint(0,2)
        if n == 0:
            color = 'bela'
        elif n ==1:
            color = 'siva'
        elif n ==2:
            color = 'crna'
        #nesto zeza sa pripremom upita, ali kako je lokalni upit, ne brinem se za injekciju
        sql = "update big_kola set boja = '"+color+"' where id = " + str(id)
        mycursor.execute(sql)
        mydb.commit()
    #postavljam vrednost menjaca random
    mycursor.execute("Select id from big_kola where menjac = ''")
    result_set = mycursor.fetchall()
    for result in result_set:
        id = result[0]
        menjac = ""
        n = random.randint(0,1)
        if n == 0:
            menjac = 'manuelni'
        elif n ==1:
            menjac = 'automatski'
        #nesto zeza sa pripremom upita, ali kako je lokalni upit, ne brinem se za injekciju
        sql = "update big_kola set menjac = '"+menjac+"' where id = " + str(id)
        mycursor.execute(sql)
        mydb.commit()
    #vidi da li za karoseriju
    #cena
    mycursor.execute("Select id from big_kola where cena is NULL")
    result_set = mycursor.fetchall()
    mycursor.execute("SELECT AVG(cena) FROM big_kola")
    avg_cena = mycursor.fetchone()[0]
    avg_cena = round(avg_cena)
    for result in result_set:
        id = result[0]
        #nesto zeza sa pripremom upita, ali kako je lokalni upit, ne brinem se za injekciju
        sql = "update big_kola set cena = "+str(avg_cena)+" where id = " + str(id)
        mycursor.execute(sql)
        mydb.commit()





#data preparation
def prep_data(marke_nazivi, marke_vrednosti, karoserija_nazivi, karoserija_vrednosti): #karoserija_nazivi, karoserija_vrednosti, boja_nazivi, boja_vrednosti, menjac_nazivi, menjac_vrednosti
    #dohvatanje marki i prebacivanje vrednosti iz tekstualne u numericku
    mycursor.execute("select DISTINCT marka FROM big_kola")
    marke = mycursor.fetchall()
    for i in range(len(marke)):
        marke_nazivi.append(marke[i][0])
        marke_vrednosti.append(i)
    #isto, ali za manje vazne parametre
    mycursor.execute("select DISTINCT karoserija FROM big_kola")
    karoserija = mycursor.fetchall()
    for i in range(len(karoserija)):
        karoserija_nazivi.append(karoserija[i][0])
        karoserija_vrednosti.append(i)
    # mycursor.execute("select DISTINCT boja FROM big_kola")
    # boje = mycursor.fetchall()
    # for i in range(len(boje)):
    #     boja_nazivi.append(boje[i][0])
    #     boja_vrednosti.append(str(i))
    # mycursor.execute("select DISTINCT menjac FROM big_kola")
    # menjaci = mycursor.fetchall()
    # for i in range(len(menjaci)):
    #     menjac_nazivi.append(menjaci[i][0])
    #     menjac_vrednosti.append(str(i))
    
def data_regulation(marke_nazivi, marke_vrednosti, karoserija_nazivi, karoserija_vrednosti, initial_dataset):
    #da ne racunam stalno
    broj_marki = len(marke_nazivi)
    for i in range(len(initial_dataset)):
        for j in range(broj_marki):
          if initial_dataset[i][0] == marke_nazivi[j]:
                initial_dataset[i] = (marke_vrednosti[j], initial_dataset[i][1], initial_dataset[i][2], initial_dataset[i][3] ,initial_dataset[i][4], initial_dataset[i][5], initial_dataset[i][6])
        for j in range(len(karoserija_nazivi)):
            if(initial_dataset[i][5]==karoserija_nazivi[j]):
                initial_dataset[i] = (initial_dataset[i][0], initial_dataset[i][1], initial_dataset[i][2], initial_dataset[i][3] ,initial_dataset[i][4], karoserija_vrednosti[j], initial_dataset[i][6])
    


#call it once for the whole set, before separating
def data_scaling(set, max_values):
    for i in range(len(set)):
        if(set[i][0] > max_values[0]):
            max_values[0] = set[i][0]
        if(set[i][1] > max_values[1]):
            max_values[1] = set[i][1]
        if(set[i][2] > max_values[2]):
            max_values[2] = set[i][2]
        if(set[i][3] > max_values[3]):
            max_values[3] = set[i][3]
        if(set[i][4] > max_values[4]):
            max_values[4] = set[i][4]
        if(set[i][5] > max_values[5]):
            max_values[5] = set[i][5]
        if(set[i][6] > max_values[6]):
            max_values[6] = set[i][6]
    
    for i in range(len(set)):
        new_tuple = (set[i][0]/max_values[0] ,set[i][1]/max_values[1],set[i][2]/max_values[2] ,set[i][3]/max_values[3],set[i][4]/max_values[4]
        ,set[i][5]/max_values[5], set[i][6]/max_values[6])
        set[i] = new_tuple
#marka, kubikaza/100, kilometraza/1000, godiste, snaga, karoserija | boja, menjac
#cena/100 - BICE 100 puta manja na izlazu, to dovijeno mnozis sa 100

marke_nazivi = []
marke_vrednosti = []

karoserija_nazivi = []
karoserija_vrednosti = []

# boja_nazivi = []
# boja_vrednosti = []

# menjac_nazivi = []
# menjac_vrednosti = []

#complete_the_data()

prep_data(marke_nazivi, marke_vrednosti, karoserija_nazivi, karoserija_vrednosti)#, karoserija_nazivi, karoserija_vrednosti, boja_nazivi, boja_vrednosti, menjac_nazivi, menjac_vrednosti
#data fetching
mycursor.execute('select marka, kubikaza, kilometraza, godiste, snaga, karoserija, cena from big_kola')
initial_dataset = mycursor.fetchall()
#data regulation
data_regulation(marke_nazivi, marke_vrednosti, karoserija_nazivi, karoserija_vrednosti, initial_dataset)
#data scaling
max_values = [0,0,0,0,0,0,0]#to remember what to multiply the later results with
data_scaling(initial_dataset, max_values)

print('max values', max_values)
#marka, kubikaza, kilometraza, godiste, snaga, karoserija | boja, menjac
#cena - izlaz
#initialize vectors
w = [0, 0.2, 0, -0.8, 0.8, 0.2, 0.0]#w0, w1, w2, w3, w4, w5, w6
temp_w = [0, 0, 0, 0, 0, 0, 0]
#0.1 or 0.01
a = 0.05
# # w = w0,w1...wn
# # x = 1, x0, x1, x2, x3, x4 | y =x5
#shuffle the data, and choose train and test sets
price_position = len(initial_dataset[0]) - 1
random.shuffle(initial_dataset)
train_set = []
test_set = []
data_perc = 0.7#percentage for the training set
separating_index = round(len(initial_dataset)*0.8)

for i in range(len(initial_dataset)):
    if i < separating_index:
        train_set.append(initial_dataset[i])
    else:
        test_set.append(initial_dataset[i])

def h(x):
    sum = 0
    for i in range(price_position+1): #dakle, 7, odnosno len(bilo koje x)
        if i==0:
            sum+=w[0]*1
        else:
            sum+=w[i]*x[i-1]
    
    #print("sum: ", sum)
    return sum

def cost(set):
    sum = 0
    for i in range (len(set)):
        sum = sum + (h(set[i]) - set[i][price_position])**2
    sum = sum/2
    sum = sum/len(set)
    return sum

def descent(set):
    prim_values = []
    for i in range(len(w)):
        sum = 0
        for j in range(len(set)):
            temp_val = (h(set[i]) - set[j][price_position])
            if(i!=0):
                temp_val*=set[j][i-1]
            sum+=temp_val
        prim_values.append(sum/len(set))
        sum = sum/len(set) #izvod po Wi
        sum*=a
        # print('suma ', sum)
        temp_w[i] = w[i] - sum
    
    for i in range(len(w)):
        #print(temp_w[i])
        w[i] = temp_w[i]

    return prim_values
    

def train_a_set(set):
    i = 0
    prim_values = [1, 1 ,1 ,1,1,1, 1]
    while (abs(prim_values[0]) > 0.000001 and abs(prim_values[1]) > 0.000001  
     and abs(prim_values[2]) > 0.000001   and abs(prim_values[3]) > 0.000001 
     and abs(prim_values[4]) > 0.000001  and abs(prim_values[5]) > 0.000001 
     and abs(prim_values[6]) > 0.000001):
        prim_values = descent(set)
        i+=1
        # print("i: ", i)
        # print('prim values: ', prim_values)
        # print("w: ", w)
    
train_a_set(train_set)

#predict
predictions = []
true_values = []
for i in range(len(test_set)):
    predictions.append(h(test_set[i])*max_values[price_position])
    true_values.append(test_set[i][price_position]*max_values[price_position])
train_set_true_values = []
for i in range(len(train_set)):
    train_set_true_values.append(train_set[i][price_position]*max_values[price_position])
    #print(train_set_true_values)

#rezultati
for i in range(1000):
    print("Predikcija: " + str(predictions[i])+" / Stvarna vrednost: " + str(true_values[i]))

print("w: ", w)

# plt.scatter(predictions, true_values)
# # plt.plot(train_set_true_values, predictions, color = 'blue', linewidth = 5)
# plt.show()

# descent(train_set)
# descent(train_set)
# descent(train_set)
# j(w) = 1/2m SUMA(h(x[i] - yi)^2)
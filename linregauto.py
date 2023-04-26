import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import mysql.connector
import random
import seaborn as sb

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
def prep_data(marke_nazivi, marke_vrednosti): #karoserija_nazivi, karoserija_vrednosti, boja_nazivi, boja_vrednosti, menjac_nazivi, menjac_vrednosti
    #dohvatanje marki i prebacivanje vrednosti iz tekstualne u numericku
    mycursor.execute("select DISTINCT marka FROM big_kola")
    marke = mycursor.fetchall()
    for i in range(len(marke)):
        marke_nazivi.append(marke[i][0])
        marke_vrednosti.append(i)
    #isto, ali za manje vazne parametre
    # mycursor.execute("select DISTINCT karoserija FROM big_kola")
    # karoserija = mycursor.fetchall()
    # for i in range(len(karoserija)):
    #     karoserija_nazivi.append(karoserija[i][0])
    #     karoserija_vrednosti.append(str(i))
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
    
def data_regulation(marke_nazivi, marke_vrednosti, initial_dataset): #za jos dinamike stavi da marke nisu fiksno 0,
                                                                     #vec prosledi i poziciju polja
    #da ne racunam stalno
    broj_marki = len(marke_nazivi)
    for i in range(len(initial_dataset)):
        for j in range(broj_marki):
          if initial_dataset[i][0] == marke_nazivi[j]:
                #OVO JE AKO NEMAM MARKU
                #initial_dataset[i][0] = marke_vrednosti[j]
                #AKO IMAM MARKU
                initial_dataset[i] = (marke_vrednosti[j], initial_dataset[i][1], initial_dataset[i][2], initial_dataset[i][3] ,initial_dataset[i][4], initial_dataset[i][5])

        #print(initial_dataset[i])

#call it once for the whole set, before separating
def data_scaling(set, max_values):
    for i in range(len(set)):
        for j in range(len(set[i])):
            if(set[i][j] > max_values[j]):
                max_values[j] = set[i][j]

    
    for i in range(len(set)):
        #scale the data, also change the set from an array of tuples to a matrix
        new_list = []
        for j in range(len(set[i])):
            new_list.append(set[i][j]/max_values[j])
        
        set[i] = new_list
#marka, kubikaza/100, kilometraza/1000, godiste, snaga, | karoserija, boja, menjac
#cena/100 - BICE 100 puta manja na izlazu, to dovijeno mnozis sa 100

marke_nazivi = []
marke_vrednosti = []

# karoserija_nazivi = []
# karoserija_vrednosti = []

# boja_nazivi = []
# boja_vrednosti = []

# menjac_nazivi = []
# menjac_vrednosti = []

#complete_the_data()

prep_data(marke_nazivi, marke_vrednosti)#, karoserija_nazivi, karoserija_vrednosti, boja_nazivi, boja_vrednosti, menjac_nazivi, menjac_vrednosti
#data fetching
mycursor.execute('select marka, kubikaza,  kilometraza, godiste,snaga , cena from big_kola') # godiste .....snaga, izmedju godista i cene
initial_dataset = mycursor.fetchall()
#data regulation
data_regulation(marke_nazivi, marke_vrednosti, initial_dataset)
#data scaling
max_values = []#to remember what to multiply the later results with
for i in range(len(initial_dataset[0])): #broj polja u torki
    max_values.append(0)
data_scaling(initial_dataset, max_values)

print('max values', max_values)
# for i in range(20):
#     print(initial_dataset[i])
#marka, kubikaza, kilometraza, godiste, snaga, | karoserija, boja, menjac
#cena - BICE 100 puta manja na izlazu, to dovijeno mnozis sa 100

#initialize vectors
w = []#w0, w1, w2, w3, w4, w5, w6
temp_w = []
for i in range(len(initial_dataset[0])): #broj polja u, sada nizu
    #w.append(0 + random.randint(-10, 10)/10)
    w.append(0)
    temp_w.append(w[i])


print(w)
#0.1 or 0.01
a = 0.8
# # w = w0,w1...wn
# # x = 1, x0, x1, x2, x3, x4 | y =x5
#shuffle the data, and choose train and test sets
price_position = len(initial_dataset[0]) - 1
random.shuffle(initial_dataset)
train_set = []
test_set = []
data_perc = 0.8#percentage for the training set
separating_index = round(len(initial_dataset)*data_perc)

for i in range(len(initial_dataset)):
    if i < separating_index:
        train_set.append(initial_dataset[i])
    else:
        test_set.append(initial_dataset[i])

def RMSE(set):
    sum = 0
    for i in range (len(set)):
        sum = sum + (h(set[i]) - set[i][price_position])**2
    sum = sum/len(set)
    sum**(1/2)
    return sum

def h(x):
    sum = 0
    for i in range(len(x)):
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

def descent(set, a):
    prim_values = []
    for i in range(len(w)):
        sum = 0
        for j in range(len(set)):
            temp_val = (h(set[j]) - set[j][price_position])
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

def stohastic_descent(set, a):
    random.shuffle(set)
    for i in range(len(set)):
        prim_values = []
        for j in range(len(w)):
            current_w = h(set[i]) - set[i][price_position]
            if(j!=0):
                current_w*=set[i][j-1]
            prim_values.append(current_w)
            current_w*=a
            current_w/=len(set)
            temp_w[j] = current_w
        for k in range(len(w)):
            w[k] =temp_w[k]
        a*=0.9
    return prim_values

    

def train_a_set(set, cost_arr, iteration_arr):
    i = 0
    prim_values = [1, 1, 1]
    while (#(abs(prim_values[1]) > 0.00001 or abs(prim_values[2]) > 0.00001 ) and
     i < 20000 ): 
        prev_prim_values = []
        for j in range(len(prim_values)):
            prev_prim_values.append(prim_values[j])    
        #DESCEND
        prim_values = descent(set, a)
        i+=1

        cost_arr.append(cost(set))
        iteration_arr.append(i)


        # print("i: ", i)
        # print('prim values: ', prim_values)
        # print("w: ", w)
        
        #print('prim values: ', prim_values)

        #check if started overfitting to avoid diverging
        # for j in range(len(prim_values)):
        #     if abs(prim_values[j]) > abs(prev_prim_values[j]):
        #         if prim_values[j] > 0 and prev_prim_values[j] > 0:
        #             prim_values[j]-=0.001
        #         elif prim_values[j] < 0 and prev_prim_values[j] < 0:
        #             prim_values[j]+=0.001

cost_arr = []
iteration_arr = []
train_a_set(train_set, cost_arr, iteration_arr)

#crtanje fje greske
plt.scatter(iteration_arr, cost_arr)
plt.show()

#predict
predictions = []
true_values = []
#true values variant
for i in range(len(test_set)):
    predictions.append(h(test_set[i])*max_values[len(max_values)-1])
    true_values.append(test_set[i][len(max_values)-1]*max_values[len(max_values)-1])
train_set_true_values = []
train_set_predictions = []
for i in range(len(train_set)):
    train_set_predictions.append(h(train_set[i])*max_values[len(max_values)-1])
    train_set_true_values.append(train_set[i][len(max_values)-1]*max_values[len(max_values)-1])
    #print(train_set_true_values)


#rezultati
for i in range(100):
    print("Predikcij testa: " + str(predictions[i])+" / Stvarna vrednost: " + str(true_values[i]))
for i in range(100):
    print("Predikcij traina: " + str(train_set_predictions[i])+" / Stvarna vrednost: " + str(train_set_true_values[i]))

print("w: ", w)

print("RMSE - train: ", RMSE(train_set))
print("RMSE - test: ", RMSE(test_set))

#ovde su x i y jednodimenzionalni nizovi, znaci ja moram da iscrtam grafik
#za svaki atribut pojedinacno, odnosno za svaki pravim niz, pa crtam grafik
# plt.scatter(x_train,y_train)
# plt.plot(x_train, model.predict(x_train.to_numpy().reshape(-1,1)), color='blue', linewidth=5)
#predictions, true_values i train_set true values su vrednosti predikcija, cene test seta i cene trening seta

# 3D CRTANJE - VAZI ZA KILOMETRAZU i GODISTE - CENA
# from mpl_toolkits.mplot3d import Axes3D 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# to_plot = [] # - smenjuju se x1, x2...xn
# for i in range (len(train_set[0]) - 1): #po atributu, osim izlaznog
#     exact_attr = []
#     for j in range(len(train_set)): #po objektu
#         exact_attr.append(train_set[j][i] * max_values[i])
#     to_plot.append(exact_attr)

# ax.scatter(to_plot[0], to_plot[1], train_set_true_values)
# ax.set_xlabel("Kilometraza")
# ax.set_ylabel("Godiste")
# ax.set_zlabel("Cena")

# plt.show()

#2d crtanje - 1 atribut utice samo
# exact_attr = []
# for j in range(len(train_set)): #po objektu
#     exact_attr.append(train_set[j][0] * max_values[0])


# plt.scatter(exact_attr,train_set_true_values)
# plt.plot(exact_attr, train_set_predictions)
# plt.show()



# #crtanje sa seabornom
# to_plot = [] # - smenjuju se x1, x2...xn
# for i in range (len(train_set[0]) - 1): #po atributu, osim izlaznog
#     exact_attr = []
#     for j in range(len(train_set)): #po objektu
#         exact_attr.append(train_set[j][i] * max_values[i])
#     to_plot.append(exact_attr)

# sb.scatterplot(to_plot[0], to_plot[1], hue=train_set_true_values)

# plt.show()

#coefficient of determinance
def R_squared(set):
    rss = 0
    mean_price = 0
    for i in range(len(set)):
        rss = rss + (h(set[i]) - set[i][price_position])**2
        mean_price+=set[i][price_position]
    mean_price/=len(set)
    print('mean price', mean_price * max_values[price_position])
    tss = 0
    for i in range(len(set)):
        tss+=(set[i][price_position]-mean_price)**2
    print('rss', rss)
    print('tss ', tss)
    return 1 - rss/tss
   
    
print("Coefficient of determinance: ", R_squared(test_set))




#mycursor.execute('select kilometraza, godiste, snaga, cena from big_kola')
# treba mi to_plot, i predikcija nad istim skupom, bilo da su train ili test
#dakle treba mi visedimenzionalno crtanje


# plt.scatter(true_values, predictions, c= 'red')
# plt.plot(true_values, predictions)
# plt.show()

# plt.plot(true_values, predictions, color='blue')
# plt.show()

# descent(train_set)
# descent(train_set)
# descent(train_set)
# j(w) = 1/2m SUMA(h(x[i] - yi)^2)
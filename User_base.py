import sqlite3
import datetime
import time
import Esi
import Killboard
import os


conn = sqlite3.connect("user_data.db")



    
def create_db():
    
    
    cursor = conn.cursor()
    
    cursor.execute(""" CREATE TABLE if not exists user_info (Nickname text,Corporation text,Alliance text,Sec_status float,Ship_Kill int,Solo_Kill int,Ship_Lost int,Gang_Ratio int,ZKillboard_inf int, time_update float, url_zkillb text) """)
    conn.commit()


def check_file_path():
    file_path = os.path.abspath(os.curdir)
    print(file_path)
    print(os.path.abspath(__file__))
    print(os.getcwd())
    full_file_path = file_path + "\\user_data.db"
    print(full_file_path)
    print(os.path.isfile(full_file_path))
    
def insert_data_many(name):
    spisok_user = []

    z =[]
    print(spisok_user)
    
    for l in range(0,len(name)):
        spisok_user.append([])
    
        for i in range(1) :

            x = time.time()
            spisok_user[l].append(name[l][0])
            spisok_user[l].append(x)

    z = spisok_user
    for i in z:
        print(i)



    for i in range(0,len(name)):
   
        cursor.execute("""INSERT INTO user_info VALUES (?,?)""",(z[i][0],z[i][1]))
        
    
    conn.commit()

def insert_data(name):
    cursor = conn.cursor()
    req_data_user = user_req(name)
    print("INSERT NAME ",name)
    #print(req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],sep = '\n')
    cursor.execute("""INSERT INTO user_info VALUES (?,?,?,?,?,?,?,?,?,?,?)""",(req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],time.time(),req_data_user[9]))
    conn.commit()
    return req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8]
    cursor.close()            

    
def del_data():
    cursor = conn.cursor()
    sql = "DELETE FROM user_info"
    cursor.execute(sql)
    conn.commit()
    cursor.close()

def search_nicknames(name):
    cursor = conn.cursor()
    sql = "SELECT * FROM user_info WHERE Nickname = ? "
    search_data_update = []
    print("search_nicknames ",name)
    
    
    
    cursor.execute(sql, (name,))  
    #print(name[i])
    
    result =   cursor.fetchall()
    cursor.close()
    #print("Fetachall: ", result)
    if result  == []:
        print("ISNERT")
        return insert_data(name)
         

##        if cursor.fetchall() == []:
##            print(name[i])
##            print(cursor.fetchall())
##            cursor.execute("""INSERT INTO testdb VALUES (?)""",name[i],datetime.datetime.now())
##            conn.commit()
    if result != []:

        print("Есть в БД", name,result[0][9])
       
        if (time.time() - result[0][9]) > 1800 or result[0][1] == "ERROR":

            print("Последний раз обновлялся ",time.ctime(result[0][9]) ," ", result[0][1],result[0][2])
            print(time.ctime(time.time()))
##            print("Обновимся?")
            
            #search_data_update.append(name[i])
            
            return update_data(name)

##        elif result[0][1] == "ERROR":
##            print("В ПОСЛЕДНИЙ РАЗ ПРОИЗОШЛА ОШИБКА")
##            return update_data(name)
        else:
            print("рановато " , name)
            
            return result[0]

                
    #print("Время  ",search_data_update)
    #update_data(search_data_update)
    ##    for i in range(0,len(search_dubliacate)):
        
def update_data(name):
    cursor = conn.cursor()
    
#Ben Solomon Carson
    
    print("update_data " , name)
    req_data_user = user_req(name)
   

    #print("UPDATE DATA",req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],time.time(),name[0])
##    sql  = """UPDATE user_info set  Corporation  = ? ,Alliance = ?,Sec_status = ? ,Ship_Kill = ? ,Solo_Kill = ?,Ship_Lost = ?,Gang_Ratio = ? ,ZKillboard_inf = ?, time_update = ?  WHERE Nickname = ?"""
##    timer = time.time()
##    req = (req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],timer,name[0],)

   
    cursor.execute("""UPDATE user_info set Corporation = ? ,Alliance = ?,Sec_status = ? ,Ship_Kill = ? ,Solo_Kill = ?,Ship_Lost = ?,Gang_Ratio = ? ,ZKillboard_inf = ?, time_update = ?  WHERE Nickname == ?""",(req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],time.time(),name))
    try:
        cursor.execute(sql,req)
    except Exception as e:
        print("SQL : " ,e.__class__)

    print("CURSOR", cursor.fetchall() )
    print(cursor.fetchone())
    
    
    #cursor.execute("""UPDATE user_info set Alliance = ?  WHERE Nickname == ?""",(google,(name),))
   
    #name[0]
    conn.commit()
    cursor.close()

    return req_data_user
##    for i in range(0,len(name)):
##        #print(time.time())
##        print(name[i][0])
##        cursor.execute("""UPDATE user_info SET time_update = ? WHERE Nickname = ?""",(time.time(),name[i][0]))
##        conn.commit()
    

def user_req(name):
    user_r = Esi.esi_data()
    user_id = user_r.req_id(name)
    print(user_id)
    if user_id == "ERROR": 
        print("ERROR ",user_id)
        
        
        user_Alliance = "ERROR"
        user_Corporation = "ERROR"
        user_killboard = 0
      
    
    else:
        try:
            id_Affiliation  = user_r.req_userAffiliation(user_id['characters'][0]['id'])
            try:
                id_Alliance =  id_Affiliation[0]['alliance_id']
            except Exception as e:
                print("id_Alliance Ошибка: " ,e.__class__)
                id_Alliance = 0
                print("нет Альянса")
            #print("id Альянс\Корпорация " , id_Affiliation[0]['alliance_id'],"  " ,id_Affiliation[0]['corporation_id'] )
                
                    #print(id_Alliance)
            id_Corporation =   id_Affiliation[0]['corporation_id']                              
                    #print(id_Corporation)
            user_Corporation = user_r.req_Names(id_Corporation)[0]['name'] #
             #print("id Корпорации " +  str(id_Corporation) + " name: " +   user_Corporation)
            print(user_id['characters'])
            if id_Alliance != 0 :
                user_Alliance = user_r.req_Names(id_Alliance)[0]['name']
            else:
                user_Alliance = "Не состоит в альянсе"

        except Exception as e:
            print("Affiliaton Ошибка: " ,e.__class__)
            user_Alliance = "Try again later"
            user_Corporation = "Try again later"
            
            
            
        user_killboard = Killboard.getCharKillboard(user_id['characters'][0]['id'])
            #user_killboard = Killboard.getCharKillboard(2115461525)
            #print(user_killboard.keys())
            
    if user_killboard == 0:
        
        killb_info = 'None'
    else:
        killb_info = str(user_killboard[0]['info'])
        
    if killb_info == 'None' or killb_info == 'none' or killb_info == 'null':
        print("Ник введён не правильно или не добавлен в БД Killboard")
        user_killb_info = 0
        user_secstatus = 0
        user_destroyship = 0
        user_solokill = 0
        user_shiplost = 0
        user_gangratio = 0 
    else:
        user_killb_info = 1
        try:
            #print("Sec status " , user_killboard['info']['secStatus'],sep = '\n',end = '\n')
            user_secstatus =  str("{:.2f}".format(user_killboard[0]['info']['secStatus']))
            #print(user_secstatus)
        except Exception as e:
            print("Ошибка: ", e.__class__)
            user_secstatus = "Нет в БД КБ"        
                
        try:
            #print("Уничтожил",user_killboard['shipsDestroyed'], " кораблей")
            user_destroyship = str(user_killboard[0]['shipsDestroyed'])
            #print("User ", user_destroyship)    
        except Exception as e:
            print("user_destroyship Ошибка:  Уничтожил 0 кораблей" ,e.__class__)
            user_destroyship = 0

        try:
            #print("Уничтожил в одиночку",user_killboard['soloKills'], " кораблей")
            user_solokill = str(user_killboard[0]['soloKills'])
            #print("User ", user_solokill)
        except Exception as e:
            print("User_solokill Ошибка: " ,e.__class__)
            user_solokill = 0            
            
            
        try:
            #print("Потерял: ",user_killboard['shipsLost'], " кораблей")
            user_shiplost = str(user_killboard[0]['shipsLost'])
            #print("Потерял: ", user_shiplost)
        except Exception as e:
            print("User_ship Ошибка: " ,e.__class__)
            user_shiplost = 0
        try:
            #print(user_killboard['gangRatio'])
            user_gangratio = str(user_killboard[0]['gangRatio'])
        except Exception as e :
            print("User_gang Ошибка: " ,e.__class__)
            user_gangratio = 0 
                
    if user_id == "ERROR":
        return [name,user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info]

    else:
        #print("id Альянса " + str(id_Alliance) + " name: " +  user_Alliance)
        print(user_id['characters'][0]['name'],user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info, sep = '  ')
        return [user_id['characters'][0]['name'],user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info,user_killboard[1]]
    
def user_url_req(name):
    cursor = conn.cursor()
    sql = "SELECT * FROM user_info WHERE Nickname = ? "

    
    cursor.execute(sql, (name,))  
    #print(name[i])
    
    result =   cursor.fetchall()
    print("Resultat: " , result[0][10])
    cursor.close()
    return result[0][10]
    
nicknames = [('ANNE MIDNIGHT',),
            ('Awari Berend',),
            ('CMOYIER',) ]


nicknames_test = [('Arctos Bear',),
    ('ANNE MIDNIGHT',),
    ('Berlin Saimon',),
    ('brown drago',),
    ('Cubic Bistot',),
    ('Drexston McDaddy',),
    ('CMOYIER',)
                  ]

#check_database()
#create_db()

#cursor.execute("""UPDATE user_info set Alliance = 102  WHERE Nickname == "Ben Solomon Carson" """)

#cursor.executemany("INSERT INTO testdb VALUES (?)", nicknames)
##name_is = "ANNE MIDNIGHT"
##cursor.execute("SELECT * FROM testdb WHERE Nickname=?",(name_is,))
##print(cursor.fetchall()[0][0])

##for i in cursor.execute("SELECT rowid, * FROM  testdb WHERE Nickname =?"):
##    print(i)

##a = [('Arctos Bear',),]
##print(a[0])
##for i in nicknames_test:
##    search_nicknames(i)
#print("ZZZZ: ",z)
#insert_data(nicknames)


#del_data()
#cursor.execute("""INSERT INTO testdb VALUES ('Eugenii')""")

#create_db()
#conn.commit()




#insert_data("Evgenii")
##for row in cursor.execute("SELECT rowid, * FROM testdb ORDER BY Nickname"):
##    if (time.time() - row[2]) > 1800:
##        print(row[1])
##        print("Время обновиться")
##        print( "%.2f" % ((row[2] - time.time())/60))
##        x = time.time()
##        print(x)
##        cursor.execute("UPDATE testdb SET time_update = ? WHERE Nickname = ?", (x,row[1]))
##        conn.commit()
##    else:
##        print("Время ещё не пришло")
##    #print(time.ctime(row[2]))





##cursor.execute("""SELECT * FROM testdb""")
##
##records = cursor.fetchall()
##print(records)
##for row in records:
##            print("Id: ", row[0])
##            print("Name: ", row[1])
##
##            print("\n")
# Тестовое время 1577454219.533239
##
##conn.commit()

##d= datetime.datetime(2017,2,14,20,10,1)
##
##print(d.year)
##print(d.day)
##print(d.month)
##print(d.hour)
##print(d.minute)
##print(d.second)

##now = datetime.datetime.now()
##
##then = datetime.datetime(2019,12,26,21,17,10)
##
##delta = now - then
##
##
##print(delta.days)
##print(delta.seconds)
##
##
##if delta.total_seconds() > 600:
##    print("Время обновиться")
##else:
##    print("Время ещё не пришло ",then)

##conn.close()
##conn.close()

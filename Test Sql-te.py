import sqlite3
import datetime
import time
import Esi
import Killboard
import os

conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

def create_db():
    
    file_path = os.path.abspath(os.curdir)
    print(file_path)
    print(os.path.abspath(__file__))
    print(os.getcwd())




    
def insert_data_many(name):
    spisok_user = []

    z =[]
    print(spisok_user)

    for l in range(0,len(name)):
        spisok_user.append([])
    
        for i in range(1) :
            print(name[i][0])
            x = time.time()
            spisok_user[l].append(name[l][0])
            spisok_user[l].append(x)
        print(spisok_user)
    z = spisok_user
    for i in z:
        print(i)



    for i in range(0,len(name)):
        print(i)
        print(name[i])
        cursor.execute("""INSERT INTO user_info VALUES (?,?)""",(z[i][0],z[i][1]))
        

    conn.commit()

def insert_data(name):
    req_data_user = user_req(name)
    
    cursor.execute("""INSERT INTO user_info VALUES (?,?,?,?,?,?,?,?,?,?)""",(req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],time.time()))
    conn.commit()
    return req_data_user[0],req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8]
                   

    
def del_data():
    sql = "DELETE FROM user_info"
    cursor.execute(sql)
    conn.commit()

def search_nicknames(name):
    sql = "SELECT * FROM user_info WHERE Nickname=?"
    search_data_update = []
    print("search_nicknames ",name[0])
    
    
    
    cursor.execute(sql, (name))
    conn.commit()

    
    result =   cursor.fetchall()

    if result  == []:
        print("ISNERT")
        return insert_data(name[0])
         


    if result != []:

        print("Есть в БД", name,result[0][9])
       
        if (time.time() - result[0][9]) > 1800:
            print(result[0][9])
            print("Последний раз обновлялся ",time.ctime(result[0][9]))
            print(time.ctime(time.time()))
            print("Обновимся?")
            
            return update_data(name,result)
            
        else:
            
            for i in result[0]:
                print(i,end = '\n')
            
                

        
def update_data(name):
    
    print("update_data " , name[0],"RESULTAT ",result)
    req_data_user = user_req(name[0])
    print("UPDATE DATA",req_data_user)
    cursor.execute("UPDATE user_info SET Corporation = ? ,Alliance = ?,Sec_status = ? ,Ship_Kill = ? ,Solo_Kill = ?,Ship_Lost = ?,Gang_Ratio = ? ,ZKillboard_inf = ?, time_update = ?  WHERE Nickname = ?",(req_data_user[1],req_data_user[2],req_data_user[3],req_data_user[4],req_data_user[5],req_data_user[6],req_data_user[7],req_data_user[8],time.time(),name[0]))
    conn.commit()





def user_req(name):
    user_r = Esi.esi_data()
    user_id = user_r.req_id(name)
    print(user_id)
    if user_id == "ERROR": 
        print(user_id)
        user_id['characters'][0]['name'] = name
        
        user_Alliance = ""
        user_Corporation = ""
        user_killboard == 0
      
    #print("id Альянс\Корпорация " , id_Affiliation[0]['alliance_id'],"  " ,id_Affiliation[0]['corporation_id'] )
    else:
        id_Affiliation  = user_r.req_userAffiliation(user_id['characters'][0]['id'])
        try:
            id_Alliance =  id_Affiliation[0]['alliance_id']
        except Exception as e:
            print("id_Alliance Ошибка: " ,e.__class__)
            id_Alliance = 0
            print("нет Альянса")
		   
		
        id_Corporation =   id_Affiliation[0]['corporation_id']                              
	
        user_Corporation = user_r.req_userCorporation(id_Corporation)['name']
	if id_Alliance != 0 :
            user_Alliance = user_r.req_userAlliance(id_Alliance)['name']
        else:
            user_Alliance = "Не состоит в альянсе"
        user_killboard = Killboard.getCharKillboard(user_id['characters'][0]['id'])
            
            
    if user_killboard == 0:
        print("Ошибка user_killboard: ", e.__class__)
        killb_info = 'None'
    else:
        killb_info = str(user_killboard['info'])
        
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
            
            user_secstatus =  str("{:.2f}".format(user_killboard['info']['secStatus']))
            
        except Exception as e:
            print("Ошибка: ", e.__class__)
            user_secstatus = "Нет в БД КБ"        
                
        try:
            
            user_destroyship = str(user_killboard['shipsDestroyed'])
              
        except Exception as e:
            print("user_destroyship Ошибка:  Уничтожил 0 кораблей" ,e.__class__)
            user_destroyship = 0

        try:
            user_solokill = str(user_killboard['soloKills'])
            )
        except Exception as e:
            print("User_solokill Ошибка: " ,e.__class__)
            user_solokill = 0            
            
            
        try:
            
            user_shiplost = str(user_killboard['shipsLost'])
            
        except Exception as e:
            print("User_ship Ошибка: " ,e.__class__)
            user_shiplost = 0
        try:
            
            user_gangratio = str(user_killboard['gangRatio'])
        except Exception as e :
            print("User_gang Ошибка: " ,e.__class__)
            user_gangratio = 0 
                
        
        
    
    print(user_id['characters'][0]['name'],user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info, sep = '  ')
    return [user_id['characters'][0]['name'],user_Corporation,user_Alliance,user_secstatus,user_destroyship,user_solokill,user_shiplost,user_gangratio,user_killb_info]
    
    
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



conn.close()
conn.close()

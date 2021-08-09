from sendsms import sendsms
def savenumberplateindatabase(number):
    
    import sqlite3
    import datetime
    
    conn = sqlite3.connect('Database.db')
    
    c = conn.cursor()
    
    d= conn.cursor()
    
    receiptno=number+str(datetime.date.today())
    
    time=datetime.datetime.now();
    
    fine=200
    
    
    c.execute("CREATE TABLE IF NOT EXISTS Records (Id integer primary key autoincrement,RECEIPT_NO text,VEHICLE_NO text,FINE_GENERATION_TIME date,FINE integer)")
    
    conn.commit()
    
    c.execute("SELECT * FROM Records WHERE RECEIPT_NO=?",(receiptno,))
    
    if(len((c.fetchall()))==0):
        c.execute("INSERT INTO Records(RECEIPT_NO,VEHICLE_NO,FINE_GENERATION_TIME,FINE) VALUES(?,?,?,?)", (receiptno,number,time,fine))
        
        #c.execute("SELECT * FROM Records")
    
        #print(c.fetchall())
    
        #c.execute("DROP table Records")
        
        d.execute("CREATE TABLE IF NOT EXISTS Numbers (VEHICLE_NO text,MOBILE_NUMBER int)")
        
        d.execute("SELECT MOBILE_NUMBER FROM Numbers WHERE VEHICLE_NO=?",(number,))
        
        mobileno=d.fetchall()
        
        #print(mobileno)
        
        if(len(mobileno)==0):    
        
            c.execute("INSERT INTO Numbers(VEHICLE_NO,MOBILE_NUMBER) VALUES(?,?)",(number,9999999999))
            
        else:

            #d.execute("SELECT MOBILE_NUMBER FROM Numbers WHERE VEHICLE_NO=?",(number,))
            
            #mobileno=d.fetchall()
        
            #print(d.fetchall())
        
            #print(type(mobileno))
            
            mobile=mobileno[0]
            
            #print(mobile)
            #print("ji")
        
            mobile=str(mobile)
            #print(mobile)
        
            mob=''
            for i in range(len(mobile)):
                if(mobile[i].isdigit()):
                    mob+=mobile[i]
            
            #print(mob)
                    
            mobilenumber=int(str(mob))
        
        #print(mobilenumber)
        
        sendsms(mobilenumber)
    
        conn.commit()
    
        conn.close()
        
        return True
    
    else:
        print("Fine already generated for this vehicle number today")
        return False

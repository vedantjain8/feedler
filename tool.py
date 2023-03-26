import sqlite3
import os
import mylog
from myyaml import yamldef


db = sqlite3.connect("rss.db")
curr = db.cursor()

def dropAllSQLtable():
    for siteI in yamldef()['sites']:
            site_name = str(siteI)
            curr.execute(f"drop table {site_name};")
            mylog.logDef(loggLevel='info', logMSG=f"droped table {site_name}")
    db.commit()

def dropAllSQLtableTrigger():
    try:
        for siteI in yamldef()['sites']:
            site_name = str(siteI)
            curr.execute(f"drop trigger oldPost_delete_{site_name};")
            mylog.logDef(loggLevel='info', logMSG=f"droped sqltable oldPost_delete trigger for {site_name}")
        db.commit()
    except:
        mylog.logDef(loggLevel='info', logMSG=f"failed to drop sqltable oldPost_delete trigger for {site_name}")
        pass

def dropSpecificSQLtableTrigger(site_name):
    curr.execute(f"drop trigger oldPost_delete_{site_name};")
    db.commit()
    mylog.logDef(loggLevel='info', logMSG=f"droped sqltable oldPost_delete trigger for {site_name}")

def dropSpecificSQLtable(site_name):
    curr.execute(f"drop table {site_name};")
    db.commit()
    mylog.logDef(loggLevel='info', logMSG=f"droped sqltable {site_name}")


def listAllSQLtable():
    print("\n\n")
    for siteI in yamldef()['sites']:
            site_name = str(siteI)  # site name
            print(site_name)
    db.commit()

def countTable():
    print("\n\n")
    siteCount =0
    for i in yamldef()['sites']:
        siteCount +=1
    print(siteCount)

def nuke():
    db.close()
    os.system("del rss.db")
    mylog.logDef(loggLevel='info', logMSG=f"WoH! I hope you were sure for the nuke")

if __name__=="__main__":
    while True:
        choice = int(input(
            """\n\nSQLite command aliases
            1. List all tables 
            2. Drop specific table 
            3. Drop all table 
            4. Drop specific trigger 
            5. Drop oldPost_delete trigger for all tables 
            6. Count all tables 
            7. Nuke - Delete unnecessary files
            8. Export to csv
            99. Exit \n\nEnter your choice: """))

        if choice == 1:
            listAllSQLtable()
        elif choice == 2:
            dropSpecificSQLtable(str(input("\n\nEnter table name: ")))
        elif choice == 3:
            dropAllSQLtable()
        elif choice == 4:
            dropSpecificSQLtableTrigger(str(input("\n\nEnter trigger name: ")))
        elif choice == 5:
            dropAllSQLtableTrigger()
        elif choice == 6:
            countTable()
        elif choice == 7:
            print("""
                _.-^^---....,,--       
            _--                  --_  
            <                        >)
            |                         | 
            \._                   _./  
                ```--. . , ; .--'''       
                    | |   |             
                .-=||  | |=-.   
                `-=#$%&%$#=-'   
                    | ;  :|     
            _____.,-#%&$@%#&#~,._____
            """)
            nuke()
            try:
                os.system("del /s /q logs")
                del mylog
                break
            except:
                print("del /s /q logs")
        elif choice == 8:
            print("""\n
.open rss.db
.mode csv
.header on
.mode csv
.output data.csv
select * from rss_data;
.quit
""")    
        elif choice == 99:
            break
        else:
            print("Enter a valid option!")
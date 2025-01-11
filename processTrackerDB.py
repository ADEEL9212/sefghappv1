from tempDB import tempDB

loggerDB = tempDB(["S.No","Time-Stamp","Data-Type","Process-Name","From-Process","To-Process","LogData"],nameDB="LoggerDB")

sno = 1 #inital row

def processLogger(name:str ,value:list,fromProcess:list,toProcess:list):
    global sno
    loggerDB.append({"S.No": sno, "Time-Stamp" : str(loggerDB.TimeStamp()),"Data-Type": [type(item) for item in value] ,"Process-Name" : name,"From-Process": fromProcess, "To-Process" : toProcess, "LogData": value})
    print("\n","from loggerDB: \n",str(loggerDB.getRow(sno-1,jsonMode=False)),"\n")
    sno+=1

from src.models.sensors_data import Sensors_data
from src.models.processed_data import Processed_data

sa1 = 0
sa2 = 0


#identifier|sensor_type|sensor_id|processed_data|raw_data
def add_record(vals,session):
    sid = vals[1]+vals[2]
    if vals[3] == 'Y':
        v = 1
    elif vals[3] == 'N':
        v = 0
    else:
        v = vals[3]
    data = Sensors_data(carriage_id=1, sensor_id=sid, sensor_type=vals[1], comfort_indicator=vals[0], value=v)
    session.add(data)
    session.commit()
    #print('sensors_data updated')

#CD|ULT|0|±X
def count_crowd(vals,connection,session):
    selectNum = """select value from processed_data pd  where carriage_id  = 1 and comfort_indicator = 'crowd' order by timestamp desc limit 1;"""
    exNum = connection.execute(selectNum).fetchall()[0][0]
    if exNum < 0:
        exNum = 0
   # print('exNum='+str(exNum))

    newNum = exNum + int(vals[3])
    print('newNum='+str(exNum))
    data = Processed_data(carriage_id=1, comfort_indicator='crowd', value=newNum)
    session.add(data)
    session.commit()
    print('crowd updated')



#SA|ULT|2|PP|RR
def count_seat(vals,connection,session):
    global sa1
    global sa2

    sid = vals[1]+vals[2]

    selectNum = """select value from processed_data pd  where carriage_id  = 1 and comfort_indicator = 'seat' order by timestamp desc limit 1;"""
    exNum = connection.execute(selectNum).fetchall()[0][0]
    print('exNum='+str(exNum))
    #the latest record
    selectPP = """select value from sensors_data sd where carriage_id  = 1 and sensor_id = '{}' order by timestamp desc limit 1;""".format(sid)
    exPP = connection.execute(selectPP).fetchall()[0][0]
    if exPP == 1:
        exPP = 'Y'
    elif exPP == 0:
        exPP = 'N'
    print('exPP='+str(exPP))
    # print('val='+str(vals[3]))
    print('sa1='+str(sa1))
    print('sa2='+str(sa2))

    if exPP == vals[3]: # sensor reading is stable now
        if vals[3] == 'Y':
            if vals[2] == '1':
                sa1 = 1
            elif vals[2] == '2':
                sa2 = 1
        elif vals[3] == 'N':
            if vals[2] == '1':
                sa1 = 0
            elif vals[2] == '2':
                sa2 = 0
    
    sum =20 -sa1 - sa2

    if sum != exNum:
        data = Processed_data(carriage_id=1, comfort_indicator='seat', value=sum)
        session.add(data)
        session.commit()
        print('seat updated')

#TP|TEM|0|PP|RR
def update_temp(vals,session):
    data = Processed_data(carriage_id=1, comfort_indicator='temp', value=vals[3])
    session.add(data)
    session.commit()
    print('temp updated')
    print('temp='+str(vals[3]))
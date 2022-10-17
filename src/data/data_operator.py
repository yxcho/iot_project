def count_crowd(vals,connection,session,model):
    select = """select density from crowd where train_line = 'red' and train_id = 1 and carriage_id = 1 order by timestamp desc limit 1;"""
    num = connection.execute(select).fetchall()
    num += int(vals[1])
    s1 = float(vals[2])
    s2 = float(vals[3])
    s3 = float(vals[4])
    s4 = float(vals[5])
    
    crowd_data = model.crowd.Crowd(train_line='red', train_id=1,carriage_id=1,density=num)
    crowd_raw_data1 = model.crowd_raw.Crowd_raw(train_line='red', train_id=1,carriage_id=1,sensor_id='s1',value=s1)
    crowd_raw_data2 = model.crowd_raw.Crowd_raw(train_line='red', train_id=1,carriage_id=1,sensor_id='s2',value=s2)
    crowd_raw_data3 = model.crowd_raw.Crowd_raw(train_line='red', train_id=1,carriage_id=1,sensor_id='s3',value=s3)
    crowd_raw_data4 = model.crowd_raw.Crowd_raw(train_line='red', train_id=1,carriage_id=1,sensor_id='s4',value=s4)
    session.add(crowd_data)
    session.add(crowd_raw_data1)
    session.add(crowd_raw_data2)
    session.add(crowd_raw_data3)
    session.add(crowd_raw_data4)
    session.commit()

    return num


def count_seat(vals,connection,session,model):
    select = """select count(1),status from seat where train_line = 'red' and train_id = 1 and carriage_id = 2 group by status having status ='e';"""
    num = connection.execute(select).fetchall()
    
    return num
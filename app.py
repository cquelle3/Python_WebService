from flask import Flask, json, jsonify, request, Response
import datetime

app = Flask(__name__)

oldest_transactions = {}
points_dict = {}
total_points = 0

@app.route('/at', methods=['POST'])
def add_transaction():
    global total_points

    #try to parse data from client
    data = None
    try:
        data =  json.loads(request.data)
    except:
        return Response("*Please provide a valid input.")
    print(f'Received from client: {data}')

    #store data and update total number of points
    #first check to see if there is an entry for the payer
    #otherwise update current values with given data
    name = data["payer"]
    if points_dict.get(name) == None:
        points_dict[name] = int(data["points"])
        
        #used to keep track of oldest times for each payer
        time = datetime.datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        oldest_transactions[name] = time.timestamp()
    else:
        update_points = {name: points_dict.get(name) + int(data["points"])}
        points_dict.update(update_points)

        #if the current transaction from the payer is older then the one stored, it now becomes the oldest time recorded
        curr_time = datetime.datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        if(oldest_transactions.get(name) > curr_time.timestamp()):
            updated_time = {name: curr_time.timestamp()}
            oldest_transactions.update(updated_time)

    total_points += int(data["points"])

    return Response("Points successfully added.")

@app.route('/sp', methods=['POST'])
def spend_points():
    #try to parse data given from client
    data = None
    try:
        data =  json.loads(request.data)
    except:
        return Response("*Please provide a valid input.")
    print(f'Received from client: {data}')

    if total_points < int(data["points"]):
        return Response("*You do not have enough points to spend")

    #sort payers depending on which has the oldest transaction
    oldest_order_dict = sorted(oldest_transactions.items(), key=lambda x:x[1])
    
    #objects used to store amounts subtracted from each payer 
    ret = []
    ret_data = {}

    #Start value for subtracting points for a payer
    #**************Based on the example given in the exercise, I assumed we only subtract by 100's
    count = 100

    #used to know the closest payer to the end of the dictionary that still has points
    last_index = len(oldest_order_dict) - 1

    #while we still need to take out points... 
    curr_points = int(data["points"])
    while(curr_points > 0):
        #loop through each key in the sorted dictionary
        for index, (key, value) in enumerate(oldest_order_dict):

            if curr_points == 0:
                break

            #if we are at the "last index" and there are no points left, move the index down by 1
            if(index == last_index and points_dict.get(key) == 0):
                last_index -= 1

            #if we are at the last index and we have points left...
            if index == last_index and points_dict.get(key) > 0:

                #if the number of points we need to remove is greater than 
                #is greater than the number of points the payer has,
                #subtract all the current payers points
                if curr_points > points_dict.get(key):
                    count = points_dict.get(key)
                    update_key = {key: points_dict.get(key) - count}
                    points_dict.update(update_key)
                
                #otherwise, subtract all the points left to remove from the current payer
                else:
                    count = curr_points
                    update_key = {key: points_dict.get(key) - count}
                    points_dict.update(update_key)

                #if we don't have an index for the current payer in ret_data
                #update the dictionary with a new value as -count
                if ret_data.get(key) == None:
                    update_key = {key: 0 - count}
                    ret_data.update(update_key)

                #otherwise, update dictionary entry by subtracting the count from 
                #the current stored amount  
                else:
                    update_key = {key: ret_data.get(key) - count}
                    ret_data.update(update_key)

                #update our values
                curr_points -= count
                count = 0
                last_index -= 1
            
            #if the current payer is able to subtract the current count without going negative
            #subtract current count from the payer's points
            elif points_dict.get(key) - count >= 0:
                update_key = {key: points_dict.get(key) - count}
                points_dict.update(update_key)

                #if we don't have an index for the current payer in ret_data
                #update the dictionary with a new value as -count
                if ret_data.get(key) == None:
                    update_key = {key: 0 - count}
                    ret_data.update(update_key)

                #otherwise, update dictionary entry by subtracting the count from 
                #the current stored amount  
                else:
                    update_key = {key: ret_data.get(key) - count}
                    ret_data.update(update_key)

                #make sure to update curr_points variable
                curr_points -= count
    
            #increase count (amount which we will try to subtract from next payer)
            count += 100

    #put all payers and corresponding withdrawals in a list to return to client
    for key, value in ret_data.items():
        ret.append({"payer": key, "points": value})

    return jsonify(ret)

@app.route('/pb', methods=['GET'])
def points_balance():
    #return all balances from each payer
    return jsonify(points_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# Python_WebService
A web service developed in Python and Flask to keep track of point spending

# Install
I built and tested this program using Python 3.8.

Please make sure to install Python 3.8 and Flask to run this application.

Python 3.8: [Download Link](https://www.python.org/downloads/release/python-386/)

Once you have Python installed, you can install Flask with the following command in the terminal:
```
pip install Flask
```

# Running the Service
I tested the service using two terminals, one for the Web Service, and one for the client application.

Open up the web service in one terminal using the following command:
```
python app.py
```
The service should now be running.

Similarly, open up the client application in another terminal using:
```
python client.py
```

You should now be able to send data to the web service via the client!

# Web Service Commands
### Transactions
All transactions are given to the service via the **/at** route. To give a transaction to the service, you can input the following in the client terminal:
```
/at {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"} 
```
This information should now be stored in the server.

### Spending Points
Points can be spent using the **/sp** route. To spend points, use inputs such as:
```
/sp {"points": 5000}
```
The payers that points were taken from will then be displayed.

### Balance Check
To check the point balance, use the **/pb** route. You can input the following to the client:
```
/pb
```
This will display all current points from each payer.

# Note
If there is an error connecting to the web service or incorrect input, you may get a message saying: **Could not connect to the web service**

**Based on the example given, the Spending Points route assumes points are only spent by multiples of 100**
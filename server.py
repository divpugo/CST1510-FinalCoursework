# Importing libraries
import socket
import csv
import pickle
from _thread import *
import threading

# Opening the csv file containing all the information needed on the product which the Vending Machine will sell
with open('coffee.csv', 'r+') as csv_file:
    csv_reader = csv.reader(csv_file)   # Using csv module to read the csv file
    product_list = list(csv_reader) # Converting the data inside the csv file into a list

    # Converting the quantity of products from the stock from strings to integers for later calculations
    for products in product_list:   # Looping through elements of the product list
        x = products[3]     # Extracting the stock quantity of each product (in strings)
        y = int(products[3])    # Converting the quantity of each product into integer
        products[3] = y     # Replacing the string values with the integer values

# Function in another thread to be run concurrently with main function
def threaded(conn):
    while True:     # Creating an infinite loop
        order_details = pickle.loads(conn.recv(1024))   # Receiving the order list as transaction from client side

        for product in product_list:    # Looping through elements of the product list
            for details in order_details:   # Looping through elements of the order list
                if details[0]==product[0]:  # Matching element from the product list to the order list using their
                    # product ID
                    # Creating and opening up a transaction .txt file to store each transaction
                    with open('transaction.txt', 'a') as transaction_file:
                        transaction_file.writelines(f'Item purchased: {details[1]}\nQuantity purchased: {details[3]}\n\n')
                    # Updating the stock of the products by decreasing the quantity available by the quantity already
                    # ordered
                    stock = product[3] - details[3]
                    product[3] = stock # Replacing the quantity available in the product list with the updated stock
                    # level quantity
        # Encoding the updated stock using pickle for better data transmission
        updated_stock = pickle.dumps(product_list)
        # Sending back an updated version of the stock to the client
        conn.send(updated_stock)

# Main function of the server which establishes connection with client
def main():
    host = 'localhost'  # Declaring a host
    port = 12345    # Declaring a port on which to operate
    # Create a server socket
    # AF.INET refers to the address family IPV4
    # SOCK_STREAM means connection oriented TCP protocol
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binding server socket to the host and port
    server_client.bind((host, port))
    print("socket bound to port", port)

    # put the socket into listening mode
    server_client.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        conn, addr = server_client.accept()

        print('Connected to :', addr[0], ':', addr[1])

        # Encoding product list using pickle for better data transmission
        data = pickle.dumps(product_list)
        conn.send(data) # Sending the product list to the client

        # Start a new thread and return its identifier
        start_new_thread(threaded, (conn,))


if __name__ == '__main__':
    main()
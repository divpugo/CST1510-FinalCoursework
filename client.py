# importing libraries
import socket
import pickle
from tkinter import *
from tkinter import messagebox
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a client socket
client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connects the client to the server IP address
client_Socket.connect(('localhost', 12345))

# creating global variables
order_list = []
total_pay = 0
amount_entered = 0
qty = 0
product_id = ''
product_list = []


class Machine(Tk):
    # Machine class
    # Object Oriented Programming of the tkinter GUI. This class sets up the tkinter module and produces the base for
    # Vending Machine's user interface.
    # Within this class, the following operations are executed:
    # i.Creates the skeleton needed for the GUI
    # ii.Creates and formats frames thereby allowing the switching of frames by destroying and creating frames for
    #    better user-friendliness of the program.

    # function initialise constructor
    def __init__(self):
        # super() to inherit from tkinter
        super().__init__()
        self.title('Coffee Beans')  # Setting the title of the tkinter window
        self.geometry("520x620+500+15")  # Defining the size of the window and its placement on computer screen
        self.resizable(0, 0)  # Disabling the option to resize the tkinter window
        self.configure(background="sienna4")  # Setting the background color of the window
        self.frame = None   # No frame for the default window
        self.switch_frame(WelcomePage)  # Setting first frame as the WelcomePage fram from the WelcomePage class

    # function to switch between frames
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(fill=BOTH, expand=TRUE)


class WelcomePage(Frame):

    # WelcomePage class is a frame which contains the welcoming message of the program as well as functions which are
    # needed for the proper functioning of the program in the following frames. The GUI starts with this frame and the
    # latter gives the option to proceed to the vending machine menu where orders can be made.

    # function initialise constructor
    def __init__(self, master):
        # Calling global variables needed in the function
        global order_list
        global total_pay
        global amount_entered
        global product_list
        # receiving the product list from the server
        product_list = pickle.loads(client_Socket.recv(2048))
        # ensuring that the following variables are empty
        total_pay = 0
        amount_entered = 0
        order_list = []
        # calling constructor from superclass
        Frame.__init__(self, master, bg='bisque2')
        # implementing and displaying widgets for welcoming message
        Label(self, text="Welcome to Coffee Beans Vending Machine!", font=('Courier', 15, "bold"), bg='bisque2',
              fg='sienna4').place(x=20, y=180)
        Label(self, text="ʕ•́ᴥ•̀ʔっ", font=('Courier', 40, "bold"), bg='bisque2', fg='sienna4').place(x=160, y=240)
        # button which proceeds to the next frame i.e. Menu
        Button(self, text="Order Now!", font=('Courier', 15, 'bold'), bg='sienna4', fg='bisque2',
               command=lambda: master.switch_frame(Menu)).place(x=190, y=350)


class Menu(Frame):
    # Menu class is a frame which contains the Menu of the program as well as functions which are
    # needed for the user to place an order and see the visual representation of the stock available via the matplotlib
    # bar chart. It is within this frame that the user really starts on interacting with the Vending Machine

    # function initialise constructor
    def __init__(self, master):
        # Calling global variables needed in the function
        global qty
        global product_id
        global product_list
        # Ensuring that the following global variables are empty
        qty = 0
        product_id = 0

        # Creating a dictionary from the product list for the creation of barchart using Matplotlib and Pandas Dataframe
        prod_dict = {'Product_ID': [], 'Quantity': []}
        # Going through elements of the product list and appending sub elements into the dictionary
        for products in product_list:
            prod_dict.setdefault('Product_ID', []).append(products[0])
            prod_dict.setdefault('Quantity', []).append(products[3])
        # Taking dataset from dictionary and turning it into dataframe using pandas
        df = DataFrame(prod_dict, columns=['Product_ID', 'Quantity'])
        # Creating one main frame which will contain other frames and widgets
        main_frame = Frame.__init__(self, master, bg='bisque2')
        # Creating frame on which product buttons lay
        frame1 = Frame(main_frame, width=200, height=200, bg='bisque2')
        frame1.place(x=0, y=5)
        # Creating frame on which bar chart will lay
        frame2 = Frame(main_frame, width=285, height=290, bg='bisque2')
        frame2.place(x=230, y=135)
        # Creating figure which will help embed bar chart in the GUI
        figure = plt.Figure(figsize=(7, 6.74), dpi=40)
        ax = figure.add_subplot(111)
        # Using FigureCanvasTkAgg to embed bar chart in figure and place figure in frame
        bar = FigureCanvasTkAgg(figure, frame2)
        bar.get_tk_widget().place(x=3, y=10)
        # Using Dataframe to sort dataset and plot bar chart
        df = df[['Product_ID', 'Quantity']].groupby('Product_ID').sum()
        # Setting bar chart and its xsticks and ysticks and updating its aesthetic appearance
        df.plot(kind='bar', legend=False, ax=ax, rot=70, colormap='twilight', fontsize=12)
        ax.set_title('Coffee Stock', fontsize=15)
        ax.set_ylabel('Quantity', fontsize=12)
        ax.set_xlabel('Product ID', fontsize=12)

        # Function which will be called by clicking on the Add to Cart button
        # Function ensures that the products chosen by user are stored in an order list
        def add_to_cart():
            # Calling global variables needed in the function
            global product_list
            global order_list
            global total_pay
            global qty
            global product_id
            # Looping through the product list
            for details in product_list:
                if product_id == details[0]:  # Checking if product ID entered by uer is in the list
                    price = float(details[2])  # Extracting price of product from list
                    total = price * qty  # Calculating total price of order placed
                    order = [product_id, details[1], details[2], qty, total]  # Creating list for the order
                    total_pay += order[4]  # Calculating the total amount of all order placed and storing them
                    # in the total_pay global variable
                    order_list.append(order)  # appending orders into the global order_list to create a 2D list
            # Switching frame to the cart frame whereby user will see the order placed
            master.switch_frame(Cart)

        # Function associated with product buttons which will display product details such as product ID, price and
        # quantity available in stock
        def prod_details(prod_id, prod_price, prod_qty):
            # Decorative background frame
            background = Frame(self, width=285, height=120, bg='sienna4').place(x=230, y=10)
            # Frame on which product ID, price and quantity available in stock will lay on
            details = Frame(background, width=265, height=100, bg="AntiqueWhite3").place(x=240, y=20)
            Label(details, text="Product ID:", font=('Courier', 11, 'bold'), fg="sienna4", bg='AntiqueWhite3').place(
                x=260, y=25)
            Label(details, text=prod_id, font=('Courier', 11, 'bold'), fg="sienna4", bg='AntiqueWhite3').place(x=420,
                                                                                                               y=25)
            Label(details, text="Price:", font=('Courier', 11, 'bold'), fg="sienna4", bg='AntiqueWhite3').place(x=260,
                                                                                                                y=55)
            Label(details, text=prod_price, font=('Courier', 11, 'bold'), fg="sienna4", bg='AntiqueWhite3').place(x=420,
                                                                                                                  y=55)
            Label(details, text="Qty Available:", font=('Courier', 11, 'bold'), fg="sienna4",
                  bg='AntiqueWhite3').place(x=260, y=85)
            Label(details, text=prod_qty, font=('Courier', 11, 'bold'), fg="sienna4", bg='AntiqueWhite3').place(x=420,
                                                                                                                y=85)

        # Function for the button which allows user to increase quantity of product they are ordering
        def increase():
            # Calling global variables needed in the function
            global qty
            global product_id
            global product_list
            # Incrementing quantity ordered by one with ever click and displaying the quantity
            qty += 1
            display.set(qty)
            # Extracting products ID entered by user
            product_id = id_input.get()
            # Looping through products in the product list
            for details in product_list:
                # Verifying if product ID exist in the product list and checking if quantity ordered is not more than
                # stock available
                if product_id == details[0] and qty > details[3]:
                    # Displaying a warning message informing user that they can't order more than the quantity available
                    messagebox.showwarning("showwarning", "Cannot order more than stock level!")
                    # Disabling the add to cart button to prevent user from ordering more than quantity available
                    add["state"] = 'disabled'
                    fin_pay["state"] = 'disabled'
                # Verifying that ID entered by user exist in product list and ensuring that quantity ordered is more
                # than zero before enabling user to have access to add to cart button which allows them to proceed
                elif product_id == details[0] and (details[3] > qty > 0):
                    add["state"] = 'normal'

        # Function for the button which allows user to increase quantity of product they are ordering
        def decrease():
            # Calling global variables needed in the function
            global qty
            global product_id
            global product_list
            # Decreasing quantity ordered by one with ever click and displaying the quantity
            qty -= 1
            # Extracting products ID entered by user
            product_id = id_input.get()
            # Looping through products in the product list
            for details in product_list:
                # Ensuring that quantity ordered is not a negative number and that the product ID exist in the product
                # list before enabling user to process and be able to click on the add to cart button
                if product_id == details[0] and qty <= 0 or not product_id == details[0] and qty <= 0:
                    add["state"] = 'disabled'
                # When product ID exist in product list and quantity ordered is greater than zero but less than or
                # equal to the stock available, the uer is able to proces and click on the add to cart button
                elif product_id == details[0] and (details[3] >= qty > 0):
                    add["state"] = 'normal'
            # Displaying the quantity onto the screen for user to see how many they are ordering
            display.set(qty)

        _ = 1  # Using a throwaway variable to store the x row where button will be placed
        for row in product_list:  # Looping through elements of the product list and extracting values for the
            # elements in each row to be on a button and take onto the command function of the latter
            Button(frame1, text=row[1], width=30, height=2, font=('Helvetica', 8, 'bold'), bd=2, bg="dark slate gray",
                   fg='white',
                   command=lambda prod_id=row[0], prod_price=row[2], prod_qty=row[3]: prod_details(prod_id, prod_price,
                                                                                                   prod_qty)).grid(
                row=_, column=0, padx=6, pady=4)
            _ += 10  # Incrementing the positional value of the x grid for each button

        # Decorative frame
        order_background = Frame(main_frame, width=285, height=180, bg='sienna4').place(x=230, y=430)
        # Creating a frame on which widgets to place an order will lay
        order_frame = Frame(order_background, width=265, height=160, bg="AntiqueWhite3").place(x=240, y=440)
        # Placing the buttons on the frame
        # Button prompting user to add their order to cart
        add = Button(order_frame, text='Add to cart', font=('Helvetica', 11, 'bold'), fg='bisque2', bg='sienna4',
                     command=add_to_cart)
        add.place(x=409, y=520)
        add["state"] = 'disabled'  # Button disabled unless quantity ordered is in the range of the stock available but
        # not zero
        # Button giving the user the option to cancel their orders and prompts them to the frame with apology message
        Button(order_frame, text="Cancel", font=('Helvetica', 11, 'bold'), fg='bisque2', bg='sienna4',
               command=lambda: master.switch_frame(Cancel)).place(x=245, y=560)
        # Button allowing user to go to their receipt where they can finish their order and pay for their transaction
        # Button switches frame to the Finish one
        fin_pay = Button(order_frame, text="Finish and Pay", font=('Helvetica', 11, 'bold'), bg='dark slate gray',
                         fg='bisque2',
                         command=lambda: master.switch_frame(Finish))
        fin_pay.place(x=383, y=560)
        # Labels describing what user has to do
        Label(order_frame, text="Quantity:", font=('Courier', 11, 'bold'), bg="AntiqueWhite3", fg='sienna4').place(
            x=245, y=480)
        Label(order_frame, text="Enter Product ID:", font=('Courier', 11, 'bold'), bg='AntiqueWhite3',
              fg='sienna4').place(x=245, y=450)

        display = StringVar()  # Creating input_text variable which will ensure what is displayed onto screen
        display.set("0")  # Setting default value to be displayed as zero
        # Creating screen through Entry box to display quantity of product being ordered
        screen = Entry(order_frame, textvariable=display, bd=2, width=5, justify=CENTER)
        screen.place(x=335, y=480)
        # Button allowing user to increase the quantity
        Button(order_frame, text='+', font=('Helvetica', 8, 'bold'), width=2, bg="AntiqueWhite3", fg='sienna4',
               command=lambda: increase()).place(x=328, y=505)
        # Button allowing user to decrease the quantity
        minus = Button(order_frame, text='-', font=('Helvetica', 8, 'bold'), width=2, bg="AntiqueWhite3", fg='sienna4',
                       command=lambda: decrease())
        minus.place(x=352, y=505)
        # Creating Entry box for user to enter product ID they wish and order
        id_input = Entry(order_frame, width=5, bd=2)
        id_input.place(x=405, y=450)

        # Calling global variable needed in the function
        global order_list
        # Ensuring that user does not have access to the payment window unless they have made an order priorly
        if not order_list:
            fin_pay["state"] = "disabled"


class Cart(Frame):
    # function initialise constructor
    def __init__(self, master):
        # Creating one main frame which will contain other frames and widgets
        main_frame = Frame.__init__(self, master, bg='bisque2')
        # Decorative frames
        Frame(main_frame, bg='sienna4', width=420, height=470).place(x=50, y=85)
        Frame(main_frame, bg='dark slate gray', width=400, height=450).place(x=60, y=95)
        # Frame on which the latest order placed will be displayed and widgets allowing user to proceed and pay, add
        # another product to their order or cancel the transaction altogether will way
        display = Frame(main_frame, bg='papaya whip', width=380, height=430).place(x=70, y=105)
        Label(self, text="============ ⊂(◉‿◉)つ ============", bg='bisque2', fg='sienna4',
              font=('Helvetica', 20, "italic")).place(x=0, y=25)
        Label(display, text='You ordered the following:', font=("Courier", 14, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(x=75, y=115)
        Label(display, text='Product ID:', font=("Courier", 10, 'bold'), bg='papaya whip', fg='dark slate gray').place(
            x=75, y=200)
        Label(display, text=order_list[-1][0], font=("Courier", 9, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(x=200, y=200)  # Accessing product ID of the last item added to the order list
        Label(display, text='Product name:', font=("Courier", 10, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(x=75, y=250)
        Label(display, text=order_list[-1][1], font=("Courier", 9, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(x=200, y=250)  # Accessing product name of the last item added to the order
        # list
        Label(display, text='Unit price:', font=("Courier", 10, 'bold'), bg='papaya whip', fg='dark slate gray').place(
            x=75, y=300)
        Label(display, text=order_list[-1][2], font=("Courier", 9, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(x=200, y=300)  # Accessing unit price of the last item added to the order list
        Label(display, text='Quantity:', font=("Courier", 10, 'bold'), bg='papaya whip', fg='dark slate gray').place(
            x=75, y=350)
        Label(display, text=order_list[-1][3], font=("Courier", 9, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(x=200, y=350)  # Accessing quantity of the last item added to the order list
        Label(display, text='Total price:', font=("Courier", 10, 'bold'), bg='papaya whip', fg='dark slate gray').place(
            x=75, y=400)
        Label(display, text=order_list[-1][4], font=("Courier", 9, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(
            x=200, y=400)  # Accessing total price of the last item added to the order list
        # Button allowing user to go back to the menu frame where they can add another order to their transaction
        Button(self, text="Add Another", width=12, command=lambda: master.switch_frame(Menu),
               font=('Helvetica', 12, 'bold'),
               bg='sienna4', fg='bisque2').place(x=15, y=570)
        # Button giving the user the option to cancel their orders and prompts them to the frame with apology message
        Button(self, text='Cancel', font=('Helvetica', 12, 'bold'), bg='sienna4', width=12, fg='bisque2',
               command=lambda: master.switch_frame(Cancel)).place(x=195, y=570)
        # Button allowing user to proceed to the next frame where they can review their orders and finish and pay
        Button(self, text='Finish and Pay', command=lambda: master.switch_frame(Finish),
               font=('Helvetica', 12, 'bold'), bg='dark slate gray', fg='bisque2').place(x=375, y=570)


class Finish(Frame):
    # function initialise constructor
    def __init__(self, master):
        # Calling global variables needed in the function
        global order_list
        global total_pay
        # Creating one main frame which will contain other frames and widgets
        main_frame = Frame.__init__(self, master, bg='bisque2')
        # Creating a receipt frame which will display the details of the orders made by the user
        receipt = Frame(main_frame, width=180, height=555, relief=RAISED, bg='old lace').place(x=330, y=55)
        Label(self, text="================ Your Receipt ================", bg='bisque2', fg='sienna4',
              font=('Helvetica', 15, "italic")).place(x=0, y=25)
        Label(self, text="Description", bg='bisque2', fg='sienna4',
              font=('Helvetica', 13, "italic")).place(x=10, y=58)
        Label(receipt, text="Qty", bg='old lace', fg='sienna4',
              font=('Helvetica', 13, "italic")).place(x=338, y=58)
        Label(receipt, text="Cost", bg='old lace', fg='sienna4',
              font=('Helvetica', 13, "italic")).place(x=390, y=58)
        Label(receipt, text="Price", bg='old lace', fg='sienna4',
              font=('Helvetica', 13, "italic")).place(x=455, y=58)
        Label(receipt, text="Total", bg='old lace', fg='sienna4',
              font=('Helvetica', 13, 'bold')).place(x=330, y=525)
        Label(receipt, text="----------", bg='old lace', fg='sienna4',
              font=('Helvetica', 13,)).place(x=440, y=510)
        Label(receipt, text="----------", bg='old lace', fg='sienna4',
              font=('Helvetica', 13,)).place(x=440, y=535)
        Label(receipt, text=total_pay, bg='old lace', fg='sienna4',
              font=('Helvetica', 10)).place(x=455, y=525)
        # Button allowing user to go back to the previous frame that was displayed which is the Finish frame
        Button(self, text="Go Back", command=lambda: master.switch_frame(Cart), width=12,
               font=('Helvetica', 12, 'bold'), bg='sienna4', fg='bisque2').place(x=15, y=570)
        # Button giving the user the option to cancel their orders and prompts them to the frame with apology message
        Button(self, text='Cancel', font=('Helvetica', 12, 'bold'), width=12, bg='sienna4', fg='bisque2',
               command=lambda: master.switch_frame(Cancel)).place(x=190, y=570)
        # Button prompting user to go pay for their order and switching frame the Pyament one
        Button(receipt, text='Payment Method', command=lambda: master.switch_frame(Payment),
               font=('Helvetica', 12, 'bold'), bg='dark slate gray', fg='bisque2').place(x=350, y=570)

        _ = 100  # Using a throwaway variable to store the y position where label will be placed
        for description in order_list:  # Looping through elements of order list to extract some of them
            # Extracting the name of the product ordered and displaying it in the receipt frame
            Label(self, text=description[1], font=("Courier", 10, 'bold'), bg="bisque2").place(x=10, y=_)
            # Extracting the quantity of the product ordered and displaying it in the receipt frame
            Label(receipt, text=description[3], font=("Courier", 10, 'bold'), bg="old lace").place(x=350, y=_)
            # Extracting the price of the product ordered and displaying it in the receipt frame
            Label(receipt, text=description[2], font=("Courier", 10, 'bold'), bg="old lace").place(x=385, y=_)
            # Extracting the total price of the products ordered and displaying it in the receipt frame
            Label(receipt, text=description[4], font=("Courier", 10, 'bold'), bg="old lace").place(x=455, y=_)

            _ += round(620 / 18)


class Payment(Frame):
    # function initialise constructor
    def __init__(self, master):
        # Calling global variable needed in the function
        global amount_entered
        amount_entered = 0
        # Creating one main frame which will contain other frames and widgets
        main_frame = Frame.__init__(self, master, bg='sienna4')
        # Decorative frames
        Frame(main_frame, bg='LightSalmon4', width=420, height=350).place(x=50, y=115)
        Frame(main_frame, bg='dark slate gray', width=400, height=330).place(x=60, y=125)
        # Frames on which widgets prompting user to choose a payment method lay
        display = Frame(main_frame, bg='papaya whip', width=380, height=310).place(x=70, y=135)
        Label(display, text="( ͡~ ͜ʖ ͡°)", font=('Helvetica', 30, "bold"), bg='papaya whip',
              fg='dark slate gray').place(x=190, y=180)
        Label(display, text='Choose your payment method:', font=("Courier", 13, 'bold'), bg='papaya whip',
              fg='dark slate gray').place(x=125, y=280)
        # Button for cash payment which when clicked switches frame to the Cash frame
        Button(display, text="Cash", font=('Helvetica', 18, 'bold'), fg='sienna4', bg='bisque2',
               command=lambda: master.switch_frame(Cash)).place(x=120, y=345)
        # Button for card payment which when clicked switched frame to the Card frame
        Button(display, text='Card', font=('Helvetica', 18, 'bold'), fg='sienna4', bg='bisque2',
               command=lambda: master.switch_frame(Card)).place(x=330, y=345)
        # Button giving the user the option to cancel their orders and prompts them to the frame with apology message
        Button(self, text='Cancel', font=('Helvetica', 12, 'bold'), width=12, bg='bisque2', fg='sienna4',
               command=lambda: master.switch_frame(Cancel)).place(x=375, y=570)
        # Button allowing user to go back to the previous frame that was displayed which is the Finish frame
        Button(self, text="Go Back", command=lambda: master.switch_frame(Finish), width=12,
               font=('Helvetica', 12, 'bold'), bg='bisque2', fg='sienna4').place(x=15, y=570)


class Cash(Frame):
    # function initialise constructor
    def __init__(self, master):
        # Calling global variables needed in the function
        global amount_entered
        global total_pay
        # Creating one main frame which will contain other frames and widgets
        main_frame = Frame.__init__(self, master, bg='bisque2')
        # Creating frame on which buttons that represent cash entered will lay
        num_pad = Frame(main_frame, bg='papaya whip', width=380, height=320).place(x=70, y=135)
        # Creating a Frame which will act as display screen whereby user can see their balance, the amount of money
        # they entered and the change they should receive
        display = Frame(num_pad, bg='AntiqueWhite3', width=355, height=150).place(x=83, y=145)
        Label(display, text='Your balance is:', font=("Courier", 13, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
            x=95, y=160)
        Label(display, text=total_pay, font=("Courier", 13, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
            x=340, y=160)
        Label(display, text='Cash entered (Rs.):', font=("Courier", 13, 'bold'), bg='AntiqueWhite3',
              fg='sienna4').place(
            x=95, y=200)

        Label(display, text='Your change is (Rs.):', font=("Courier", 13, 'bold'), bg='AntiqueWhite3',
              fg='sienna4').place(
            x=95, y=240)
        # Button allowing user to go back to the previous frame that was displayed which is the payment frame
        go_back = Button(self, text="Go Back", command=lambda: master.switch_frame(Payment), width=12,
                         font=('Helvetica', 12, 'bold'), bg='sienna4', fg='bisque2')
        go_back.place(x=15, y=570)
        # Button giving the user the option to cancel their orders and prompts them to the frame with apology message
        cancel = Button(self, text='Cancel', font=('Helvetica', 12, 'bold'), width=12, bg='sienna4', fg='bisque2',
                        command=lambda: master.switch_frame(Cancel))
        cancel.place(x=195, y=570)
        # Button prompting user to ThankYou frame when transaction is over
        done = Button(self, text='Done', command=lambda: master.switch_frame(ThankYou),
                      font=('Helvetica', 12, 'bold'), bg='dark slate gray', fg='bisque2', width=12)
        done.place(x=375, y=570)
        # Button allowing to switch to ThankYou frame is disabled until cash entered is greater or equal to the balance
        # that is amount to be paid and the user has received their change if any
        done["state"] = 'disabled'

        # Function taking in the cash entered by user who clicked on the buttons representing money
        # Money is a parameter in the function and it takes the value associated with the button pressed
        def button(money):
            # Calling global variables needed in the function
            global amount_entered
            global total_pay
            # Each button pressed carries a value which is added to the amount_entered variable
            amount_entered += money
            # User is able to press pay button only when the amount entered is greater or equal to the amount to be paid
            if amount_entered >= total_pay:
                pay["state"] = 'normal'
            # Amount entered displayed changes dynamically with the amount the user clicks to insert
            Label(display, text=amount_entered, font=("Courier", 13, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
                x=340, y=200)

        # Function calculating the change user should receive
        def change():
            # Calling global variables needed in the function
            global total_pay
            global amount_entered
            change_received = amount_entered - total_pay
            # Prompting user to complete transaction once the change they receive is greater or equal to zero
            if change_received >= 0:
                done["state"] = 'normal'
            # Displaying change received onto screen
            Label(display, text=change_received, font=("Courier", 13, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
                x=340, y=240)
            # Disabling buttons preventing user to go back to menu and other frames since transaction is over
            undo["state"] = "disabled"
            cancel["state"] = "disabled"
            go_back["state"] = "disabled"

        # Function allowing user to undo and "get back" the money they entered
        def erase():
            # Calling global variable needed in the function
            global amount_entered
            amount_entered = 0
            Label(display, text=amount_entered, font=("Courier", 13, 'bold'), width=5, bg='AntiqueWhite3',
                  fg='sienna4').place(
                x=370, y=200)

        # Creating a list of the money to be displayed on buttons for cash payment transactiong
        coins = [0.5, 1, 5, 10, 20, 25]
        notes = [50, 100, 200, 500, 1000, 2000]

        _ = 85  # Using a throwaway variable to store the x position where buttons will be placed
        for i in coins:  # Looping through the coins list to create buttons
            Button(num_pad, text=i, width=5, height=2, font=('Helvetica', 10, 'bold'), bd=2, bg="dark slate gray",
                   fg='white', command=lambda money=i: button(money)).place(x=_, y=305)
            _ += 60

        _ = 85  # Using a throwaway variable to store the x position where buttons will be placed
        for j in notes:  # Looping through the coins list to create buttons
            Button(num_pad, text=j, width=5, height=2, font=('Helvetica', 10, 'bold'), bd=2, bg="dark slate gray",
                   fg='white', command=lambda money=j: button(money)).place(x=_, y=355)
            _ += 60
        # Button for user to pay and receive their change
        pay = Button(num_pad, text='Pay', width=20, height=2, font=('Helvetica', 10, 'bold'), bd=2,
                     bg="dark slate gray",
                     fg='white', command=lambda: change())
        pay.place(x=266, y=405)
        # Pay button is disabled until amount entered is greater or equal to the amount to be paid that is their balance
        pay["state"] = 'disabled'
        # Undo button which allows user to "take out" the money they entered
        undo = Button(num_pad, text='Undo', width=20, height=2, font=('Helvetica', 10, 'bold'), bd=2,
                      bg="brown3", fg='white', command=lambda: erase())
        undo.place(x=85, y=405)


class Card(Frame):
    # function initialise constructor
    def __init__(self, master):
        # Function mimicking the validity of credit or debit card
        def validate():
            # Getting the length of the values entered in the entry fields
            number = len(num.get())
            mnth = len(month.get())
            yr = len(year.get())
            names = len(name.get())
            cvv_num = len(cvv.get())
            # Verifying that values entered meet conditions and enabling done button while disabling buttons which
            # otherwise would allow user to go back to vending machine even after completing payment
            if number == 16 and mnth == 2 and yr == 2 and names > 0 and cvv_num == 3:
                done["state"] = 'normal'
                cancel["state"] = "disabled"
                go_back["state"] = "disabled"

        # Creating one main frame which will contain other frames and widgets
        main_frame = Frame.__init__(self, master, bg='bisque2')
        background = Frame(main_frame, bg='dark slate gray', width=400, height=340).place(x=60, y=125)
        display = Frame(background, bg='AntiqueWhite3', width=380, height=320).place(x=70, y=135)
        # Labels and widgets displayed on the display frame
        Label(display, text='Your balance is:', font=("Courier", 15, 'bold'), bg='AntiqueWhite3',
              fg='sienna4').place(x=95, y=160)  # Label displaying user's balance and amount to be paid
        Label(display, text=total_pay, font=("Courier", 14, 'bold'), bg='AntiqueWhite3',
              fg='sienna4').place(x=300, y=160)  # Label displaying user's balance and amount to be paid
        # Labels and widgets which allow user to enter their card details
        Label(display, text='Enter card details:', font=("Courier", 13, 'bold'), bg='AntiqueWhite3',
              fg='sienna4').place(x=95, y=200)
        Label(display, text='Card number:', font=("Courier", 10, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
            x=95, y=240)
        num = Entry(display, width=40, bd=2)  # Enter card number
        num.place(x=95, y=260)
        Label(display, text='Expiry date:', font=("Courier", 10, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
            x=95, y=290)
        month = Entry(display, width=5, bd=2)  # Enter month from expiry date
        month.place(x=95, y=310)
        Label(display, text='/', font=("Courier", 10, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
            x=130, y=310)
        year = Entry(display, width=5, bd=2)  # Enter year from expiry date
        year.place(x=145, y=310)
        Label(display, text='Name on card:', font=("Courier", 10, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
            x=95, y=340)
        name = Entry(display, width=40, bd=2)  # Enter name associated with card
        name.place(x=95, y=360)
        Label(display, text='CVV:', font=("Courier", 10, 'bold'), bg='AntiqueWhite3', fg='sienna4').place(
            x=95, y=390)
        cvv = Entry(display, width=5, bd=2)  # Enter cvv number for card verification
        cvv.place(x=95, y=410)
        # Button validating payment
        Button(display, text='Validate', width=12, font=('Helvetica', 12, 'bold'), bg='dark slate gray',
               fg='AntiqueWhite3', command=lambda: validate()).place(x=300, y=410)
        # Button allowing user to go back to the previous frame that was displayed which is the payment frame
        go_back = Button(self, text="Go Back", command=lambda: master.switch_frame(Payment), width=12,
                         font=('Helvetica', 12, 'bold'), bg='sienna4', fg='bisque2')
        go_back.place(x=15, y=570)
        # Button giving the user the option to cancel their orders and prompts them to the frame with apology message
        cancel = Button(self, text='Cancel', font=('Helvetica', 12, 'bold'), width=12, bg='sienna4', fg='bisque2',
                        command=lambda: master.switch_frame(Cancel))
        cancel.place(x=195, y=570)
        # Button prompting user to ThankYou frame when transaction is over
        done = Button(self, text='Done', command=lambda: master.switch_frame(ThankYou),
                      font=('Helvetica', 12, 'bold'), bg='dark slate gray', fg='bisque2', width=12)
        done.place(x=375, y=570)
        done["state"] = 'disabled'


class ThankYou(Frame):
    # function initialise constructor
    def __init__(self, master):
        # Calling global variable needed in the function
        global order_list
        # Sending order list to server so that stock is updated and transaction is saved
        client_message = pickle.dumps(order_list)
        client_Socket.send(client_message)

        # Creating one main frame which will contain other frames and widgets
        # Creating Labels displaying apology message in the main frame
        # and prompting user to click button to return to the home page
        Frame.__init__(self, master, bg='dark slate gray')
        Label(self, text="Thank you for your purchase!", font=('Helvetica', 13, "bold"), bg='dark slate gray',
              fg='bisque2').place(x=140, y=180)
        Label(self, text='( ＾◡＾)っ ♡', font=('Helvetica', 25, "bold"), bg='dark slate gray', fg='bisque2').place(x=177,
                                                                                                                y=290)
        Label(self, text='We hope to see you again. Have a good day!', font=('Helvetica', 13, "bold"),
              bg='dark slate gray', fg='bisque2').place(x=90, y=220)
        # Button prompting user back to the WelcomePage which is the homepage and where vending machine "reboots"
        Button(self, text="Go back to main page.", font=('Helvetica', 13, 'bold'), bg='sienna4', fg='bisque2',
               command=lambda: master.switch_frame(WelcomePage)).place(x=170, y=390)


class Cancel(Frame):
    # function initialise constructor
    def __init__(self, master):
        # Calling global variable needed in the function
        global order_list
        order_list = []  # emptying the order list
        # sending back an empty order list to server to maintain smooth running connection
        client_message = pickle.dumps(order_list)
        client_Socket.send(client_message)

        # Creating one main frame which will contain widgets for when the cancel button is clicked
        Frame.__init__(self, master, bg='sienna4')
        # Creating Labels displaying apology message and prompting user to click button to return to the home page
        Label(self, text="Sorry, we could not provide you with your choice today.", font=('Helvetica', 13, "bold"),
              bg='sienna4', fg='bisque2').place(x=35, y=180)
        Label(self, text='( ＾◡＾)っ ♡', font=('Helvetica', 25, "bold"), bg='sienna4', fg='bisque2').place(x=175, y=280)
        Label(self, text='We hope to see you again. Have a good day!', font=('Helvetica', 13, "bold"), bg='sienna4',
              fg='bisque2').place(x=90, y=220)
        # Button prompting user back to the WelcomePage which is the homepage and where vending machine "reboots"
        Button(self, text="Go back to main page.", font=('Helvetica', 13, 'bold'), bg='bisque2', fg='sienna4',
               command=lambda: master.switch_frame(WelcomePage)).place(x=150, y=390)


# Calling function to run vending machine program
if __name__ == '__main__':
    machine = Machine()
    machine.mainloop()

# CST 1510- Final Coursework
The aim of this project is to design and implement a Vending Machine for hot and cold coffee beverages. Through Python, a Client/Server-side software system is built to interact with the user on the client-side while the data storage is processed on the server-side. The server program allows multiple clients to interact with the current stock of the product through an intuitive graphical user interface, and background operations ensure that the stock remains up to date based on the orders done by the client. This vending machine is entitled "Coffee Beans" and offer the following operations when launched:

1. Start up the main page and greet the user with a welcoming message.
2. Product selection and display of product details such as product ID, price, quantity available and graphical representation (bar chart) of stock level for all products available. 
3. User is prompted to enter product ID and quantity of the product they wish to order.
4. Once order is added to cart, a summary of the transaction is displayed. User can either proceed to "Finish and Pay", "Add Another" product or "Cancel" the transaction.
5. Clicking on "Add another" redirects the user to the previous window whereby product selection and product details are displayed and they can place another order.
6. Clicking on "Finish and Pay" redirects the user to a virtual receipt which displays every order placed and their total balance. The user can then proceed to Payment Methods or Go back to the previous window, and they are once again presented with the possibility to cancel their transaction.
7. Clicking on "Cancel" opens a window which displays an apology message and prompts the user back to the main page.
8. Payment Methods include either cash or card. If payment is made by cash, change will be displayed on the screen.
9. Once payment is complete, a window displays a Thank You message before prompting the next user back to the main page.

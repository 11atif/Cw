# -*- coding: utf-8 -*-
"""Car Rental.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cpGSpGrebWksmOuGt6kh_pHPoAp_qAUb
"""

class RentalShop: # Main class for the rent shop
    def __init__(self):
        self.available_cars_stock = {'hatchback': 4, 'sedan': 3, 'SUV': 3}
        # Rates of cars
        self.rates = {
            'hatchback': {'less_than_week': 30, 'more_than_week': 25},
            'sedan': {'less_than_week': 50, 'more_than_week': 40},
            'SUV': {'less_than_week': 100, 'more_than_week': 90}
        }
        # VIP rates are here
        self.vip_rates = {'hatchback': 20, 'sedan': 35, 'SUV': 80}

    def available_cars(self):
        return self.available_cars_stock

    def rent_cost(self, days, car_type, vip=False):
      # Calculation. Multiplying days by rates above
        if vip:
            return days * self.vip_rates[car_type]
        else:
            rate_key = 'less_than_week' if days < 7 else 'more_than_week'
        return days * self.rates[car_type][rate_key]


    def rent_car(self, customer, car_type, days, vip=False):
      # Check if the car is in stock before renting
        if self.available_cars_stock[car_type] > 0:
      # Decrease by one from inventory
            self.available_cars_stock[car_type] -= 1
            self.show_inventory()
            return "", True
        else:
            print(f"Sorry, The {car_type} is not available to rent. Try another, {show_inventory}")
            return "", False

    def return_car(self, customer, car_type, days, vip=False):
        if self.available_cars_stock[car_type] >= 0:  # Ensure the car was rented from this shop
            self.available_cars_stock[car_type] += 1  # Add it back to inventory once returned
            self.generate_bill(customer, car_type, days, vip)
            self.show_inventory()
            return "", True
        else:
            print(f"Error: The {car_type} car was not rented from this shop.")
            return "", False

    def generate_bill(self, customer, car_type, days, vip=False):
        if vip:
            rate = self.vip_rates[car_type]
        else:
            rate_key = 'less_than_week' if days < 7 else 'more_than_week'
            rate = self.rates[car_type][rate_key]

        total_cost = days * rate

        # Print the bill in mutiple lines.
        print (f"""
  Name: {customer.name},
  Car Type: {car_type},
  Rate: £{rate} per day,
  Total Bill Charged: £{total_cost}.
    """)
        print(f"Thank you, {customer.name}, for using our service. Enjoy your day!")

    def show_inventory(self):
      # Inventory after every transaction
      print("\nInventory:") #\n is to add a line in output.
      for car_type, stock in self.available_cars_stock.items():
            print(f"{car_type}: {stock} available")

class Customer:
    def __init__(self, name, is_vip=False):
        self.name = name
        self.returning_customer = False
        self.is_vip = is_vip


    def inquire(self, rental_shop):
        print(f"Welcome, {'VIP ' if self.is_vip else ''}{self.name}, to our rental service!")
        # Main functions of the programme
        while True:
        # Tripe quotes are used to break the line.
          Options = """
What would you like to do?
1. Rent a car
2. Return a car
3. Check prices
4. Check availability
5. Other inquiries
          """

          print (Options)

          print("Type bye to exist.") # To break the loop.

          choice = input("Enter your choice (1, 2, 3, 4, 5): ")

          if choice == '1':
                self.rent_car(rental_shop)
                break  # If car is rented end the script.
          elif choice == '2':
                self.return_car(rental_shop)
                break  # Same as rent.
          elif choice == '3':
                self.check_prices(rental_shop)
          elif choice == '4':
                self.check_availability(rental_shop)
          elif choice == '5':
                self.other_inquiries()
          elif choice.lower() in ['bye', 'thank you']:
                print(f"Thank you for using our service, {'VIP ' if self.is_vip else ''}{self.name}! Have a great day.")
                break
          else:
                print("Invalid choice. Please enter a valid option.") #Error handling for any other than 5 options.

    def get_max_rent_days(self):
      # Limit the max days for renting a car
      while True:
        days = input("Enter the number of days (up to 100 days): ")
        if days.isdigit() and 1 <= int(days) <= 100: # Has to be a positive integar
            return int(days)
        else:
            print("Invalid input. Please enter a valid number between 1 and 100.") # Error handling

    def rent_car(self, rental_shop, vip=False):
        while True:
            car_type = self.get_car_choice()
            days = self.get_max_rent_days()
            total_cost = rental_shop.rent_cost(days, car_type, vip)

            if rental_shop.available_cars_stock[car_type] > 0: # More than 1 needed to rent
                print(f"\nYou, {'VIP ' if vip else ''}{self.name}, have rented a {car_type} for {days} days.")
                print(f"You will be charged £{total_cost} in total.")
                print("Enjoy your day!")
                rental_shop.rent_car(self, car_type, days, vip=vip)
                break
            else:
                print(f"Sorry, The {car_type} is not available to rent. Try another.")


    def return_car(self, rental_shop, vip=False):
        print(f"Welcome back, {'VIP ' if self.is_vip else ''}{self.name}, you can now return a previously rented car.")

        while True:
            car_type = self.get_car_choice()
            days = self.get_max_rent_days ()
            total_cost = rental_shop.rent_cost(days, car_type, vip)

            if rental_shop.available_cars_stock[car_type] >= 0: # 0 Is ok as it is a rented car
                print(f"\nYou, {'VIP ' if vip else ''}{self.name}, have rented a {car_type} for {days} days.")
                print(f"Here is your Bill:")
                rental_shop.return_car(self, car_type, days, vip=vip)
                break
            else:
                print(f"Error: The {car_type} car was not rented from this shop. Try again.")

    def check_prices(self, rental_shop,):
        while True:
            print("Prices:")
            for car_type, rate_info in rental_shop.rates.items():
                normal_rate = (f"£{rate_info['less_than_week']} per day (less than a week), "
                               f"£{rate_info['more_than_week']} per day (more than a week)")
                vip_rate = f"VIP Rate: £{rental_shop.vip_rates[car_type]} per day"

                print(f"{car_type}: {normal_rate}, {vip_rate}")

            print("would you like to see the total cost of renting?")
            # Just to check the prices for total rental.
            choice = self.get_yes_no_input()
            if choice == 'yes':
                car_type = self.get_car_choice()
                days = self.get_max_rent_days ()
                total_cost = rental_shop.rent_cost(days, car_type, vip = self.is_vip)
                print(f"The total cost for {days} days of renting a {car_type} is £{total_cost}.")
                break
            elif choice == 'no':
                print("Returning to options.")
                break  # Exit the loop and go back to main options
            else:
                print("Invalid choice. Please enter a valid option (yes/no).")

    def check_availability(self, rental_shop):
        print("Available Stock:")

        for car_type, stock in rental_shop.available_cars().items():
            print(f"{car_type}: {stock} available")

    def other_inquiries(self): # Other inquiries can be anything so, email.
        print("For other inquiries, please contact us at support@rentalshop.com.")

    def get_yes_no_input(self): # For inputs that require a yes or no. Error Handling.
        while True:
            response = input().lower()
            if response in ['yes','no']:
                return response
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")

    def get_car_choice(self): # To not repeat the code. Car choice is in a funtion.
        while True:
            print("\nCar Types:")
            print("1. Hatchback")
            print("2. Sedan")
            print("3. SUV")
            car_choice = input("Enter the car type (1, 2, 3): ")

            if car_choice in {'1', '2', '3'}:
                return {'1': 'hatchback', '2': 'sedan', '3': 'SUV'}[car_choice]
            else:
                print("Invalid choice. Please enter a valid option (1, 2, 3).")


class VIPCustomer(Customer):
    def rent_car(self, rental_shop):
        super().rent_car(rental_shop, vip=True)  # Reuse the implementation from the base class

    def return_car(self, rental_shop):
        super().return_car(rental_shop, vip=True)

# script
rental_shop = RentalShop()
rental_shop.show_inventory()

# Please delete the 'while True: to run the programme independetly.
# To test the break point for rent/return/bye input, just delete the while True: line of code.

while True: # Only needed to run the programme continiously.
  customer_name = input("\nPlease enter your name: ")

  print("\nAre you a VIP member? (Yes/No): ")
  vip_option = Customer(customer_name).get_yes_no_input()

# Use VIPCustomer if the customer is a VIP member
  if vip_option == 'yes':
    customer_rent = VIPCustomer(customer_name, is_vip=True)
  else:
    customer_rent = Customer(customer_name, is_vip=False)

  customer_rent.inquire(rental_shop)
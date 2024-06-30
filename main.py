import traceback
import curses
from typing import List

class PurchaseItem(object):
    def __init__(self, option):
        self.price = option.p
        self.name = str(option)

def get_total_order_amount(order: List[PurchaseItem]):
    """
    The total cost of all the items ordered
    """
    total_amount = sum(item.price for item in order)
    return total_amount

def get_service_charge(order: List[PurchaseItem]):
    """
    For every Rs. 100, the service charge amount should increase by 1% of order amount, up to a max of 20%
    Eg:
        Order Amount = 80, Service Charge = 0
        Order Amount = 150, Service Charge = 1.5
        Order Amount = 800, Service Charge = 64
        Order Amount = 1500, Service Charge = 225
        Order Amount = 3000, Service Charge = 600
    """
    total_amount = get_total_order_amount(order)
    if total_amount == 0:
        return 0
    service_charge_rate = min((total_amount // 100) * 0.01, 0.20)
    service_charge = total_amount * service_charge_rate
    return service_charge

class Option(object):
    def __init__(self, n=None, pu=None, p=None, d=None):
        self.p = p
        self.n = n
        self.pu = pu
        if d:
            self.n = d.get("name")
            self.p = d.get("price")
        if self.p is None:
            self.p = 0
        if self.n is None:
            raise AttributeError
        self.pu = self.pu if self.pu else "Rs."

    def __str__(self):
        return f"{str(self.n)} {str(self.pu) + ' ' + str(self.p) if self.p else ''}"

    def __len__(self):
        return len(self.__str__())

MCDONALDS_FOOD_OPTIONS = [
    Option(d={"name": "Veg Burger", "price": 115.00}),
    Option(d={"name": "Veg Wrap", "price": 130.00}),
    Option(d={"name": "Veg Happy Meal", "price": 215.00}),
    Option(d={"name": "Chicken Burger", "price": 175.00}),
    Option(d={"name": "Chicken Wrap", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]

MCDONALDS_BEVERAGES_OPTIONS = [
    Option(d={"name": "Sprite (M)", "price": 115.00}),
    Option(d={"name": "Sprite (L)", "price": 130.00}),
    Option(d={"name": "Mango Smoothie", "price": 215.00}),
    Option(d={"name": "Chocolate Smoothie", "price": 175.00}),
    Option(d={"name": "Chocolate Smoothie w/ Icecream", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]

def get_option_from_result(result, options):
    for option in options:
        if str(option) == result:
            return option
    raise Exception("Unexpected option selected")

def print_order(stdscr, order):
    stdscr.clear()

    try:
        total_amount = get_total_order_amount(order)
    except:
        traceback.print_exc()
        total_amount = "ERROR"

    service_charge = "ERROR"
    if total_amount != "ERROR":
        try:
            service_charge = get_service_charge(order)
        except:
            traceback.print_exc()
            service_charge = "ERROR"

    stdscr.addstr("Final Order\n", curses.color_pair(1))
    for i, item in enumerate(order):
        stdscr.addstr(f"{i+1}. {item.name}\n", curses.color_pair(2))

    stdscr.addstr(f"Order Amount: {str(total_amount)}\n", curses.color_pair(1))
    stdscr.addstr(f"Service Charge: {str(service_charge)}\n", curses.color_pair(1))
    final_amount = (
        total_amount + service_charge
        if isinstance(total_amount, (int, float)) and isinstance(service_charge, (int, float))
        else 'ERROR'
    )
    stdscr.addstr(f"Final Amount: {str(final_amount)}\n", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

def select_option(stdscr, prompt, options):
    curses.curs_set(0)
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(prompt + "\n")
        for i, option in enumerate(options):
            if i == selected:
                stdscr.addstr(f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {option}\n")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return options[selected]

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_GREEN)

    stdscr.addstr("Welcome to McDonalds on your shell :)\n", curses.color_pair(1))
    stdscr.addstr("Here you can place your order\n", curses.color_pair(1))
    stdscr.addstr("And then we will show you your bill\n", curses.color_pair(1))
    stdscr.getch()
    
    order = []
    while True:
        result = select_option(stdscr, "Add an item", [str(opt) for opt in MCDONALDS_FOOD_OPTIONS])
        option = get_option_from_result(result, MCDONALDS_FOOD_OPTIONS)
        if result == str(MCDONALDS_FOOD_OPTIONS[-1]):
            break
        order.append(PurchaseItem(option))
        stdscr.addstr(f"{result} is added to your order\n", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()

    while True:
        result = select_option(stdscr, "Add a beverage", [str(opt) for opt in MCDONALDS_BEVERAGES_OPTIONS])
        option = get_option_from_result(result, MCDONALDS_BEVERAGES_OPTIONS)
        if result == str(MCDONALDS_BEVERAGES_OPTIONS[-1]):
            break
        order.append(PurchaseItem(option))
        stdscr.addstr(f"{result} is added to your order\n", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()

    print_order(stdscr, order)

if __name__ == "__main__":
    curses.wrapper(main)


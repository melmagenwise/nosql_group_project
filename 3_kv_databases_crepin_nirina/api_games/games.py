# Definition of the Game class
class Game:
    # Constructor method to initialize a Game instance with provided attributes
    def __init__(self, sid, title, year, genre, platform, price, quantity):
        # Assigning provided values to instance variables
        self.sid = sid
        self.title = title
        self.year = year
        self.genre = genre
        self.platform = platform
        self.price = price
        self.quantity = quantity

    # Class method to create a Game instance from user input
    @classmethod
    def from_user_input(cls):
        # Taking user input for each attribute
        sid = input("Enter GameId: ")
        title = input("Enter Game Title: ")
        year = int(input("Enter Released Year: "))
        genre = input("Enter Genre Name: ")
        platform = input("Enter Platform Name: ")
        price = int(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))

        # Creating and returning a new Game instance with user-provided values
        return cls(sid, title, year, genre, platform, price, quantity)
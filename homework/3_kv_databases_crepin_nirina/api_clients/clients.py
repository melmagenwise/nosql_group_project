# Definition of the Client class
class Client:
    # Constructor method to initialize a Client instance with provided attributes
    def __init__(self, sid, name, birthday, email, phone, city, genre):
        # Assigning provided values to instance variables
        self.sid = sid
        self.name = name
        self.birthday = birthday
        self.email = email
        self.phone = phone
        self.city = city
        self.genre = genre

    # Class method to create a Client instance from user input
    @classmethod
    def from_user_input(cls):
        # Taking user input for each attribute
        sid = input("Enter ClientId: ")
        name = input("Enter Client Name: ")
        birthday = input("Enter Client Birthday (DD/MM/YYYY): ")
        email = input("Enter Email Name: ")
        phone = input("Enter Phone Name: ")
        city = input("Enter City: ")
        genre = input("Enter Genre: ")

        # Creating and returning a new Client instance with user-provided values
        return cls(sid, name, birthday, email, phone, city, genre)
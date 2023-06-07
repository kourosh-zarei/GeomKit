class MyClass:
    @staticmethod
    def my_method():
        print("This is a static method")

    def my_method(self):
        print("This is a non-static method")


# Creating an instance of the class
obj = MyClass()

# Calling the static method
MyClass.my_method()  # Output: This is a static method

# Calling the non-static method
obj.my_method()  # Output: This is a non-static method

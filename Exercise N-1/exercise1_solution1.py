from collections import Counter, OrderedDict


class MyClass(Counter, OrderedDict):
    pass


try:
    # =================== INPUT SECTION =================== #
    my_integer = int(input("Enter Number of Words: "))
    if 1 <= my_integer <= 10**5:
        my_inputs = []
        for item in range(my_integer):
            my_inputs.append(input(f"Enter {item+1} Word: ").strip().lower())

        # ============== CHECK WORD'S SUM LENGTH SECTION ================ #
        whole_length = 0
        for each_item in my_inputs:
            whole_length += len(each_item)

        if whole_length <= (10**6):
            my_result = MyClass(my_inputs)

            print(len(my_result))
            for i in my_result:
                print(my_result[i], end=" ")
        else:
            print("The Sum of the lengths of the Entered words is more than 10**6 - Please enter shorter words!")
    else:
        print("The Entered Integer Number must be between 1 and 10**5!")

except ValueError:
    print("Please Enter Only Numbers Into First Input Form!")

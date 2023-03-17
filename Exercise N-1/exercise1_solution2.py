# =============================== INPUT SECTION ================================ #
try:
    my_integer = int(input("Enter Integer Number: "))

    if 1 <= my_integer <= 10 ** 5:
        my_inputs = []
        for i in range(my_integer):
            my_inputs.append(input(f"Enter {i+1} String: ").strip().lower())

        # ====================== CHECK WORD'S SUM LENGTH SECTION ======================= #
        whole_length = 0
        for each_item in my_inputs:
            whole_length += len(each_item)

        if whole_length <= (10 ** 6):
            unique_values = []
            for item in my_inputs:
                if item not in unique_values:
                    unique_values.append(item)

            unique_quantity = len(unique_values)

            count_occurrences = []
            for item in unique_values:
                count_occurrences.append(my_inputs.count(item))

            print(unique_quantity)
            for my_count in count_occurrences:
                print(my_count, end=" ")

        else:
            print("The Sum of the lengths of the Entered words is more than 10**6 - Please enter shorter words!")
    else:
        print("The Entered Integer Number must be between 1 and 10**5!")

except ValueError:
    print("Please Enter Only Number - Integer Into First Input Form!")

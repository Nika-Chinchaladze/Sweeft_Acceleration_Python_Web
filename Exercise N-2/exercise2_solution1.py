from string import ascii_lowercase

MY_LETTERS = list(ascii_lowercase)


def check_for_ascii(my_word: str):
    """checks if all character of entered word is in the MY_LETTERS list"""
    my_check = 0
    for letter in my_word.lower():
        if letter not in MY_LETTERS:
            my_check += 1

    if my_check > 0:
        return False
    else:
        return True


# ================================== MAIN LOGIC SECTION ====================================== #
def bigger_is_greater(my_word):
    my_list = [ord(letter) for letter in my_word]

    # find first element from the end which does not belong to decreasing sequence
    i = len(my_list) - 1
    while i > 0 and my_list[i-1] >= my_list[i]:
        i = i - 1

    # check point 1: if pivot element was not found
    if i <= 0:
        return False

    # check point 2: if pivot element was found then make swapping operation
    j = len(my_list) - 1
    while my_list[j] <= my_list[i - 1]:
        j = j - 1

    my_list[i-1], my_list[j] = my_list[j], my_list[i-1]

    my_list[i:] = my_list[len(my_list)-1:i-1:-1]
    my_answer = [chr(item) for item in my_list]
    my_answer = "".join(my_answer)
    print(my_answer)
    return True


# ===================================== MULTIPLE TESTS SECTION ========================================= #
try:
    my_test_number = int(input("Enter Number of Test Cases: "))
    if 1 <= my_test_number <= 10**5:
        for m in range(my_test_number):
            my_string = input("Please Enter Word: ")
            if 1 <= len(my_string) <= 100:
                if check_for_ascii(my_word=my_string):
                    my_value = bigger_is_greater(my_string)
                    if my_value:
                        continue
                    else:
                        print("no answer")
                else:
                    print("Entered Word is inappropriate, Word should contain letters only from a to z!")
            else:
                print("Entered Word is inappropriate, Please enter words with length from 1 to 100!")
    else:
        print("Entered Integer Number must be between 1 and 100000!")
except ValueError:
    print("Please, Enter Only Integers In the Number of Test Cases Input!")

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
def swap_positions(my_list, position_1, position_2):
    my_list[position_1], my_list[position_2] = my_list[position_2], my_list[position_1]
    return my_list


def bigger_is_greater(my_word: str):
    my_list = [ord(letter) for letter in my_word]
    n = len(my_list)
    i = 0
    j = 0

    # find first element from the end which does not belong to decreasing sequence
    for i in range(n - 2, -1, -1):
        if my_list[i] < my_list[i + 1]:
            break

    # check point 1: if pivot element was not found
    if i < 0:
        return "no answer"
    # check point 2: if pivot element was found then make swapping operation
    else:
        for j in range(n - 1, i, -1):
            if my_list[j] > my_list[i]:
                break

        swap_positions(my_list, i, j)
        start, end = i + 1, len(my_list)
        my_list[start:end] = my_list[start:end][::-1]

    word_again = [chr(number) for number in my_list]
    word_again = "".join(word_again)

    if word_again == my_word:
        return "no answer"
    else:
        return word_again


# ================================== MULTIPLE TESTS SECTION ====================================== #
try:
    my_test_number = int(input("Enter Number of Test Cases: "))
    if 1 <= my_test_number <= 10**5:
        for m in range(my_test_number):
            my_string = input("Please Enter Word: ")
            if 1 <= len(my_string) <= 100:
                if check_for_ascii(my_word=my_string):
                    my_value = bigger_is_greater(my_string)
                    print(my_value)
                else:
                    print("Entered Word is inappropriate, Word should contain letters only from a to z!")
            else:
                print("Entered Word is inappropriate, Please enter words with length from 1 to 100!")
    else:
        print("Entered Integer Number must be between 1 and 100000!")
except ValueError:
    print("Please, Enter Only Integers In the Number of Test Cases Input!")

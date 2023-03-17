from itertools import permutations
from string import ascii_lowercase

MY_LETTERS = list(ascii_lowercase)


# ================================== MAIN LOGIC SECTION ====================================== #
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


def generated_swapped_combinations(target_string: str):
    """generates all combinations of swapped target_string in list format"""
    my_list = list(permutations(target_string))
    my_result = ["".join(item) for item in my_list]
    return my_result


def bigger_is_greater(my_string: str):
    """sorts returned list in Lexicographically / Alphabetically order and finds greater the closest string"""
    my_list = generated_swapped_combinations(target_string=my_string)
    my_list.sort()
    # find next lexicographically greater string:
    my_index = my_list.index(my_string) + 1
    try:
        if my_list[my_index] == my_string:
            return "no answer"
        else:
            return my_list[my_index]
    except IndexError:
        return "no answer"


# ===================================== MULTIPLE TESTS SECTION ========================================= #
try:
    my_test_number = int(input("Enter Number of Test Cases: "))
    if 1 <= my_test_number <= 10**5:
        my_inputs = []
        for i in range(my_test_number):
            entered_word = input(f"Please Enter {i+1} Word: ").lower()
            if 1 <= len(entered_word) <= 100:
                if check_for_ascii(my_word=entered_word):
                    my_inputs.append(entered_word)
                else:
                    print("Entered Word is inappropriate, Word should contain letters only from a to z!")
                    my_inputs = []
                    break
            else:
                print("Entered Word is inappropriate, Please enter words with length from 1 to 100!")
                my_inputs = []
                break

        for word in my_inputs:
            print(bigger_is_greater(my_string=word))
    else:
        print("Entered Integer Number must be between 1 and 100000!")
except ValueError:
    print("Please, Enter Only Integers In the Number of Test Cases Input!")

# Tests for project

# loads all the functions defined in Siu_Liao_Final_Project.py into the
# current environment.
from Siu_Liao_Final_Project import *

## Comparison functions that don't compare floats using '=='

def eq(e, a):
    # == is stricter than this function, so if e == a is true,
    # then eq(e, a) would be true as well.  
    if e == a:
        return True

    # Compare ints as float instead
    if type(e) == int:
        e = float(e)
    if type(a) == int:
        a = float(a)

    # Arguments must be of the same type.
    if type(e) != type(a):
        return False

    # Delegate to a more specific comparator. Only the types
    # for this assignment are implemented.
    if type(e) == dict:
        return eq_dict(e, a)
    elif type(e) == float:
        return eq_float(e, a)
    elif type(e) == str:
        return eq_str(e, a)

def eq_dict(e, a):
    # In this assignment, keys will never be float, so this 
    # comparison is okay.
    if sorted(e.keys()) != sorted(a.keys()):
        return False

    for key in e:
      if not eq(e[key], a[key]):
          return False

    return True

def eq_float(e, a):
    """Returns true of e is within 0.00001 of a.
    
    Take-away point: You should never compare floats using ==
    
    Explanation:
    Computers store floating point numbers as only an approximation
    of the actual value.  This is not just a limitation of Python, it is
    true in most languages and is due to the way floating point numbers
    are stored as bits in computers. See ICPUP section 3.4 for more info.
    Try typing this example into the Python interpreter (adding 0.1 ten times):
    >>> b = .1 + .1 + .1 + .1 + .1 + .1 + .1 + .1 + .1 + .1
    >>> b
    0.9999999999999999
    >>> b == 1.0
    False
    Since 0.1 cannot be represented exactly in floating point, adding 
    together 0.1 ten times does NOT equal 1.0 exactly!! It is not just 
    this example, it happens for many values and combining (or taking
    the difference, or dividing, etc.) these inexact values will 
    accumulate and amplify minor differences as you manipulate a 
    floating point value multiple times.
 
    So instead of testing for equality, whenever you want to check to see
    if two floating point values are equal, you should use a technique 
    like we do here: you should check if value e is *within some epsilon* 
    of value a. We can pick epsilon to be however small/close we want.
    In this case we arbitrarily picked 0.00001 as "close enough to be 
    considered equal".  
    """
    epsilon = 0.00001
    return abs(e - a) < epsilon

def eq_str(e, a):
    return e == a

## Tests
def test_wordToCount():
    text = "hello hello hello one one happy cute cute cute cute cow"
    dict_test_1 = wordToCount(text)
    dict_correct_1 = {
        "hello" : 3,
        "one" : 2,
        "happy" : 1,
        "cute" : 4,
        "cow" : 1
    }

    assert eq_dict(dict_test_1, dict_correct_1)

def test_removeXMLTags():
    test_input_1 = "<p>Chianson is the most <strong>handsome<strong> man  "
    test_input_1 += "<cost>$infinite</cost> in the world</p>!"

    test_expect_1 = "Chianson is the most handsome man  $infinite in the world!"

    assert eq_str(removeXMLTags(test_input_1), test_expect_1)

def test_top10Words():
    dict_test_1 = {
        "hoho" : 1,
        "hehe" : 1,
        "haha" : 1,
        "random" : 1,
        "e" : 3,
        "!" : 2,
        "u" : 8,
        "v" : 4,
        "o" : 5,
        "l" : 7,
        "i" : 9,
        "ans" : 31,
        "c" : 100,
        "h" : 70,
        "the" : 1000,
        "of" : 1002,
        "a" : 1003
    }
    list_correct_1 = ["c", "h", "ans", "i", "u", "l", "o", "v", "e", "!"]
    
    assert eq_str(list_correct_1, top10Words(dict_test_1))


def test_filter10User():
    users_df = pd.read_csv("Users.csv")

    # Test sort by high
    sorted_high_df = users_df.sort_values("_Reputation", ascending=False)
    high_dict = filter10User(sorted_high_df)
    #print(high_dict)

    # Test sort by low
    sorted_low_df = users_df.sort_values("_Reputation")
    low_dict = filter10User(sorted_low_df)
    #print(low_dict)


# If this file, tests.py, is run as a Python script (such as by typing
# "python tests.py" at the command shell), then run the following tests:
if __name__ == "__main__":
    print("**************************************")
    print("*** Testing Siu_Liao_Final_Project ***")
    print("**************************************")
    test_wordToCount()
    test_removeXMLTags()
    test_top10Words()
    test_filter10User()

    print("Tests passed.")

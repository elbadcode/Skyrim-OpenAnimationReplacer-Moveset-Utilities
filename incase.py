#case insensitive
def i_equals(str1,str2):
    try:
        return str1.lower() == str2.lower()
    except ValueError:
        return str(str1).lower() is str(str2).lower()

def i_in(str1,str2):

    try:
        flag = False
        for _str in str1:
            if i_in(_str,str2):
                flag = True
                break
        return flag

    except IndexError:
        print("str1 not iterable")

    try:
        flag = False
        for _str2 in str2:
            if i_in(_str2,str1):
                flag = True
                break
        return flag

    except IndexError:
        print("str2 not iterable")

    try:
        return str1.lower() in str2.lower()
    except AttributeError:
        return str(str1).lower() in str(str2).lower()

def i_endswith(str1,str2):
    if
    return str1.lower().endswith(str2.lower())


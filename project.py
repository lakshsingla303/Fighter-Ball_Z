import os


# The only reason we had to define functions in such a way was because we used classes extensively and could not call the
# functions form those classes without breaking our code.

def main():
    os.system("Start_Screen.py")
    os.system("player.py")


def function1(x):
    return x


def function2(x):
    return x*x


def function3(x):
    return x*x*x


if __name__ == '__main__':
    main()

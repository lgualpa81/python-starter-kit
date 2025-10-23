"""
The nonlocal keyword is used to work with variables inside nested functions, where the variable should not belong to the inner function.

Use the keyword nonlocal to declare that the variable is not local.
"""


def outer():
    enclosing_variable = "Enclosing variable"

    def inner():
        nonlocal enclosing_variable
        enclosing_variable = "Enclosing Modificado"

    inner()
    print(enclosing_variable)


outer()

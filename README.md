# pycalc - Python Calculator

Calculator terminal application written in Python 3.

## Usage

### Getting started

Download the `pycalc/` directory.
In the terminal, `cd` to the directory containing `pycalc/`, and run

    $ python3 pycalc

You should see something like this:

![Screenshot](images/startup.png)

To exit the program, type `quit` at the prompt.

### Evaluating Arithmetic Expressions

At the prompt, type arithmetic expressions and hit `ENTER` to have them evaluated:

![Screenshot](images/evaluating-expressions.png)

`pycalc` supports the following operations and functions:
* `+`, `-`, `*`, `/`, `^`: (*infix*) addition, subtraction, multiplication, division, and exponentiation.
* `!`: (*postfix*) factorial (only defined for non-negative integers).
* `exp`, `log`, `cos`, `sin`, `tan`: standard transcendental function.
* `(..)`, `|..|`: parentheses and absolute value delimiters.


### Declaring Variables

In the screenshot above, the `ans =` line means that the result of the computation is stored as the variable `ans`.
You can define your own variables and use them in computations:

![Screenshot](images/declaring-variables.png)


### The `vars` Command

To see what variables are currently stored, type `vars` at the prompt:

![Screenshot](images/vars-command.png)


### The `del` Command

To delete a variable, use the `del` keyword at the prompt, followed by the names
of the variables you want to delete:

![Screenshot](images/del-command.png)


### The `help` Command

For more help, type `help` at the prompt:

![Screenshot](images/help-command.png)


### Runtime Errors

If a computation fails, `pycalc` will try to tell you why:

![Screenshot](images/runtime-errors.png)

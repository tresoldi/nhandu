#' # Hello World with Nhandu
#'
#' This is the simplest possible example of a Nhandu document. It demonstrates basic Python code execution and output capture.
#'
#' ## Basic Output
#'
#' Let's start with the classic hello world:

print("Hello, World!")

#' ## Simple Calculations
#'
#' Nhandu can execute Python expressions and capture their results:

2 + 2

result = 42 * 1.5
print(f"The answer is {result}")

#' ## Variables Persist
#'
#' Variables defined in one code block are available in subsequent blocks:

name = "Alice"
age = 30

print(f"{name} is {age} years old")

#' ## That's It!
#'
#' This example shows the basic functionality of Nhandu:
#' - Executing Python code blocks
#' - Capturing print output
#' - Displaying expression results
#' - Maintaining variable state across blocks
#'
#' Try running: `nhandu examples/01_hello_world.py`
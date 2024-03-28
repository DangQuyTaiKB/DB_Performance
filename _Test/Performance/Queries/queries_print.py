# print("{  userPage {\n    id\n    name\n    surname\n    email\n    valid\n  }\n}")

# {  userPage {
#     id       
#     name     
#     surname  
#     email    
#     valid    
#   }
# }

# function: convert query to string
def convert_to_python_string(query):
    return repr(query)


query = """
{  userPage {
    id
    name
    surname
    email
    valid
  }
}
"""

print(convert_to_python_string(query[1:]))




# The repr() function returns a string containing a printable representation of an object. For strings, this means it includes the quotes and any special characters are escaped with backslashes. So, for a multi-line string, repr() will include the newline characters as \n in the output.
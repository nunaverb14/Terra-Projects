print("Hello World")
while True:
    try:
        input = input("Type a number 1-4: ")
        if type(input) == str:
            break
    except Exception as e:
        print(f"Error: {e}")

print(f"Hi: {input}")
Prepkdeme
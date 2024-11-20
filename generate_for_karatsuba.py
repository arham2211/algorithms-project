
import random

def run():
    i=1

    while(i<=10):
        vals = [(random.randint(10, 100000000000000000000), random.randint(10, 100000000000000000)) for _ in range(500)]
        file_name = f"./karatsuba_inputs/karatsuba_input_{i}.txt"


        # Open the file in write mode (this will create the file if it doesn't exist)
        with open(file_name, "w") as file:
                for x,y in vals:
                    file.write(f"{x} {y} \n")

        i+=1            

    print(f"File '{file_name}' has been created and written to.")

#run()
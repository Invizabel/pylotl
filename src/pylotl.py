# references:
# x86/64: http://ref.x86asm.net/geek.html#x90 
import argparse
import binascii
import re

def pylotl():
    parser = argparse.ArgumentParser()
    parser.add_argument("-filename", required = True)
    args = parser.parse_args()
    filename = args.filename
    
    results = []
    x86_array = {"00": "ADD\tEb Gb", "01": "ADD\tEvqp Gvqp", "02": "ADD\tGb Eb", "03": "ADD\tGvqp Evqp", "04": "ADD\tAL Ib", "05": "ADD\trAX Ivds", "06": "PUSH\tES", "07": "POP\tES", "08": "OR\tEb Gb", "09": "OR\tEvqp Gvqp", "0A": "OR\tGb Eb", "0B": "OR\tGvqp Evqp", "0C": "OR\tAL Ib", "0D": "OR\trAX Ivds", "0E": "PUSH\tCS", "0F": "POP\tCS", "10": "ADC\tEb Gb"}
    x64_array = {"00": "ADD\tEb Gb", "01": "ADD\tEvqp Gvqp", "02": "ADD\tGb Eb", "03": "ADD\tGvqp Evqp", "04": "ADD\tAL Ib", "05": "ADD\trAX Ivds", "06": None, "07": None, "08": "OR\tEb Gb", "09": "OR\tEvqp Gvqp", "0A": "OR\tGb Eb", "0B": "OR\tGvqp Evqp", "0C": "OR\tAL Ib", "0D": "OR\trAX Ivds", "0E": None, "0F": None, "10": "ADC\tEb Gb"}

    with open(filename, "rb") as file:
        raw_data = file.read()

    data = binascii.hexlify(raw_data).decode().upper()

    hits = re.findall(r"\w{2}", data)
    for hit in hits:
        try:
            if x86_array[hit]:
                results.append(f"{hit}\t{x86_array[hit]}")
            
        except:
            pass

    with open("assmebly.txt", "w") as file:
        for result in results:
            print(result)
            file.write(f"{result}\n")

    print("DONE!")

if __name__ == "__main__":
    pylotl()

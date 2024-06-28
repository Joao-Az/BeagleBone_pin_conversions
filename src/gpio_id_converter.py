"""
PocketBeagle is an open-source and low-cost embedded system nad t uses a AM3358 
Sitara™ processor from Texas Instruments,  seems there's little information on 
the naming pattern 
In the context of embedded systems, GPIO (General Purpose Input/Output) 
are used to address physical locations of versatile pins unlike other's that 
hold specific protocols (e.g. I2C, UART, SPI). These can be configured as 
inputs and/or outputs and can interact with the latter.

In our particular case, when defining a device tree overlay for prucam it is 
useful when integrate the sensor with the system. PocketBeagle is an open-source and 
low-cost embedded system that uses a AM3358 Sitara™ processor from Texas Instruments. 

Seems there's little information on the relation between the pin number (GPIO {n})
as defined in the BeagleBoard and the .dts gpio reference <&gpio{i} {j} 0>. 
In the last case, we are dealing with a phandle which has that syntax.

Furthermore, in the TI's "am3358" datasheet there's yet another way of addressing to the same 
GPIO with "gpio{i}_{j}". Between these naming conventions, by brute-force, one can find
that {i}∈{0,1,2,3} with {j}^{21}_{0} for i=3 and with {j}^{31}_{0} for the 
other cases.  
Thus it can become handy to have a function that promptly translates between these 
for operationability matters.

For the internal GPIO number corresponding to pin GPIOi_j we calculate as: (i*32)+j 
"""

import re
import pandas as pd

def convert_gpio_to_internal(input_str):
    # Use regular expression to extract numbers from the input string
    match = re.match(r"gpio(\d+)_(\d+)", input_str)
    if match:
        # Extract numbers j and k
        j = int(match.group(1))
        k = int(match.group(2))
        # Perform calculation
        n = j * 32 + k
        # Return formatted result
        return f"{n}"
    else:
        return "Invalid input format"


def convert_gpio_to_dts(gpio_num):
    gpio_num = int(gpio_num)
    # Calculate j and k
    j = gpio_num // 32
    k = gpio_num % 32
    # Return formatted result
    return f"gpio{j}_{k}"

def convert_gpio_to_dts2(gpio_num):
    gpio_num = int(gpio_num)
    # Calculate j and k
    j = gpio_num // 32
    k = gpio_num % 32
    # Return formatted result
    return f"<gpio{j} {k} 0>"

def search_table_to_header(gpiox):
    data = pd.read_excel("Pins_Table.xlsx")
    gpiox_bus, gpiox_pos = gpiox.split("_")
    gpiox_bus = "&" + gpiox_bus
    gpiox_pos = int(gpiox_pos)
    print(gpiox_bus)
    header = data[(data['GPIO_bus'] == gpiox_bus) & (data['GPIO_position'] == gpiox_pos)]['Header_pin']
    
    if not header.empty:
        return header.iloc[0]
    else:
        return None
    
def search_table_from_header(header):
    data = pd.read_excel("Pins_Table.xlsx")
    df = pd.DataFrame(data)
    result = df[df['Header_pin'] == header][['GPIO_bus', 'GPIO_position']]
    if not result.empty:
        bus = result.iloc[0]['GPIO_bus'].replace('&', '')
        pos = result.iloc[0]['GPIO_position']
        return f"{bus}_{pos}"
    else:
        return None

define_translation = "null"

def readme():
    print("    ")
    print("__README__")
    print("    PocketBeagle is an open-source and low-cost embedded system nad t uses a AM3358 Sitara™ processor from Texas Instruments.")
    print("    In the context of embedded systems, GPIO (General Purpose Input/Output) are used to address physical locations of versatile pins unlike other's that hold specific protocols (e.g. I2C, UART, SPI).")
    print("    These can be configured as inputs and/or outputs and can interact with the latter. \n")

    print("    In our particular case, when defining a device tree overlay for prucam it is useful when integrate the sensor with the system.")
    print("    Seems there's little information on the relation between the pin number (GPIO [n]) as defined in the BeagleBoard and the .dts gpio reference <&gpio[i] [j] 0>.")
    print("    In the last case, we are dealing with a phandle which has that syntax. \n")
    
    print("    Furthermore, in the TI's 'am3358' datasheet there's yet another way of addressing to the same GPIO with 'gpio[i]_[j]'.")
    print("    Between these naming conventions, by brute-force, one can findthat [i]∈[0,1,2,3] with [j]^[21]_{0] for i=3 and with [j]^[31]_[0] for the other cases.")
    print("    Thus it can become handy to have a function that promptly translates between these for operationability matters. \n")

    print("    For the internal GPIO number corresponding to pin GPIOi_j we calculate as: (i*32)+j. \n")

print("########################################")
print("### GPIO Naming Convention Converter ###")
print("########################################")

def conversion():
    if what.lower() == "conversion":
        print("Which naming convention do you want to translate from? ")
        define_translation = input("Enter 'p headers' ('headers' works too), 'sitara' or 'internal pin number' ('ipn' works too): ").lower()
        print("\n")
        translate(define_translation)

def translate(define_translation):
    if define_translation == "sitara":
        value = input("Enter the Sitara gpio value (in the format gpio{x}_{y}{z}): ")
        print("    The internal pin number: GPIO ", convert_gpio_to_internal(value))
        print("    The position in the physical board: ", search_table_to_header(value))
        
    elif define_translation == "internal pin number" or define_translation == "ipn":
        value = input("Enter the pin number value (e.g. 56): ")
        print("    As shown in Sitara Datasheet: ",convert_gpio_to_dts(value))
        print("    As shown in device tree syntax: ", convert_gpio_to_dts2(value))
        print("    As shown in the physical board: ", search_table_to_header(convert_gpio_to_dts(value)))
    
    elif define_translation == "p headers" or define_translation == "headers":
        value = input("Enter P header value (e.g. P1_08): ")
        print("    As shown in Sitara Datashee: ", search_table_from_header(value))
        print("    The internal pin number: GPIO ", convert_gpio_to_internal(search_table_from_header(value)))
        print("    As shown in the device tree syntax: ", convert_gpio_to_dts2(convert_gpio_to_internal(search_table_from_header(value))))
        
while True:
    print("___  ___  ___  ___  ___  ___  ___  ___")
    what = input("\n Enter 'ReadMe' to read the context of this program or 'Conversion' to use the conversion function. \n To terminate this program enter 'Quit': ")
    if what.lower() == "readme":
        readme()
    elif what.lower() == "conversion":
        conversion()
    elif what.lower() == "quit":
        print("Terminating...")
        break
    else:
        print("Invalid input. Please enter 'ReadMe', 'Conversion', or 'Quit'.")
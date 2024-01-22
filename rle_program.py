from console_gfx import ConsoleGfx

# --------------------------METHODS-------------------------
def to_hex_string(data):    # convert list into string
    num = ''

    for i in data:
        if i == 15:
            num += 'f'
        elif i == 14:
            num += 'e'
        elif i == 13:
            num += 'd'
        elif i == 12:
            num += 'c'
        elif i == 11:
            num += 'b'
        elif i == 10:
            num += 'a'
        else:
            num += str(i)

    return num

def count_runs(flat_data):     # tracks the number of runs for each number
    current_number = flat_data[0]
    current_run_length = 1
    run_count = 1

    for i in flat_data[1:]:

        if i == current_number:
            current_run_length += 1
        else:
            current_number = i
            current_run_length = 1
            run_count += 1

        if current_run_length > 15:     # start a new run if num is over 15
            current_run_length = 1
            run_count += 1

    return run_count

def encode_rle(flat_data):  # generate RLE representation of input data
    encoded_rle = []
    current_num = flat_data[0]
    current_run_size = 1

    for i in range(1, len(flat_data)):
        if flat_data[i] == current_num:
            current_run_size += 1

        elif(flat_data[i] != current_num):      # start a new run if next number is different from prev number
            encoded_rle.extend([current_run_size])
            encoded_rle.extend([current_num])
            current_num = flat_data[i]
            current_run_size = 1

        if current_run_size >= 15:      # start new run if current run is over 15
            encoded_rle.extend([current_run_size])
            encoded_rle.extend([current_num])
            current_run_size = 0

        if i == len(flat_data) - 1:
            encoded_rle.extend([current_run_size])
            encoded_rle.extend([current_num])

    return encoded_rle

def get_decoded_length(rle_data):       # find the length of decoded data
    decoded_length = 0

    for i in rle_data[0::2]:
        decoded_length += i

    return decoded_length

def decode_rle(rle_data):       # convert data from RLE to flat data
    decoded_rle = []

    rle_num_count = 1
    index = rle_data[0::2]

    for i in index:
        rle_num = rle_data[rle_num_count]
        decoded_rle.extend([rle_num] * i)
        rle_num_count += 2

    return decoded_rle

def string_to_data(data_string):        # convert hex string into data in list
    data = []

    for char in data_string.split(':'):
        for hex_char in char:
            try:    # convert the character to an integer
                data.append(int(hex_char, 16))
            except ValueError:
                data.append(15)

    return data

def to_rle_string(rle_data):        # convert numbers 10-15 into letter hex values
    rle_string = ''

    rle_num_count = 1
    index = rle_data[0::2]

    for num in index:       # converts numbers to hex values
        hex_val = rle_data[rle_num_count]

        if hex_val == 15:
            hex_val = 'f'
        elif hex_val == 14:
            hex_val = 'e'
        elif hex_val == 13:
            hex_val = 'd'
        elif hex_val == 12:
            hex_val = 'c'
        elif hex_val == 11:
            hex_val = 'b'
        elif hex_val == 10:
            hex_val = 'a'
        else:
            hex_val = str(hex_val)

        rle_string += str(num)      # appends values to RLE string
        rle_string += hex_val
        rle_string += ':'
        rle_num_count += 2

    rle_string = rle_string[:-1]

    return rle_string

def string_to_rle(rle_string):      # convert hex string with delimiters to list
    new_rle_string = rle_string.split(':')

    list = []           # converts hex string with delimiters to list
    for val in new_rle_string:
        if val[-1] == 'a' or 'b' or 'c' or 'd' or 'e' or 'f':
            list.append(int(val[0:-1]))
            hex_num = val[-1]
            new_num = int(hex_num, 16)
            list.append(int(new_num))
        else:
            list.append(int(val[0]))
            list.append(int(val[1]))

    return list

# ------------------------------PROGRAM--------------------------------
def main():
    print(f'Welcome to the RLE image encoder!\n')           # prints welcome message & rainbow image
    print(f'Displaying Spectrum Image:')
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)

    program = True
    image = None
    new_list = None

    while program == True:
        # print RLE menu
        print(f'\nRLE Menu\n--------\n0. Exit\n1. Load File\n2. Load Test Image\n3. Read RLE String\n4. Read RLE Hex String\n5. Read Data Hex String\n6. Display Image\n7. Display RLE String\n8. Display Hex RLE Data\n9. Display Hex Flat Data')
        option = int(input('\nSelect a Menu Option: '))    # prompt user for menu option

        if option == 0:
            program = False

        elif option == 1: 
            file = input(f'\nEnter name of file to load: ')     # ask user to input file name
            image = ConsoleGfx.load_file(file)      # assign file name from load_file to image

        elif option == 2: 
            image = ConsoleGfx.test_image      # load image data from test_image and assign ConsoleGfx.test_image to image
            print(f'\nTest image data loaded.')

        elif option == 3:       # RLE string input
            hex_string = input('Enter an RLE string to be decoded: ')
            compressed_list = string_to_rle(hex_string)
            new_list = decode_rle(compressed_list)

        elif option == 4:       # return decompressed data needed to generate the flat data from RLE encoding
            hex_string = input('Enter the hex string holding RLE data: ')
            compressed_list = string_to_data(hex_string)
            new_list = decode_rle(compressed_list)

        elif option == 5:
            hex_string = input('Enter the hex string holding flat data: ')

        elif option == 6:   # displays loaded image
            print('Displaying image...')
            ConsoleGfx.display_image(image)

        elif option == 7:       # display RLE string
            compressed_data = encode_rle(new_list)
            result = to_rle_string(compressed_data)
            print(f'RLE representation: {result}')

        elif option == 8:       # display hex RLE Data
            compressed_data = encode_rle(new_list)
            result = to_hex_string(compressed_data)
            print(f'RLE hex values: {result}')
        
        elif option == 9:       # display flat hex data
            result = to_hex_string(new_list)
            print(f'Flat hex values: {result}')

        else:
            print('Error invalid input.')

if __name__ == "__main__":
    main()


import PIL
import PIL.Image
import binary

def compress(img_path:str, bit_depth:int = 1) -> bytes:
    if bit_depth not in [1, 2, 4, 8]: # we limit the bit depth to these numbers because multiples of these numbers will neatly fill up a fully byte (8 bits). 3 and 6 do not fit in one.
        raise Exception("bit_depth must be set to 1, 2, 4, or 8. " + str(bit_depth) + " is not a valid bit depth.")

    img = PIL.Image.open(img_path)

    # "hopper" of bit values
    hopper:list[bool] = []
    ToReturn:bytearray = bytearray()

    # go through each pixel
    for y in range(img.height):
        for x in range(img.width):

            # determine monochrome value
            pixel = img.getpixel((x, y))
            monochrome:int = int((pixel[0] + pixel[1] + pixel[2]) / 3)

            # determine what bits to add
            number_of_options_in_bit_depth:int = 2 ** bit_depth # the number of unique options available in this bit depth.
            max_value_at_bit_depth:int = number_of_options_in_bit_depth - 1 # for example, the number of options could be 16, but that is 0-15, so 15 is the max!
            scaled:int = int(number_of_options_in_bit_depth * (monochrome / 255)) # scale the monochrome value (between 0 and 255) to a value between 0 and the ceiling that the bit depth allows us. For example, if at bit depth of 4, this means we have the range between 0 and 16. So scale to within that range.
            bits_value_bools:list[bool] = binary.byte_to_bits(scaled) # convert the scaled integer value to a series of bit values
            
            # add the last bits (determined by bit depth) to the hopper
            bits_portion_of_depth:list[bool] = bits_value_bools[-bit_depth:] # chop off the leading bools that don't matter because of our low bit depth (collect right-most)
            hopper.extend(bits_portion_of_depth) # add that to the hopper!

            # if hopper is now at 8, dump a byte!
            if len(hopper) == 8:
                ToReturn.append(binary.bits_to_byte(hopper)) # convert and append
                hopper.clear() # clear

    return bytes(ToReturn)

def reconstruct(bs:bytes, width:int, height:int, bit_depth:int = 1) -> PIL.Image.Image:
    ToReturn:PIL.Image.Image = PIL.Image.new("RGB", (width, height))
    
    on_byte:int = 0 # index
    on_bit:int = 0 # index

    # go through each pixel and set accordingly
    for y in range(0, ToReturn.height):
        for x in range(0, ToReturn.width):

            # Get the bits that make up this next pixel (determiend by bit depth)
            this_byte:int = bs[on_byte] # the byte we are on right now
            this_byte_bits:list[bool] = binary.byte_to_bits(this_byte) # conver the byte we are on right now to bits because we will be needing those.
            bit_values:list[bool] = this_byte_bits[on_bit:on_bit + bit_depth] # collect the series of bits, based on bit depth, that will be converted here to a monochrome pixel value!

            # convert the bit values to a byte (integer) value
            scaled_value:int = binary.bits_to_byte(bit_values)
            options_at_bit_depth:int = 2 ** bit_depth
            max_val_at_bit_depth:int = options_at_bit_depth - 1
            scaled_percent:float = scaled_value / max_val_at_bit_depth
            monochrome:int = int(255 * scaled_percent) # scale all the way up to a full monochrome color

            # set the pixel color
            ToReturn.putpixel((x, y), (monochrome, monochrome, monochrome))
            
            # increment for next loop!
            on_bit = on_bit + bit_depth
            if on_bit == 8: # we have surpassed the limit for one byte (8 bits)
                on_byte = on_byte + 1 # go to next byte
                on_bit = 0 # reset on_bit

    return ToReturn


depth = 1
data = compress(r"C:\Users\timh\Downloads\sample.jpg", depth)
print(data)
print(len(data))

img = reconstruct(data, 160, 120, depth)
img.show()
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

            # determine if this is "light" (1) or "dark" (0)
            pixval:bool = False # False = dark
            if monochrome >= 127:
                pixval = True
            
            # add it to the hopper
            hopper.append(pixval)

            # if hopper is now at 8, dump a byte!
            if len(hopper) == 8:
                ToReturn.append(binary.bits_to_byte(hopper)) # convert and append
                hopper.clear() # clear

    return bytes(ToReturn)

def reconstruct(bs:bytes, width:int, height:int) -> PIL.Image.Image:
    ToReturn:PIL.Image.Image = PIL.Image.new("RGB", (width, height))
    
    on_byte:int = 0
    on_bit:int = 0

    # go through each pixel and set accordingly
    for y in range(0, ToReturn.height):
        for x in range(0, ToReturn.width):

            # Get this bit (False = dark, True = light)
            this_byte:int = bs[on_byte]
            this_byte_bits:list[bool] = binary.byte_to_bits(this_byte)
            this_bit:bool = this_byte_bits[on_bit] # the color determined by this

            # determine color
            color:tuple[int, int, int] = (255, 255, 255) # default is dark
            if this_bit: # if it is True
                color = (0, 0, 0) # color is light

            # set the pixel color
            ToReturn.putpixel((x, y), color)
            
            # increment for next loop!
            on_bit = on_bit + 1
            if on_bit == 8: # we have surpassed the limit for one byte (8 bits)
                on_byte = on_byte + 1 # go to next byte
                on_bit = 0 # reset on_bit

    return ToReturn



data = compress(r"C:\Users\timh\Downloads\sample.jpg")
print(data)
print(len(data))

img = reconstruct(data, 160, 120)
img.show()
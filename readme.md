# Bit Depth Image Compression
I developed a novel way for "compressing" (lossy) images to a significantly smaller binary footprint.

I developed this method for use in very low bandwidth scenarios. At some point in the near future, I will probably develop a 3D-printed long range rover system that is capable of transmitting telemetry and other data back at distance using the very powerful, yet rather low bandwidth, LoRa technology.

## Example Usage
```
bit_depth = 1 # can be 1, 2, 4, or 8
data = compress(r"C:\Users\timh\Downloads\sample.jpg", depth)
print(str(len(data)) + " bytes")

img = reconstruct(data, 160, 120, depth)
img.show()
```

## How this is done, step by step.
-  An image is captured - say, 160x120 for example (160 pixel width, 120 pixel height).
    - This is a total of 19,200 bytes.
    - In an RGB scenario, this is 57,600 bytes (one byte per RGB value)! Far too big to be transmitted with LoRa, at least quickly.
- Each RGB pixel of the image is "averaged" to produce a monochrome shade. This reduces the total number of bytes from 57,600 (RGB) back down to 19,200 (one byte per pixel at this point).
- For each pixel in the image, the monochrome value (between 0 and 255) is then reduced to a smaller value. 
- The range of this smaller value (how high it can go) is determined by the **bit depth**, set by the user.
    - The **bit depth** basically determines how many monochrome shades any particular pixel can have.
    - The bit depth set by the user implies how many **bits** each pixel will be presented by.
    - A bit depth of 4 means there are 16 unique shades each pixel can have (2^4=16).
    - A bit depth of 2 means there are 4 unique shades each pixel can have (2^2=4).
    - A bit depth of 1 means there are 2 unique shades each pixel can have (2^1=2). *A bit depth of 1 just means each pixel will only be presented on "dark" or "light"*.
- Once the pixel's monochrome value is scaled to a smaller value, within the confines of the maximum determined by the bit depth, it is then encoded as a number of bits (think of these as True/False values) (*the number of bits it is encoded is is the bit depth!*)
- These bits are piled onto the remaining chain of bits. 
- These bits are converted into a series of byte values that represent this image.

## Image Compression Results
This lossy image compression can drastically decrease the binary footprint of an image. For a 160x120 image, this allows the number of bytes to fall from 19,200 (full monochrome image) to:
- 9,600 bytes @ bit-depth of 4 (50% of original monochrome image)
- 4,800 bytes @ bit-depth of 2 (25% of original monochrome image)
- 2,400 bytes @ bit depth of 1 (12.5% of original monochrome image)

However, please keep in mind, **a lot of fidelity is lost in this process**. Especially at small bit-depths, the resulting image may be unrecognizable. Please perform testing to find the right balance between compression and quality.

## How an Image is Reconstructed
The process of going from the compressed image bytes and an image is the same process as described above, but in reverse. Each pixel's bit representation (determined by bit depth) is used to determine the monochrome shade (between 0 and 255) of each pixel. 
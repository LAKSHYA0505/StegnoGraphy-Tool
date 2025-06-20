from PIL import Image
import os
import struct
import math




### ===================== BASIC FUNTIONS ===================== ###
def text_to_binary(data_bytes):
    binary_string = ''.join(format(byte, '08b') for byte in data_bytes)
    return binary_string



def create_header(data_length_bits, extension):
    length_packed = struct.pack('!I', data_length_bits)
    # Remove padding - use exact extension without spaces
    extension_clean = extension.lstrip('.').strip().lower()[:4]
    extension_packed = extension_clean.encode('ascii')
    # Pad to exactly 4 bytes if needed
    if len(extension_packed) < 4:
        extension_packed += b' ' * (4 - len(extension_packed))
    header=length_packed + extension_packed
    return header
    


def get_secret_data(input_type):
    if input_type == "text":
        secret_message = input("Enter your secret message: ")
        secret_bytes = secret_message.encode('utf-8')
        file_extension = "txt"
        
    elif input_type == "file":
        file_path = input("Enter the path to your secret file (e.g., secret.pdf): ")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError("Secret file not found!")
        
        with open(file_path, "rb") as f:
            secret_bytes = f.read()
        
        # Automatically extract extension from filename
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lstrip('.').strip().lower()  # Remove dot, Pad/truncate to 4 chars
    
    else:
        raise ValueError("Invalid input type. Must be 'text' or 'file'.")

    return secret_bytes, file_extension

def calculate_image_capacity(image):
    try:
        width, height = image.size
        total_pixels = width * height
        usable_bits = (total_pixels * 3) - 64
        if usable_bits < 0:
            raise ValueError("Image too small to store even the header.")
        return usable_bits // 8
    except Exception as e:
        raise RuntimeError(f"Failed to calculate image capacity: {e}")



### ===================== EMBEEDING ===================== ###

def embed_message_into_image(original_image_path,stego_image_path,input_type):
    try:
        img=Image.open(original_image_path)
        img = img.convert("RGB") #image is in RGB mode for consistent pixel access
        pixels = img.getdata() #get pixel dta as sequence of (R,G,B) tuples
        print(f"Image Mode:{img.mode}")
        print(f"Image Size:{img.size}")
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"Failed to load image: {e}")

    secret_message_bytes,file_extension=get_secret_data(input_type)
    binary_secret_message = text_to_binary(secret_message_bytes)
    data_length = len(binary_secret_message)
    header = create_header(data_length, file_extension)
    # Convert header and message to binary together
    final_binary_message = text_to_binary(header) + binary_secret_message


    #chceking if the cover image can store the given message
    usable_bits= calculate_image_capacity(img)
    if len(final_binary_message) > usable_bits*8:
        raise ValueError(
            f"[❌] Data too large for this image! "
            f"Requires {len(final_binary_message)} bits, but only {usable_bits} bits are available."
        )


    pixel_list = list(pixels)
    new_pixels = []
    data_index = 0
    message_length = len(final_binary_message)

    for pixel in pixel_list:
        r, g, b = pixel
        new_rgb = []

        for color in (r, g, b):
            if data_index < message_length:
                bit = int(final_binary_message[data_index])
                new_color = (color & ~1) | bit  # Replace LSB
                data_index += 1
            else:
                new_color = color
            new_rgb.append(new_color)

        new_pixels.append(tuple(new_rgb))
    #creating a new image with embeeded lsb 
    stego_image = Image.new(img.mode, img.size)
    stego_image.putdata(new_pixels)
    stego_image.save(stego_image_path)
    print(f"[✅]Stego image saved as '{stego_image_path}'")




### ===================== EXTRACTION ===================== ###

def extract_message_from_image(stego_image_path):
    try:
        img = Image.open(stego_image_path)
        img = img.convert("RGB")
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"Failed to open stego image: {e}")

    pixels = list(img.getdata())
    # Collect all bits from the image
    all_bits = []
    for r, g, b in img.getdata():
        all_bits.extend([str(r & 1), str(g & 1), str(b & 1)])
    all_bits = ''.join(all_bits)


    # Extract header from first 64 bits
    if len(all_bits) < 64:
        raise ValueError("Image too small to contain header")

    header_bits = all_bits[:64]
    message_length = int(header_bits[:32], 2)
    ext_bits = all_bits[32:64]
  
    extension = ''.join(chr(int(ext_bits[i:i+8], 2)) for i in range(0, 32, 8)).strip().lstrip('.')

    print(f"[ℹ️] Message length (bits): {message_length}")
    print(f"[ℹ️] File extension: '{extension}'")

    # Extract message bits (starts after 64 bits)
    if len(all_bits) < 64 + message_length:
        raise ValueError("Image does not contain full message")
    
    message_bits = all_bits[64:64+message_length]

    # Convert to bytes
    secret_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        if i+8 <= len(message_bits):
            secret_bytes.append(int(message_bits[i:i+8], 2))

    # Handle output
    if extension == "txt":
        try:
            message = secret_bytes.decode('utf-8')
            print("[✅] Secret Message:")
            print(message)
        except UnicodeDecodeError:
            print("[⚠️] Could not decode as UTF-8. Saving as binary file")
            extension = "bin"  # Fallback extension
            output_file = f"extracted_secret.{extension}"
            with open(output_file, 'wb') as f:
                f.write(secret_bytes)
            print(f"[✅] Secret saved as: {output_file}")
    else:
        extension = extension.lstrip('.').strip()
        output_file = f"extracted_secret.{extension}"
        with open(output_file, 'wb') as f:
            f.write(secret_bytes)
        print(f"[✅] Secret file saved as: {output_file}")


### ===================== MAIN ===================== ###

if __name__=="__main__":
    print("\n=== Steganography Suite ===")
    mode=input("Enter mode(embeed or extract)").strip().lower()

    if(mode=="embeed"):
        original_image_path = input("Enter the original image path")
        stego_image_path = input("Enter the stego image path")
        input_type = input("Do you want to hide 'text' or a 'file'? (type 'text' or 'file'): ").strip().lower()
        embed_message_into_image(original_image_path,stego_image_path,input_type)
    elif(mode=="extract"):
        stego_image_path=input("Enter the stego image path")
        extract_message_from_image(stego_image_path)
    else:
        print("Enter a valid mode")

from PIL import Image
import os
import struct

### ===================== BASIC FUNCTIONS ===================== ###
def text_to_binary(data_bytes):
    return ''.join(format(byte, '08b') for byte in data_bytes)

def create_header(data_length_bits, extension):
    length_packed = struct.pack('!I', data_length_bits)
    extension_clean = extension.lstrip('.').strip().lower()
    extension_padded = extension_clean.ljust(4)[:4]
    extension_packed = extension_padded.encode('ascii')
    header = length_packed + extension_packed
    return text_to_binary(header)

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

        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lstrip('.')

    else:
        raise ValueError("Invalid input type. Must be 'text' or 'file'.")

    return secret_bytes, file_extension

def calculate_image_capacity(image):
    width, height = image.size
    total_pixels = width * height
    usable_bits = (total_pixels * 3) - 64  # 64 bits reserved for header
    if usable_bits < 0:
        raise ValueError("Image too small to store even the header.")
    return usable_bits

### ===================== EMBEDDING ===================== ###
def embed_message_into_image(original_image_path, stego_image_path, input_type):
    img = Image.open(original_image_path).convert("RGB")
    pixels = list(img.getdata())

    secret_message_bytes, file_extension = get_secret_data(input_type)
    binary_secret_message = text_to_binary(secret_message_bytes)
    data_length = len(binary_secret_message)
    header = create_header(data_length, file_extension)
    final_binary_message = header + binary_secret_message

    usable_bits = calculate_image_capacity(img)
    if len(final_binary_message) > usable_bits:
        raise ValueError(
            f"[❌] Data too large for this image! Needs {len(final_binary_message)} bits, available {usable_bits} bits."
        )

    new_pixels = []
    data_index = 0
    for pixel in pixels:
        r, g, b = pixel
        new_rgb = []
        for color in (r, g, b):
            if data_index < len(final_binary_message):
                bit = int(final_binary_message[data_index])
                new_color = (color & ~1) | bit
                data_index += 1
            else:
                new_color = color
            new_rgb.append(new_color)
        new_pixels.append(tuple(new_rgb))

    stego_image = Image.new(img.mode, img.size)
    stego_image.putdata(new_pixels)
    stego_image.save(stego_image_path)
    print(f"[✅] Stego image saved as '{stego_image_path}'")

### ===================== EXTRACTION ===================== ###
def extract_message_from_image(stego_image_path):
    img = Image.open(stego_image_path).convert("RGB")
    pixels = list(img.getdata())
    
    # Extract all bits from the image
    all_bits = []
    for r, g, b in pixels:
        all_bits.append(str(r & 1))
        all_bits.append(str(g & 1))
        all_bits.append(str(b & 1))
    all_bits = ''.join(all_bits)

    # Extract header from first 64 bits
    if len(all_bits) < 64:
        raise ValueError("Image too small to contain header")
    
    header_bits = all_bits[:64]
    
    # Parse message length (first 32 bits)
    message_length = int(header_bits[:32], 2)
    
    # Parse extension (next 32 bits)
    extension_bytes = bytes(int(header_bits[i:i+8], 2) for i in range(32, 64, 8))
    extension = extension_bytes.decode('ascii', errors='ignore').strip().lstrip('.')
    
    print(f"[ℹ️] Message length: {message_length} bits")
    print(f"[ℹ️] File extension: {extension}")

    # Extract message bits (after the header)
    if len(all_bits) < 64 + message_length:
        raise ValueError("Image does not contain full message")
    
    message_bits = all_bits[64:64+message_length]
    
    # Convert bits to bytes
    secret_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        if i+8 <= len(message_bits):
            byte_val = int(message_bits[i:i+8], 2)
            secret_bytes.append(byte_val)

    # Handle output
    if extension == "txt":
        try:
            print("[✅] Secret message:")
            print(secret_bytes.decode('utf-8'))
        except UnicodeDecodeError:
            print("[⚠️] Could not decode text. Saving as binary file")
            with open("extracted_secret.bin", "wb") as f:
                f.write(secret_bytes)
            print("[✅] Saved as extracted_secret.bin")
    else:
        output_path = f"extracted_secret.{extension}"
        with open(output_path, "wb") as f:
            f.write(secret_bytes)
        print(f"[✅] Secret file saved as: {output_path}")

### ===================== MAIN ===================== ###
if __name__ == "__main__":
    print("\n=== Steganography Suite ===")
    mode = input("Enter mode ('embed' or 'extract'): ").strip().lower()

    if mode == "embed":
        original_image_path = input("Enter original image path: ")
        stego_image_path = input("Enter output image path (stego image): ")
        input_type = input("Hide 'text' or a 'file'? ").strip().lower()
        embed_message_into_image(original_image_path, stego_image_path, input_type)
    elif mode == "extract":
        stego_image_path = input("Enter stego image path: ")
        extract_message_from_image(stego_image_path)
    else:
        print("[!] Invalid mode. Use 'embed' or 'extract'.")

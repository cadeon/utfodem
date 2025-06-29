import random
import argparse
import math

# Unicode ranges
RANGE_1 = (0x4E00, 0x9FFF)
RANGE_2 = (0x3400, 0x4DBF)
RANGE_3 = (0xAC00, 0xD7AF)

# Build codex
CODEX = (
    [chr(i) for i in range(RANGE_1[0], RANGE_1[1] + 1)] +
    [chr(i) for i in range(RANGE_2[0], RANGE_2[1] + 1)] +
    [chr(i) for i in range(RANGE_3[0], RANGE_3[1] + 1)]
)
CODEX_SIZE = len(CODEX)
PAIR_SIZE = CODEX_SIZE ** 2
ASCII_SIZE = 128

def get_shuffled_codex(seed_char):
    random.seed(ord(seed_char))
    shuffled = CODEX.copy()
    random.shuffle(shuffled)
    return shuffled

def encode(text):
    # Replace specific non-ASCII characters with their ASCII counterparts
    translation_table = str.maketrans({'’': "'", '‘': "'", '“': '"', '”': '"'})
    cleaned_text = text.translate(translation_table)

    seed_char = random.choice(CODEX)
    codex = get_shuffled_codex(seed_char)
    
    # Convert ASCII to base-128 number
    num = 0
    for char in cleaned_text:
        num = num * ASCII_SIZE + ord(char)

    # Encode to base-PAIR_SIZE
    pairs = []
    while num > 0:
        digit = num % PAIR_SIZE
        first = digit // CODEX_SIZE
        second = digit % CODEX_SIZE
        pairs.append(codex[first] + codex[second])
        num //= PAIR_SIZE

    if not pairs:
        pairs.append(codex[0] + codex[0])

    encoded_text = seed_char + ''.join(reversed(pairs))
    return encoded_text

def decode(encoded):
    if not encoded:
        return ""
    
    seed_char = encoded[0]
    codex = get_shuffled_codex(seed_char)
    reverse_codex = {c: i for i, c in enumerate(codex)}
    
    # Convert pairs back to base-128
    num = 0
    for i in range(1, len(encoded), 2):
        if i + 1 >= len(encoded):
            break
        first, second = encoded[i], encoded[i + 1]
        if first not in reverse_codex or second not in reverse_codex:
            raise ValueError(f"Invalid codex character at position {i} with characters {first}{second}")
        digit = reverse_codex[first] * CODEX_SIZE + reverse_codex[second]
        num = num * PAIR_SIZE + digit
    
    # Convert number to ASCII
    decoded = ""
    while num > 0:
        if num % ASCII_SIZE == 0: break
        decoded = chr(num % ASCII_SIZE) + decoded
        num //= ASCII_SIZE

    # Debugging output for the specific case with $ characters
    if '$' in decoded:
        print(f"Debug: Encoded text: {encoded}")
        print(f"Debug: Seed char: {seed_char}")
        print(f"Debug: Decoded pairs: ...")
        print(f"Debug: Final decoded text: {decoded}")

    return decoded

def main():
    parser = argparse.ArgumentParser(description="Encode or decode a string using UTF-8 codex.")
    parser.add_argument("--encode", type=str, help="String to encode")
    parser.add_argument("--decode", type=str, help="String to decode")
    args = parser.parse_args()

    if args.encode and args.decode:
        print("Error: Please provide either --encode or --decode, not both.")
        return
    elif args.encode:
        encoded = encode(args.encode)
        print(f"Original: {args.encode} ({len(args.encode)} chars)")
        print(f"Encoded: {encoded} ({len(encoded)} chars)")
    elif args.decode:
        try:
            decoded = decode(args.decode)
            print(f"Encoded: {args.decode} ({len(args.decode.encode('utf-8'))} bytes)")
            print(f"Decoded: {decoded} ({len(decoded.encode('utf-8'))} bytes")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        # Run default tests
        for text in [
            "Hello, World!",
            "Hello, World! This is a test of compression.",
            "The quick brown fox jumps over the lazy dog. " * 5
        ]:
            encoded = encode(text)
            print(f"\nOriginal: {text[:50]}{'...' if len(text) > 50 else ''} ({len(text.encode('utf-8'))} bytes)")
            print(f"Encoded: {encoded[:50]}{'...' if len(encoded) > 50 else ''} ({len(encoded.encode('utf-8'))} bytes)")
            decoded = decode(encoded)
            print(f"Decoded: {decoded[:50]}{'...' if len(decoded) > 50 else ''}")
            assert decoded == text

if __name__ == "__main__":
    main()
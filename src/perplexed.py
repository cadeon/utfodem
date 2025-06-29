import random
import argparse

# Unicode ranges for codex (as in your code)
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

def get_shuffled_codex(seed_char):
    random.seed(ord(seed_char))
    shuffled = CODEX.copy()
    random.shuffle(shuffled)
    return shuffled

def encode(text):
    # Encode input as UTF-8 bytes (handles all Unicode)
    data = text.encode('utf-8')
    num = int.from_bytes(data, 'big') if data else 0

    # Pick a random seed char for codex shuffling
    seed_char = random.choice(CODEX)
    codex = get_shuffled_codex(seed_char)

    # Convert number to base-CODEX_SIZE
    chars = []
    base = CODEX_SIZE
    if num == 0:
        chars.append(codex[0])
    else:
        while num > 0:
            chars.append(codex[num % base])
            num //= base

    # Prepend seed_char for decoding
    return seed_char + ''.join(reversed(chars))

def decode(encoded):
    if not encoded:
        return ""
    seed_char = encoded[0]
    codex = get_shuffled_codex(seed_char)
    base = CODEX_SIZE
    num = 0
    for c in encoded[1:]:
        idx = codex.index(c)
        num = num * base + idx
    # Convert integer back to bytes
    if num == 0:
        return ""
    # Calculate minimum bytes needed
    byte_length = (num.bit_length() + 7) // 8
    data = num.to_bytes(byte_length, 'big')
    return data.decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description="Encode or decode a string using a large Unicode codex.")
    parser.add_argument("--encode", type=str, help="String to encode")
    parser.add_argument("--decode", type=str, help="String to decode")
    args = parser.parse_args()

    if args.encode and args.decode:
        print("Error: Please provide either --encode or --decode, not both.")
        return
    elif args.encode:
        encoded = encode(args.encode)
        print(f"Original: {args.encode} ({len(args.encode)} chars, {len(args.encode.encode('utf-8'))} bytes)")
        print(f"Encoded: {encoded} ({len(encoded)} chars, {len(encoded.encode('utf-8'))} bytes)")
    elif args.decode:
        try:
            decoded = decode(args.decode)
            print(f"Encoded: {args.decode} ({len(args.decode)} chars, {len(args.decode.encode('utf-8'))} bytes)")
            print(f"Decoded: {decoded} ({len(decoded)} chars, {len(decoded.encode('utf-8'))} bytes)")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Run sample tests
        for text in [
            "Hello, World!",
            "Привет, мир!",
            "你好，世界！",
            "こんにちは世界🌏",
            "The quick brown 🦊 jumps over the lazy 🐶. " * 3,
            "😀😃😄😁😆😅😂🤣☺️😊",
        ]:
            encoded = encode(text)
            print(f"\nOriginal: {text[:50]}{'...' if len(text) > 50 else ''} ({len(text)} chars, {len(text.encode('utf-8'))} bytes)")
            print(f"Encoded: {encoded[:50]}{'...' if len(encoded) > 50 else ''} ({len(encoded)} chars, {len(encoded.encode('utf-8'))} bytes)")
            decoded = decode(encoded)
            print(f"Decoded: {decoded[:50]}{'...' if len(decoded) > 50 else ''}")
            assert decoded == text

if __name__ == "__main__":
    main()

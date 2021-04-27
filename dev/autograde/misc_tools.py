"""
Miscellaneuos tools
Created Apr 18th, 2021
"""

def nice_text(longtext, truncate=False, maxlen=50):
    txt = longtext
    if truncate and (len(longtext) > maxlen):
        txt = longtext[:(maxlen-4)] + "..." + longtext[-1]
    
    return txt


def pack_message(txt):
    """
    Turn a text with '\n' or '\r' and ' ' into a corresponding text without '\n', '\r', or ' '.
    """
    packed = txt.replace("\r", "\n")
    packed = packed.replace("\n", "\\n")
    packed = packed.replace(" ", "[sp]")

    return packed
# end pack_message

def unpack_message(packed):
    unpacked = packed.replace("[sp]", " ")
    unpacked = unpacked.replace("\\n", "\n")
    return unpacked

if __name__ == '__main__':
    txt = """line1 has some words.
line2 is not much different.
Line 3 I start to have nothing to say."""

    print(txt)

    print("\nPacked to:\n", pack_message(txt))

    print("Test nice_txt")
    txt = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.1"
    print(txt)
    print(nice_text(txt, truncate=True, maxlen=20))

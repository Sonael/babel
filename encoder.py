# python
def generate_babel_alphabet():
    letters = "abcdefghijklmnopqrstuvwxyz"
    return letters + " ." + ","

def create_mapping(alphabet):
    """Cria um mapeamento de caracteres ASCII para sequências da Babel."""
    mapping = {}
    babel_chars = [c for c in alphabet]
    
    for char in babel_chars:
        mapping[ord(char)] = char

    count = 0
    
    for i in range(128):
        if i not in mapping:
            first = babel_chars[count // len(babel_chars)]
            second = babel_chars[count % len(babel_chars)]
            mapping[i] = "." + first + second
            count += 1
            if count >= len(babel_chars)**2:
                break
    return mapping

def encode_to_babel(text):
    babel_alphabet = generate_babel_alphabet()
    char_mapping = create_mapping(babel_alphabet)
    
    encoded_string = ""
    for char in text:
        char_code = ord(char)
        if char_code > 127:
            raise ValueError(f"O caractere '{char}' não é ASCII e não pode ser codificado.")
        encoded_string += char_mapping[char_code]

    return encoded_string

def decode_from_babel(encoded_text):
    babel_alphabet = generate_babel_alphabet()
    # Inverte o mapeamento para decodificação
    mapping = create_mapping(babel_alphabet)
    reverse_mapping = {v: k for k, v in mapping.items()}

    decoded_string = ""
    i = 0
    while i < len(encoded_text):
        found = False
        
        # Tenta decodificar 3 caracteres (separador + 2)
        if i + 3 <= len(encoded_text) and encoded_text[i] == ".":
            chunk = encoded_text[i:i+3]
            if chunk in reverse_mapping:
                decoded_string += chr(reverse_mapping[chunk])
                i += 3
                found = True
        
        # Se não encontrou uma sequência de 3, tenta decodificar 1 caractere
        if not found:
            char = encoded_text[i]
            if char in reverse_mapping:
                decoded_string += chr(reverse_mapping[char])
                i += 1
            else:
                i += 1
                #print(f"Ignorando caractere inválido: {char}")

    return decoded_string
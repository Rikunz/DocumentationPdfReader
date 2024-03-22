import sys

# Membuat sebuah variabel
my_variable = "Hello, World!"

# Mendapatkan ukuran memori variabel dalam byte
memory_size = sys.getsizeof(my_variable)

print("Ukuran memori variabel (dalam byte):", memory_size)
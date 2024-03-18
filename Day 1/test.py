import io

f = io.BytesIO(b"some initial binary data: \x00\x01")
print(io.BufferedIOBase.readline(f))
import urllib.request

# 파일 다운로드
url = "https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2"
filename = "shape_predictor_68_face_landmarks.dat.bz2"
urllib.request.urlretrieve(url, filename)

# 압축 해제
import bz2
with open("shape_predictor_68_face_landmarks.dat", "wb") as new_file, open("shape_predictor_68_face_landmarks.dat.bz2", "rb") as file:
    decompressor = bz2.BZ2Decompressor()
    for data in iter(lambda : file.read(100 * 1024), b''):
        new_file.write(decompressor.decompress(data))

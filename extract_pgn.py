from zipfile import ZipFile

for i in range(920, 1498):

    with ZipFile(f"twic{i}g.zip", 'r') as zObject:
        zObject.extractall()

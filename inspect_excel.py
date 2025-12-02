import openpyxl

FILE_NAME = "dados.xlsx"

try:
    wb = openpyxl.load_workbook(FILE_NAME)
    ws = wb.active
    
    # Get unique values for specific columns
    # 7: Gênero, 8: Ano Escolar, 12: Interesse Tecnologia
    
    generos = set()
    anos = set()
    interesses_tech = set()
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[7]: generos.add(row[7])
        if row[8]: anos.add(row[8])
        if row[12]: interesses_tech.add(row[12])
        
    print("\nUnique Generos:", generos)
    print("Unique Anos:", anos)
    print("Unique Interesse Tech:", interesses_tech)
        
except Exception as e:
    print(f"Error: {e}")

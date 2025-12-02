import openpyxl

FILE_NAME = "dados.xlsx"

def check_values():
    try:
        wb = openpyxl.load_workbook(FILE_NAME)
        ws = wb.active
        
        contatos = set()
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[17]: # contato_programacao
                contatos.add(row[17])
        
        print("Valores unicos para contato_programacao:", contatos)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_values()

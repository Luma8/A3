import openpyxl
from collections import Counter

FILE_NAME = "dados.xlsx"

def debug_profiles():
    try:
        wb = openpyxl.load_workbook(FILE_NAME)
        ws = wb.active
        
        avaliacoes = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is not None:
                avaliacoes.append({
                    "genero": row[7],
                    "ano_escolar": row[8],
                    "interesse_tecnologia": row[12]
                })
        
        print(f"Total avaliacoes: {len(avaliacoes)}")
        
        def filter_group(gender, year, tech_interest_levels):
            return [
                a for a in avaliacoes 
                if a['genero'] == gender 
                and a['ano_escolar'] == year 
                and a['interesse_tecnologia'] in tech_interest_levels
            ]

        tech_levels = ['Muito interesse']
        humanas_levels = ['Pouco interesse']
        
        groups = [
            ('Homem', '2º ano'),
            ('Homem', '3º ano'),
            ('Mulher', '2º ano'),
            ('Mulher', '3º ano')
        ]
        
        print("\n--- TECH (Muito interesse) ---")
        for g, y in groups:
            count = len(filter_group(g, y, tech_levels))
            print(f"{g} - {y}: {count}")

        print("\n--- HUMANAS (Pouco interesse) ---")
        for g, y in groups:
            count = len(filter_group(g, y, humanas_levels))
            print(f"{g} - {y}: {count}")
            
        print("\n--- Distribution of Interest ---")
        interests = [a['interesse_tecnologia'] for a in avaliacoes]
        print(Counter(interests))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_profiles()

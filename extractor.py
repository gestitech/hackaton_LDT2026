# pip install pyzipper
# положить скрипт в одну папку с архивом layer_1.zip
# запуск python extractor.py
import pyzipper
import os
import glob

def extract_layers():
    current_zip = "layer_1.zip"
    layer_num = 1
    
    while os.path.exists(current_zip):
        password = str(layer_num).encode()
        
        print(f"[{layer_num}/1337] Extracting {current_zip}...")
        
        try:
            with pyzipper.AESZipFile(current_zip, 'r') as zip_ref:
                zip_ref.extractall(pwd=password)
            
            # Удаляем текущий архив (опционально)
            os.remove(current_zip)
            
            # Находим следующий zip файл
            next_zips = glob.glob("layer_*.zip")
            
            if next_zips:
                # Сортируем по номеру
                next_zips.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
                current_zip = next_zips[0]
                layer_num += 1
            else:
                print(f"\nFinal layer reached!")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print("\n" + "="*50)
    print("Extraction complete!")
    print("="*50)
    
    # Показываем финальные файлы
    remaining = [f for f in os.listdir('.') if not f.endswith('.py')]
    if remaining:
        print("\nFinal extracted files:")
        for f in remaining:
            print(f"  → {f}")

if __name__ == "__main__":
    extract_layers()

import re
def dosya_oku(dosya_adi):
    with open(dosya_adi, 'r', encoding='utf-8') as dosya:
        satirlar = dosya.readlines()
    return satirlar




def satir_isle(satir, satir_numarasi, global_vars, local_vars):
    satir = satir.strip()
    if satir.startswith('yaz("') or satir.startswith('yaz (') or satir.startswith('yaz('):
        # yaz("...") ifadesi
        if satir.endswith(');'):
            icerik = satir[satir.find('(') + 1: -2].strip()
            try:
                exec(f'print({icerik})', global_vars, local_vars)
                return None
            except Exception as e:
                return f"{satir_numarasi}. satırda hata: {e}"
        else:
            return None, f"{satir_numarasi}. satırda hata: ; eksik"
    elif re.match(r'^[a-zA-Z_]\w*\s*=\s*.*;$', satir):
        # Değişken tanımlaması ve atama ifadesi
        try:
            exec(satir[:-1].strip(), global_vars, local_vars)
            return None
        except Exception as e:
            return f"{satir_numarasi}. satırda hata: {e}"
    elif not satir.endswith(';') and satir != '':
        return f"{satir_numarasi}. satırda hata: ; eksik"
    return None

def cok_satirli_isle(satirlar, baslangic_numarasi):
    satir = satirlar[baslangic_numarasi].strip()
    metin = satir[satir.find('("') + 2:]  # 'yaz("' veya 'yaz ("' kısmını çıkart
    for i in range(baslangic_numarasi + 1, len(satirlar)):
        satir = satirlar[i].strip()
        if satir.endswith('");'):
            metin += "\n" + satir[:-3]
            return f'print("""{metin}""")', i + 1, None
        else:
            metin += "\n" + satir
    return None, len(satirlar), f"{baslangic_numarasi + 1}. satırdan itibaren hata: ; eksik"

def kendi_yazilim_dilim(dosya_adi):
    satirlar = dosya_oku(dosya_adi)
    satir_numarasi = 0
    global_vars = {}
    local_vars = {}
    while satir_numarasi < len(satirlar):
        satir = satirlar[satir_numarasi].strip()
        if satir.startswith('yaz("') or satir.startswith('yaz (') or satir.startswith('yaz('):
            if satir.endswith(');'):
                hata = satir_isle(satir, satir_numarasi + 1, global_vars, local_vars)
                if hata:
                    print(hata)
                satir_numarasi += 1
            else:
                islenmis_satir, sonraki_satir_numarasi, hata = cok_satirli_isle(satirlar, satir_numarasi)
                if hata:
                    print(hata)
                    satir_numarasi = sonraki_satir_numarasi
                elif islenmis_satir:
                    exec(islenmis_satir, global_vars, local_vars)
                    satir_numarasi = sonraki_satir_numarasi
        else:
            hata = satir_isle(satir, satir_numarasi + 1, global_vars, local_vars)
            if hata:
                print(hata)
            satir_numarasi += 1

# Örnek kullanım
kendi_yazilim_dilim('main.thn')

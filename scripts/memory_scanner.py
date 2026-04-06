import ctypes
import sys

# Oyunun PID'sine göre bellekte (memory) pointer arama simülasyonu
# Kernel düzeyinde Windows API (ReadProcessMemory) kullanımı

PROCESS_ALL_ACCESS = 0x1F0FFF

def read_memory(process_id, address):
    """
    Verilen Process ID'nin bellek adresindeki 4 byte'lık değeri okur.
    Statik analiz sonrası bulunan offset değerlerini dinamik olarak test etmek içindir.
    """
    print(f"[*] {process_id} PID'li sürece (process) bağlanılıyor...")
    
    # Windows API kernel32.dll kütüphanesi yükleniyor
    k32 = ctypes.windll.kernel32
    
    # Sürece (oyuna) erişim izni (handle) alınıyor
    process_handle = k32.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)
    if not process_handle:
        print("[-] HATA: Sürece erişilemedi. Yönetici (Admin) haklarıyla çalıştırın veya Anti-Cheat engelledi.")
        return None
    
    print(f"[+] Başarılı: Kernel seviyesi erişim sağlandı. Adres taranıyor: {hex(address)}")
    
    buffer = ctypes.c_uint()
    bytes_read = ctypes.c_ulong()
    
    # Belleği Oku (ReadProcessMemory)
    result = k32.ReadProcessMemory(
        process_handle, 
        ctypes.c_void_p(address), 
        ctypes.byref(buffer), 
        ctypes.sizeof(buffer), 
        ctypes.byref(bytes_read)
    )
    
    if result:
        print(f"[+] Adres: {hex(address)} | Bulunan Değer: {buffer.value}")
        return buffer.value
    else:
        print("[-] Bellek okuma başarısız (Page Fault veya korumalı bölgeye denk gelindi).")
        return None

if __name__ == "__main__":
    # Örnek kullanım (Videodaki analizde bulunan offset değerlerine göre)
    # NOT: Projenin asıl uygulamalı, tam teşekküllü analizi README'deki YouTube demosundadır.
    TARGET_PID = 1337
    TARGET_BASE_ADDRESS = 0x7FF6B3B00000 
    OFFSET = 0x2A4C
    
    print("=== Oyun İçi Dinamik Bellek Analizörü (Memory Scanner) ===")
    read_memory(TARGET_PID, TARGET_BASE_ADDRESS + OFFSET)

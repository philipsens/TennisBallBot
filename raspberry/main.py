from scanner.ble_scanner import BLEScanner

if __name__ == '__main__':
    scanner = BLEScanner();

    scanner.start("00000000-0000-0000-0000-000000000000")

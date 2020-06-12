from scanner.ble_scanner import BLEScanner

if __name__ == '__main__':
    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")

    try:
        scanner.start()
    except KeyboardInterrupt:
        scanner.stop()

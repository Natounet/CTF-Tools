# Recovering Deleted Files

Using the **Autopsy** software on the `disk.img`, the following deleted files were recovered:

- **w0rdl1st_old.txt**: Appears to be a wordlist used for password cracking.
- **f0016696.pcap**: A network capture file containing wireless traffic data.
- **f0016680.xml**: An output file from Kismet, containing detailed Wi-Fi information.

# File Analysis

## Kismet Log File Analysis

The Kismet log file provided critical information about the target network:

- **SSID**: `Freebox-F726` (the network name we are targeting).
- **MAC Address (BSSID)**: `3A:02:8E:7D:03:C8` (the unique identifier for the Wi-Fi network).

## Network Capture Analysis

The `f0016696.pcap` file contains captured wireless traffic, including authentication packets. These packets are essential for performing a brute-force attack on the Wi-Fi password.

# Brute-Forcing the Wi-Fi Password

With the following resources:
- The **SSID** (`Freebox-F726`),
- The **MAC Address** (`3A:02:8E:7D:03:C8`),
- The recovered **wordlist** (`w0rdl1st_old.txt`), and
- The **network capture file** (`f0016696.pcap`),

We can utilize the **aircrack-ng** tool to attempt password recovery. The command used:

```bash
aircrack-ng -w ./w0rdl1st_old.txt -b "3A:02:8E:7D:03:C8" ./f0016696.pcap
```

We get the following password `GZVPQpX)c)C#B^V-599+`

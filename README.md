
# NKZ DNS Inspector

A Python-based DNS lookup tool with a dark neon interface, built for networking studies and cybersecurity education.

## Features

- DNS record lookup: A, AAAA, MX, TXT, NS, CNAME and SOA
- Query a specific record type or all supported types
- Display record values and TTL
- Export results to TXT reports
- Dark interface with purple and electric blue accents
- Input validation and error handling
- Windows executable build using PyInstaller

## Preview

The application provides a graphical interface to query DNS records and organize results in a readable table.

## Requirements

- Windows 10/11
- Python 3.11 or newer to build the executable
- Internet connection for DNS lookups

## Installation

Clone the repository:

```bash
git clone https://github.com/NkzAyano/NKZ-DNS-Inspector.git
cd NKZ-DNS-Inspector
```

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

Run the application:

```bash
py main.py
```

## Build the Windows executable

Run:

```text
build.bat
```

The executable will be generated at:

```text
dist/NKZ_DNS_Inspector.exe
```

## Supported DNS records

| Record | Purpose |
|---|---|
| A | IPv4 addresses |
| AAAA | IPv6 addresses |
| MX | Mail servers |
| TXT | Text records |
| NS | Name servers |
| CNAME | Domain aliases |
| SOA | DNS zone information |

## Disclaimer

This project is intended for educational use and legitimate network diagnostics. DNS results may vary depending on the resolver, network configuration and time of the query.

## Author

**NKZ Ayano**

GitHub: [@NkzAyano](https://github.com/NkzAyano)

## License

MIT

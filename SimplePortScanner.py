import nmap

# Initialize scanner
nm = nmap.PortScanner()

# Ask for target IP/hostname
target = input("Enter target IP or hostname: ")

# Define a dictionary of common scan options
scan_types = {
    "1": ("Quick Scan", "-F"),                  # Fast scan (top 100 ports)
    "2": ("Service & Version Detection", "-sV"),
    "3": ("Script Scan", "-sC"),                # Default nmap scripts
    "4": ("OS Detection", "-O"),                # Detect operating system
    "5": ("Aggressive Scan", "-A"),             # OS + version + script + traceroute
    "6": ("Full TCP Scan", "-p-"),              # Scan all 65535 ports
    "7": ("Custom (enter your own)", None)      # Let user type their own options
}

# Show menu
print("\nSelect a scan type:")
for key, (desc, _) in scan_types.items():
    print(f"{key}. {desc}")

# Get user choice
choice = input("Enter choice (1-7): ")

# Pick the right option
if choice in scan_types:
    scan_name, options = scan_types[choice]

    if choice == "7":
        options = input("Enter your custom nmap options: ")

    print(f"\n[+] Running {scan_name} on {target} with options: {options}\n")

    # Run the scan
    nm.scan(target, arguments=options)

    # Print results
    for host in nm.all_hosts():
        print(f"Host: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")

        for protocol in nm[host].all_protocols():
            print(f"Protocol: {protocol}")
            for port in nm[host][protocol]:
                state = nm[host][protocol][port]['state']
                name = nm[host][protocol][port].get('name', 'unknown')
                product = nm[host][protocol][port].get('product', '')
                version = nm[host][protocol][port].get('version', '')
                extrainfo = nm[host][protocol][port].get('extrainfo', '')

                print(f"Port: {port}\tState: {state}\tService: {name} {product} {version} {extrainfo}")
else:
    print("Invalid choice. Exiting.")

import socket

def whois_lookup(domain: str):
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the IANA WHOIS server
    s.connect(("whois.iana.org", 43))
    # Send the domain name with \r\n (required for WHOIS protocol)
    s.send((domain + "\r\n").encode())
    # Receive up to 4096 bytes
    response = s.recv(4096).decode()
    # Close the socket
    s.close()
    return response

domain = input("Enter your desired domain: ")
whois_data = whois_lookup(domain)
print("\nWHOIS Response:\n")
print(whois_data)

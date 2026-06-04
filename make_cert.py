from cert.certificate import DigitalCertificate

cert = DigitalCertificate(
    "Darshan",
    "darshan@gmail.com",
    "ABC123",
    "BlazeCA"
)

cert.save("cert/my_cert.json")

print("Certificate created")
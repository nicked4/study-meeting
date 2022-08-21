# generate secret key
openssl genrsa 2048 > keys/server.key

# print key
openssl rsa -text < keys/server.key

# generate csr
openssl req -new -days 365 -sha256 -key keys/server.key -subj '/C=JP/ST=Tokyo/O=Chiyoda-ku/OU=nike/CN=localhost' > keys/server.csr

# print csr
openssl req -text < keys/server.csr

# certificate
openssl x509 -req -extfile subjectnames.txt -signkey keys/server.key < keys/server.csr > keys/server.crt

# print cert
openssl x509 -text < keys/server.crt


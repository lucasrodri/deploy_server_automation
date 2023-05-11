# Automatic application deployment

This project aims to simplify and automate the continuous integration and delivery process through the use of Github Actions on a server that is not directly accessible via the Internet. This can occur for various reasons, such as the lack of a public IP or being behind a VPN. In order to perform the application deployment, the server must have a web service running and be accessible through a public domain.

The purpose of the project is to enable Github Actions to send a secure, token-authenticated POST request to the aforementioned server. Once this request is received by the server, it is capable of performing the deployment process automatically, thus ensuring a more efficient and secure continuous delivery.

## Apache vhost example

```sh
<VirtualHost *:80>
    ProxyPass /deploy http://localhost:5001
    ProxyPassReverse /deploy http://localhost:5001

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

## How to create a secure token

```py
import secrets

# Generate a 32-byte random token
token = secrets.token_hex(32)
print(token)
```

## Developer

- Lucas Costa @lucasrodri
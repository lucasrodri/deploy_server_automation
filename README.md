# Automatic application deployment

This project aims to simplify and automate the continuous integration and delivery process through the use of Github Actions on a server that is not directly accessible via the Internet. This can occur for various reasons, such as the lack of a public IP or being behind a VPN. In order to perform the application deployment, the server must have a web service running and be accessible through a public domain.

The purpose of the project is to enable Github Actions to send a secure, token-authenticated POST request to the aforementioned server. Once this request is received by the server, it is capable of performing the deployment process automatically, thus ensuring a more efficient and secure continuous delivery.

## Example of service creation in systemd

Create a file in folder `/etc/systemd/system/deploy.service` with the following content:

```sh
[Unit]
Description=Deploy service
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 <path_script.py>

[Install]
WantedBy=multi-user.target
```

Reload the daemon

```sh
sudo systemctl daemon-reload
```

Enable the service

```sh
sudo systemctl enable test.service
```

Start the service

```sh
sudo systemctl start test.service
```

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

## Workflow example

```sh
name: Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Send deploy request
        run: |
          curl -X POST -H "Content-Type: application/json" \
               -H "Authorization: ${{ secrets.SECURE_TOKEN }}" \
               -d '{"deploy": "test_deploy"}' \
               ${{ secrets.SERVER_URL }}
```


## Developer

- Lucas Costa @lucasrodri
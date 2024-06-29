# Resend Mail Webpage
A webpage to send e-mail via Resend API.

Build via Docker Compose, using the Python Flask framework.

## Step 1
Create a [Resend](https://resend.com/home) account.

## Step 2
Add a domain to your Resend account.

## Step 3
Create an API Key of your account.

## Step 4
Clone this repo.
```bash
git clone https://github.com/WilliamPeterMatthew/resend-mail-webpage.git
```

## Step 5
Create an `.env` file
```bash
cp .env.example .env
```

## Step 6
Modify `.env` file
| Variable Name     | Description     | Example     |
| -------- | -------- | -------- |
| RESEND_API_KEY | The API Key you obtained in Step 3 | re_1234567890aBcDeFgHiJkLmNoPqEsTuVw |
| SITE_PASSWORD | Website password to prevent others from abusing it | P@ssw0rd |
| PORT | Port used for external access | 5827 |

## Step 7
Run the project by executing the following command in the directory.
```bash
docker-compose up -d
```

## Congratulations
Now you can access the web page on the port you set in Step 6.

## Optional
You can configure Apache or Nginx to reverse proxy to port 80.

Apache Example
```apache
<VirtualHost *:80>
    ServerName example.com

    ProxyRequests Off
    ProxyPreserveHost On
    ProxyPass / http://localhost:<the port you set in Step 6>/
    ProxyPassReverse / http://localhost:<the port you set in Step 6>/

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Nginx Example
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:<the port you set in Step 6>;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_log /var/log/nginx/resendmail_error.log;
    access_log /var/log/nginx/resendmail_access.log;
}

```

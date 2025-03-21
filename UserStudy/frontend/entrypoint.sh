#!/bin/sh

# Check if certificates already exist
if [ ! -f /etc/letsencrypt/live/yalmazabdullah.com/fullchain.pem ]; then
  echo "Requesting SSL certificate..."
  # Obtain a certificate using Certbot (replace with your email)
  certbot --nginx -d yalmazabdullah.com -d www.yalmazabdullah.com --email yalmaz@ualberta.ca --agree-tos --non-interactive --redirect

   #If certbot fails, exit the script.  This will cause the container to exit,
    # which is important because we don't want to run Nginx without valid certs.
    if [ $? -ne 0 ]; then
         echo "Certbot failed. Exiting."
         exit 1
     fi
else
  echo "SSL certificate already exists."
fi

# Start Nginx in the foreground
echo "Starting Nginx..."
nginx -g 'daemon off;
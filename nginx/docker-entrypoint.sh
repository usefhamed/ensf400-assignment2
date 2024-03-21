#!/usr/bin/env bash

set -e

[ "$DEBUG" == 'true' ] && set -x

DAEMON=nginx

# Copy default config from cache
if [ ! "$(ls -A /etc/nginx)" ]; then
    cp -a /etc/nginx.cache/* /etc/nginx/
fi

# Function to set up SSL certificates and DH parameters for HTTPS
setup_ssl() {
    # Ensure the SSL directory exists
    mkdir -p /etc/nginx/ssl

    # Example of generating a Diffie-Hellman group, can be commented out if not needed
    if [ ! -f /etc/nginx/ssl/dhparam.pem ]; then
        openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
    fi

    # Copy SSL certificates
    # This is a placeholder; in reality, you'd copy your certificates or use a tool like Certbot
    # cp /path/to/your/fullchain.pem /etc/nginx/ssl/
    # cp /path/to/your/privkey.pem /etc/nginx/ssl/
}

# Reload NGINX configuration
reload_nginx() {
    nginx -t && nginx -s reload
}

# Initial SSL setup
setup_ssl

# Add or modify NGINX configurations here
# e.g., setting up reverse proxy configurations, load balancing rules, etc.

# Reload NGINX to apply any changes
reload_nginx

# Add users if WEB_USERS=user:uid:gid set (for running NGINX as non-root users, if required)
if [ -n "${WEB_USERS}" ]; then
    USERS=$(echo $WEB_USERS | tr "," "\n")
    for U in $USERS; do
        IFS=':' read -ra UA <<< "$U"
        _NAME=${UA[0]}
        _UID=${UA[1]}
        _GID=${UA[2]}

        echo ">> Adding user ${_NAME} with uid: ${_UID}, gid: ${_GID}."
        getent group ${_NAME} >/dev/null 2>&1 || groupadd -g ${_GID} ${_NAME}
        getent passwd ${_NAME} >/dev/null 2>&1 || useradd -r -m -p '' -u ${_UID} -g ${_GID} -s /bin/false -c 'NGINX User' ${_NAME}
    done
fi

# Example of a stop function, similar to the original script
stop() {
    echo "Received SIGINT or SIGTERM. Shutting down $DAEMON"
    # Gracefully stop NGINX
    nginx -s quit
    echo "Done."
}

echo "Running $@"
if [[ "$1" == "nginx" ]]; then
    trap stop SIGINT SIGTERM
    $@ &
    pid="$!"
    wait "${pid}" && exit $?
else
    exec "$@"
fi

# # # Use the Alpine base image with OpenRC (similar to the app Dockerfiles)
# # FROM alpine:3.9 as alpine-systemd
# # RUN apk --update --no-cache add openrc nginx && \
# #   ln -sf /sbin/openrc-init /sbin/init

# # # Remove the default Nginx configuration file
# # RUN rm /etc/nginx/conf.d/default.conf

# # # Copy the custom Nginx configuration file
# # COPY nginx.conf /etc/nginx/nginx.conf

# # # Expose the standard port for HTTP
# # EXPOSE 80

# # # Set the entrypoint and command to use OpenRC's init system
# # ENTRYPOINT ["/sbin/init"]
# # CMD ["nginx", "-g", "daemon off;"]


# # Use Alpine Linux as the base image
# FROM alpine:3.9

# # Install OpenRC, Nginx, SSH, and other necessary tools
# RUN apk --update --no-cache add openrc nginx openssh bash && \
#     rc-update add sshd && \
#     rm -f /etc/nginx/conf.d/default.conf && \
#     ln -sf /sbin/openrc-init /sbin/init && \
#     echo "root:root" | chpasswd

# # Copy the custom Nginx configuration into the container
# COPY nginx.conf /etc/nginx/nginx.conf

# # Create the .ssh directory
# RUN mkdir -p /root/.ssh

# # Correctly place the authorized_keys file. Ensure this COPY command
# # is adjusted to match the actual path to your id_rsa_container.pub file.
# COPY ./secrets/id_rsa_container.pub /root/.ssh/authorized_keys


# # Ensure permissions are set correctly on the authorized_keys file
# RUN mkdir /root/.ssh && \
#     chmod 600 /root/.ssh/authorized_keys && \
#     chmod 700 /root/.ssh && \
#     ssh-keygen -A && \
#     rc-update add nginx default

# # Expose the standard ports for HTTP and SSH
# EXPOSE 80 2222

# # Set the entrypoint and command to use OpenRC's init system
# ENTRYPOINT ["/sbin/init"]



# # Base setup with Alpine and SSHD
# FROM alpine:3.9 as alpine-systemd
# RUN apk --update --no-cache add openrc python && \
#     ln -sf /sbin/openrc-init /sbin/init

# ENTRYPOINT ["/sbin/init"]

# FROM alpine-systemd as alpine-nginx-sshd

# # Install necessary packages including Nginx and SSH
# RUN apk update && \
#     apk add nginx openssh bash && \
#     apk add bash git openssh rsync augeas shadow && \
#     deluser $(getent passwd 33 | cut -d: -f1) 2>/dev/null || true && \
#     delgroup $(getent group 33 | cut -d: -f1) 2>/dev/null || true && \
#     mkdir -p ~root/.ssh /etc/authorized_keys && chmod 700 ~root/.ssh/ && \
#     echo "Port 2223" >> /etc/ssh/sshd_config && \
#     echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
#     ssh-keygen -A && \
#     rm /etc/nginx/conf.d/default.conf

# # Add your custom Nginx configuration
# COPY nginx.conf /etc/nginx/nginx.conf

# # Assuming id_rsa_container.pub is your public key for SSH access,
# # ensure it's located at ./secrets/id_rsa_container.pub relative to the Dockerfile.
# # COPY ../secrets/id_rsa_container.pub /root/.ssh/authorized_keys

# # Ensure permissions are correct
# RUN chmod 600 /root/.ssh/authorized_keys && \
#     chmod 700 /root/.ssh

# # Expose the Nginx port and the SSH port
# EXPOSE 80 2226

# # Custom entrypoint script to start SSHD and Nginx
# COPY docker-entrypoint.sh /entry.sh
# RUN chmod a+x /entry.sh
# ENTRYPOINT ["/entry.sh"]

# # This CMD starts SSHD in the foreground. Adjust as necessary for your entrypoint script.
# CMD ["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]



# Base setup with Alpine and OpenRC
FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
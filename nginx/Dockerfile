FROM tiangolo/nginx-rtmp

# Copy nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Create HLS directory
RUN mkdir -p /tmp/hls && chmod -R 777 /tmp/hls

# Create HTML directory for simple web player
RUN mkdir -p /var/www/html
COPY player.html /var/www/html/index.html

# Expose ports
EXPOSE 1935
EXPOSE 8080

# Start Nginx without daemon mode (it's already set in the base image)
CMD ["nginx", "-g", "daemon off;"] 
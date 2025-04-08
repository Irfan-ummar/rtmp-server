FROM tiangolo/nginx-rtmp

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for HTML files
RUN mkdir -p /var/www/html

# Copy HTML files
COPY html/ /var/www/html/

# Create HLS directory with proper permissions
RUN mkdir -p /tmp/hls && \
    chown -R nginx:nginx /tmp/hls

# Expose ports
EXPOSE 1935
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 
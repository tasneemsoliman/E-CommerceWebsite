# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy your frontend files into the NGINX html directory
COPY . /usr/share/nginx/html

# Expose port 80 (NGINX default port)
EXPOSE 80

# Command to start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]

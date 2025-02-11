# Use a Node.js image optimized for Alpine Linux
FROM node:22-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package files and install dependencies
COPY package.json yarn.lock ./
RUN yarn install

# Copy the rest of the React app code into the container
COPY . .

# Expose port 3000 for the React development server
EXPOSE 3000

# Start the React app (using the development server)
CMD ["yarn", "dev"]
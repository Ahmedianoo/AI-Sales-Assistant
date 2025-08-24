# Use a base Node.js image for the frontend
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
#COPY package.json .
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port where Next.js will run
EXPOSE 3000

# Command to run the Next.js application
CMD ["npm", "run", "dev"]
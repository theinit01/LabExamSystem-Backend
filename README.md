# **Code Runner System**

## **1. Project Overview**

This project allows users to submit and execute code written in **Python** and **C** through pre-warmed Docker containers. A **proxy server** routes incoming requests to the appropriate backend container based on the specified programming language.

## **2. Directory Structure**
```project-root/
├── python-runner/          # Service to execute Python code
│   ├── app.py              # Flask app to execute Python code
│   ├── Dockerfile          # Dockerfile for Python runner
├── c-runner/               # Service to execute C code
│   ├── app.py              # Flask app to compile and execute C code
│   ├── Dockerfile          # Dockerfile for C runner
├── proxy-server/           # Proxy server to route requests
│   ├── app.py              # Flask app acting as the proxy
│   ├── Dockerfile          # Dockerfile for Proxy server
├── docker-compose.yml      # Compose file to spin up all services
```
## **3. Services**
### **Python Runner**

-   **Description**: Executes Python code sent from the frontend.
-   **Endpoint**: `POST /execute`
-   **Port**: `5001` (containerized)
-   **Request Format** (JSON):
    
   ```json
   { 
	   "code": "for i in range(5): print(i)" 
}
   ```
   **Response**:

```json
{ 
	"output": "0\n1\n2\n3\n4\n", 
	"error": "" 
}
```
### **Proxy Server**

-   **Description**: Routes incoming requests to the appropriate runner container (Python or C) based on the **language** specified in the request.
-   **Endpoint**: `POST /execute`
-   **Port**: `5000` (accessible from host)
-   **Request Format** (JSON):
    
  ```json
{ 
	"language": "python", 
	"code": "for i in range(5): print(i)"
}
```
    
-   **Response**:
 ```json
{ 
	"output": "0\n1\n2\n3\n4\n", 
	"error": "" 
}
```

## **4. How to Run the Project**

1.  **Prerequisites**
    
    -   Install **Docker** and **Docker Compose** on your machine.
2.  **Build and Run the Services**
    
    -   Navigate to the project root directory.
    -   Run the following command to build and start all containers:
        `docker-compose up --build` 
        
3.  **Access the Proxy Server**
    
    -   The proxy server will be accessible at:        
        `http://localhost:8080/execute` 
        
4.  **Example Requests**
    
    -   Use tools like **Postman** or `curl` to send POST requests to the proxy server.
    
    **Python Code Example:**

    `curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{
        "language": "python",
        "code": "for i in range(5): print(i)"
    }'` 
    
    **C Code Example:**

    `curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{
        "language": "c",
        "code": "#include <stdio.h>\nint main() {\n   printf(\"Hello, World!\\n\");\n   return 0;\n}"
    }'`

## **5. Notes**

-   Ensure that **ports 5000, 5001, and 5002** are free on your host machine.
-   The proxy server is the single entry point for code execution.

----------

## **6. Cleanup**

To stop and remove the containers, run:
`docker-compose down` 

----------

### **7. Future Improvements**

-   Add support for additional programming languages.
-   Implement authentication to restrict access.
-   Use Kubernetes for container orchestration in production.

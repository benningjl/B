import socket
import threading
import logging
import os

class NetworkManager:
    def __init__(self, host="127.0.0.1", port=8080):
        """
        Initialize the NetworkManager to manage server and client communication.
        :param host: Host IP address to bind the server.
        :param port: Port number to bind the server.
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_threads = []
        self.logger = self.setup_logger()

    def setup_logger(self):
        """Sets up logging for the NetworkManager."""
        logger = logging.getLogger("NetworkManagerLogger")
        logger.setLevel(logging.INFO)

        # Ensure log directory exists
        log_dir = "F:/B/logs"
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "network_manager.log")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def start_server(self):
        """Starts the server and listens for incoming connections."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.logger.info(f"Server started on {self.host}:{self.port}")

            # Start a thread to accept incoming connections
            threading.Thread(target=self.accept_connections, daemon=True).start()
        except Exception as e:
            self.logger.error(f"Error starting server: {e}")
            raise

    def accept_connections(self):
        """Accepts incoming client connections."""
        self.logger.info("Waiting for client connections...")
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.logger.info(f"Connection established with {client_address}")

                # Start a thread to handle the client
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_address), 
                    daemon=True
                )
                client_thread.start()
                self.client_threads.append(client_thread)
            except Exception as e:
                self.logger.error(f"Error accepting connection: {e}")

    def handle_client(self, client_socket, client_address):
        """
        Handles communication with a connected client.
        :param client_socket: The socket object for the connected client.
        :param client_address: The address of the connected client.
        """
        try:
            while True:
                # Receive message from client
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break  # Client disconnected
                self.logger.info(f"Received from {client_address}: {message}")

                # Send acknowledgment back to client
                response = f"Message received: {message}"
                client_socket.send(response.encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            self.logger.info(f"Connection closed with {client_address}")

    def stop_server(self):
        """Stops the server and closes all client connections."""
        self.logger.info("Stopping server...")
        try:
            # Close all client connections
            for thread in self.client_threads:
                thread.join(timeout=1)

            if self.server_socket:
                self.server_socket.close()
                self.logger.info("Server socket closed.")
        except Exception as e:
            self.logger.error(f"Error stopping server: {e}")

if __name__ == "__main__":
    # Example usage of NetworkManager
    network_manager = NetworkManager(host="127.0.0.1", port=8080)

    try:
        network_manager.start_server()
        while True:
            pass  # Keep the server running
    except KeyboardInterrupt:
        network_manager.stop_server()
    except Exception as e:
        network_manager.logger.error(f"Unexpected error: {e}")

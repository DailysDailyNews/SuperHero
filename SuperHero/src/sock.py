import socket
import threading
import logging

#Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -%(levelname)s - %(message)s')

# Define Custom Ports
PORTS_TO_BLOCK =[80, 443, 22, 3389, 135, 139, 445, 1433, 1434, 3306, 5432, 5900, 5938]

# List to store active sockets
active_sockets = []

def block_incoming_connection(client_socket, client_address):
   """ Blocks and Logs and incoming connection."""
   try:
     logging.warning(f"Blocking incoming connection from {client_address[0]}: {client_address[1]}")
     client_socket.close()
   except Exception as e:
     logging.error(f"Error blocking incoming connection: {e}")

def handle_socket(port):
   """Creates a socket and listens for incoming connections."""
   try:
     server_socket = socket.socket(sockey.AF_INET, socket.SOCK_STREAM)
     server_socket.bind(('0.0.0.0', port)) # Add to the list of active sockets
     server_socket.listen(1) # Only 1 connection at a time
     active_sockets.append(server_socket) #Adds to active socket list
     logging.info(f"Listening on port {port}...")

     while True:
       client_socket, client_address = server_socket.accept()
       block_incoming_connection(client_socket, client_address)

   except OSError as e:
     if e.errno == socket.errno.EADDRINUSE:
       logging.warning(f"Port {port} is already in use.
Skipping...)
     else:
       logging.error(f"Error creating socket on port {port}: {e}")

  except Exception as e:
    logging.error(f"Error creating socket on port {port}: {e}")
  finally:
    try:
      active_sockets.remove(server_socket) #Remove socket from list
      server_socket.close()
  except (NameError, ValueError):
      pass

def block_all_ports():
   """Creates threads to block incoming connections on all ports."""
   threads = []
   for port in PORTS_TO_BLOCK:
     thread = threading.Thread(target=handle_socket, args=(port,))
     threads.append(thread)
     thread.start()

     for thread in threads:
       thread.join(180) #Wait for 180 seconds

def close_all_sockets():
  """Closes all active sockets."""
  for sock in active_sockets:
    try:
      sock.close()
      logging.info(f"Error closing socket: {e}")

if __name__ == "__main__":
  try:
    block_all_ports()
  except KeyboadInterrupt:
    logging.info("Shutting down...")
finally:
    close_all_sockets()
    logging.info("Shutdown complete.")
       

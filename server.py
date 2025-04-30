import socket
import select

HOST = '127.0.0.1'
PORT = 12345

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    print(f"Server started on {HOST}:{PORT}, waiting for 2 players...")

    inputs = [server_socket]
    clients = []

    try:
        # Wait for 2 players to connect
        while len(clients) < 2:
            readable, _, _ = select.select(inputs, [], [])
            for s in readable:
                if s is server_socket:
                    client_socket, addr = server_socket.accept()
                    print(f"Player connected from {addr}")
                    clients.append(client_socket)
                    inputs.append(client_socket)

        judge, guesser = clients[0], clients[1]

        # Ask the judge for the secret number
        judge.sendall(b"Enter the secret number:")
        secret_number_data = judge.recv(1024)
        if not secret_number_data:
            raise Exception("No secret number received.")
        try:
            secret_number = int(secret_number_data.decode().strip())
        except ValueError:
            judge.sendall(b"Invalid number. Closing connection.")
            raise

        print(f"Secret number is: {secret_number}")
        guesser.sendall(b"Start guessing the number:")

        # Main guessing loop
        while True:
            guess_data = guesser.recv(1024)
            if not guess_data:
                break

            guess = guess_data.decode().strip()
            print(f"Guesser guessed: {guess}")

            try:
                g = int(guess)
                if g < secret_number:
                    feedback = "Too low"
                elif g > secret_number:
                    feedback = "Too high"
                else:
                    feedback = "Correct!"
            except ValueError:
                feedback = "Please enter a valid number."

            guesser.sendall(feedback.encode())
            if feedback == "Correct!":
                judge.sendall(b"The guesser guessed correctly!")
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        for client in clients:
            try:
                client.close()
            except:
                pass
        server_socket.close()
        print("Server shut down.")

if _name_ == "_main_":
    start_server()
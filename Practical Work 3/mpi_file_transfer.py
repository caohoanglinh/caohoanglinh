from mpi4py import MPI
import os
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

CHUNK = 4096

if rank == 0:  # SENDER
    filename = input("Enter file to send: ").strip()

    if not os.path.exists(filename):
        print("File not found!")
        sys.exit(0)

    filesize = os.path.getsize(filename)

    # Send metadata
    comm.send(os.path.basename(filename), dest=1)
    comm.send(filesize, dest=1)

    with open(filename, "rb") as f:
        sent = 0
        while sent < filesize:
            data = f.read(CHUNK)
            comm.send(data, dest=1)
            sent += len(data)

    print("Sender done.")

elif rank == 1:  # RECEIVER
    filename = comm.recv(source=0)
    filesize = comm.recv(source=0)

    output_file = "received_" + filename

    with open(output_file, "wb") as f:
        received = 0
        while received < filesize:
            data = comm.recv(source=0)
            f.write(data)
            received += len(data)

    print("Receiver saved:", output_file)

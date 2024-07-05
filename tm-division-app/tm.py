#!/usr/bin/env python3

from pytm import (TM, Server, Dataflow, Boundary, 
    Actor, Process, Data)

# Define the Threat Model
tm = TM("Simple Division Calculator Threat Model")
tm.description = "A threat model for a division calculator"
tm.isOrdered = True

# Define boundaries
internet = Boundary("Internet")
web_app_boundary = Boundary("Web Application")
web_server_boundary = Boundary("Server")
web_server_boundary.inBoundary = web_app_boundary
process_boundary = Boundary("Process")
process_boundary.inBoundary = web_app_boundary

# Define actors
user = Actor("User")
user.inBoundary = internet

# Define server and controls
web_server = Server("Web Server")
web_server.inBoundary = web_server_boundary

# Define processes
process_division = Process("Division Process")
process_division.inBoundary = process_boundary
process_division.controls.sanitizesInput = False

# Define data
dividend = Data("Dividend")
divisor = Data("Divisor")
division_result = Data("Division Result")
error_message = Data("Error Message")

# Define data flows
user_to_server = Dataflow(user, web_server, "User provides inputs")
user_to_server.protocol = "HTTP"
user_to_server.dstPort = 80
user_to_server.data = [dividend, divisor]

server_to_process = Dataflow(web_server, process_division, 
                             "Server sends inputs to division process")
server_to_process.data = [dividend, divisor]
server_to_process.protocol = "Flask"
server_to_process.dstPort = 5000
server_to_process.dstProcess = process_division

process_to_server = Dataflow(process_division, web_server, 
                             "Division process returns result or error")
process_to_server.data = [division_result, error_message]
process_to_server.protocol = "Flask"
process_to_server.srcPort = 5000
process_to_server.srcProcess = process_division


server_to_user = Dataflow(web_server, user, 
                          "Server returns result or error")
server_to_user.protocol = "HTTP"
server_to_user.data = [division_result, error_message]

# Process the threat model
if __name__ == "__main__":
    tm.process()

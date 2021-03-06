
import random
import time

import station


class NullMac(station.Station):
	'''
	`NullMac` is essentially having no MAC protocol. The node sends
	whenever it has a packet ready to send, and tries up to two retries
	if it doesn't receive an ACK.

	The node makes no attempt to avoid collisions.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)

	def run(self):
		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()

			# Try up to three times to send the packet successfully
			for i in range(0, 3):
				self.send('DATA')

				# Wait for a possible ACK. If we get one, we are done with this
				# packet. If all of our retries fail then we just consider this
				# packet lost and wait for the next one.
				recv = self.receive()
				if recv == 'ACK':
					break


class NullMacExponentialBackoff(station.Station):
	'''
	`NullMacExponentialBackoff` extends the basic NullMac to add exponential
	backoff if a packet is sent and an ACK isn't received.

	The sender should use up to two retransmissions if an ACK is not received.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)

	def run(self):
		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()

			# Implement NullMacExponentialBackoff here.
			for i in range(1, 4):
				self.send('DATA')
				recv = self.receive()
				if recv != 'ACK':
					k = random.randint(0, 2**(i)-2)
					time.sleep(self.interval*k)
				else:
					break
 
class CSMA_CA(station.Station):
	'''
	`CSMA_CA` should implement Carrier Sense Multiple Access with Collision
	Avoidance. The node should only transmit data after sensing the channel is
	clear.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)

	def run(self):
		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()

			# Implement CSMA/CA here.
			retransmission = 0
			while True:
				waitTime = random.randint(0,2**retransmission-1)*self.interval
				if self.sense():
					continue
				else:
					self.send("DATA")
					rec = self.receive()
					if rec != "ACK":
						retransmission = retransmission + 1
						time.sleep(waitTime)
					else:
						break


class RTS_CTS(station.Station):
	'''
	`RTS_CTS` is an extended CSMA/CA scheme where the transmitting station also
	reserves the channel using a Request to Send packet before transmitting. In
	this network, receiving a CTS message reserves the channel for a single DATA
	packet.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)

	def run(self):
		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()

			# Implement CSMA/CA + RTS/CTS here.
			col = 0
			while self.sense():
				continue

			self.send("RTS")
			re = self.receive()
			if re == "CTS":
				retransmission = 0
				while True:
					waitTime = random.randint(0, 2**retransmission-1)*self.interval
					self.send("DATA")
					re = self.receive()
					if re != "ACK":
						retransmission = retransmission + 1
						time.sleep(waitTime)
					else:
						break

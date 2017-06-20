import sys
import msvcrt
import hashlib
import os
import json
import client

def get_server(cpps):
	filename = os.path.join(os.path.dirname(__file__), "json/servers.json")
	with open(filename) as file:
		data = json.load(file)
	if not cpps in data:
		sys.exit("CPPS not found")
	return data[cpps]

def get_password(cpps, user, remember = True):
	filename = os.path.join(os.path.dirname(__file__), "json/penguins.json")
	try:
		with open(filename) as file:
			data = json.load(file)
	except:
		data = {}
	if cpps in data and user in data[cpps]:
		return data[cpps][user], True
	
	print "Password: ",
	password = ""
	special = False
	while True:
		c = msvcrt.getch()
		if special:
			special = False
		elif c == '\r' or c == '\n':
			break
		elif c == '\b':
			if len(password) > 0:
				sys.stdout.write("\b \b")
				password = password[:-1]
		elif c == '\xe0':
			special = True
		elif 32 <= ord(c) < 127:
			sys.stdout.write('*')
			password += c
	print ""
	
	if remember and raw_input("Remember? [y/N] ") == "y":
		if not cpps in data:
			data[cpps] = {}
		data[cpps][user] = hashlib.md5(password).hexdigest()
		with open(filename, "w") as file:
			json.dump(data, file)
	return password, False

def help(client, params):
	print """HELP"""

def room(client, params):
	if len(params) > 0:
		client.room(params[0])
	else:
		# TODO
		pass
	
def color(client, params):
	if len(params) > 0:
		client.update_color(params[0])
	else:
		# TODO
		pass

def head(client, params):
	if len(params) > 0:
		client.update_head(params[0])
	else:
		# TODO
		pass

def face(client, params):
	if len(params) > 0:
		client.update_face(params[0])
	else:
		# TODO
		pass

def neck(client, params):
	if len(params) > 0:
		client.update_neck(params[0])
	else:
		# TODO
		pass

def body(client, params):
	if len(params) > 0:
		client.update_body(params[0])
	else:
		# TODO
		pass

def hand(client, params):
	if len(params) > 0:
		client.update_hand(params[0])
	else:
		# TODO
		pass

def feet(client, params):
	if len(params) > 0:
		client.update_feet(params[0])
	else:
		# TODO
		pass

def pin(client, params):
	if len(params) > 0:
		client.update_pin(params[0])
	else:
		# TODO
		pass

def background(client, params):
	if len(params) > 0:
		client.update_background(params[0])
	else:
		# TODO
		pass

def walk(client, params):
	if len(params) < 2:
		# TODO
		pass
	else:
		client.walk(params[0], params[1])

def dance(client, params):
	client.dance()

def wave(client, params):
	client.wave()

def sit(client, params):
	if len(params) > 0:
		client.sit(params[0])
	else:
		# TODO
		pass

def snowball(client, params):
	if len(params) < 2:
		# TODO
		pass
	else:
		client.snowball(params[0], params[1])

def say(client, params):
	if len(params) > 0:
		client.say(' '.join(params))
	else:
		# TODO
		pass

def joke(client, params):
	if len(params) > 0:
		client.joke(params[0])
	else:
		# TODO
		pass

def emote(client, params):
	if len(params) > 0:
		client.emote(params[0])
	else:
		# TODO
		pass

def item(client, params):
	if len(params) > 0:
		client.add_item(params[0])
	else:
		# TODO
		pass

def follow(client, params):
	client.follow(' '.join(params))

def unfollow(client, params):
	client.unfollow()

def logout(client, params):
	client.logout()
	sys.exit(0)

if __name__ == "__main__":
	cpps = "cpr"
	data = get_server(cpps)
	user = raw_input("Username: ")
	password, encrypted = get_password(cpps, user)
	server = raw_input("Server: ").lower()
	
	ip = data["ip"]
	login_port = data["login"]
	game_port = data["servers"]
	if not server in game_port:
		sys.exit("Server not found")
	game_port = game_port[server]
	
	client = client.Client(ip, login_port, game_port)
	if not client.log:
		print "Connecting..."
	connected = client.connect(user, password, encrypted)
	if connected:
		print "Connected!"
		
		commands = {
			"help": help,
			"room": room,
			"color": color,
			"head": head,
			"face": face,
			"neck": neck,
			"body": body,
			"hand": hand,
			"feet": feet,
			"pin": pin,
			"background": background,
			"walk": walk,
			"dance": dance,
			"wave": wave,
			"sit": sit,
			"snowball": snowball,
			"say": say,
			"joke": joke,
			"emote": emote,
			"item": item,
			"follow": follow,
			"unfollow": unfollow,
			"logout": logout
		}
		
		while True:
			print ">>>",
			cmd = raw_input().split(' ')
			name = cmd[0]
			params = cmd[1:]
			if name in commands:
				commands[name](client, params)
			else:
				print "command '" + name + "' doesn't exist"
	else:
		sys.exit("Failed to connect")
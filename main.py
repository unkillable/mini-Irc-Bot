import socket, os, random
if os.path.isfile('quotes.py'): pass
else: f = open("quotes.py", "w+"); f.write("quotes_list = []"); f.close(); from quotes import quotes_list
host = "irc.niggerbread.me"; port = 6667; nick = "Kaya"; chan = "#k"; s = socket.socket(); s.connect((host, port)); connected = True; #config
for packet in ["NICK {0}\r\n".format(nick), "USER {0} {0} {0} :{0}\r\n".format(nick), "JOIN %s" % chan + "\r\n"]: s.send(packet);
while connected:
	data = s.recv(1024).strip(); print data;
	if data.startswith("PING "): s.send("PONG %s\r\n" % data.split(" ")[1])
	if "PRIVMSG " in data: chan = data.split("PRIVMSG ")[1].split(" :")[0].strip();
	if "~join " in data: s.send("JOIN %s\r\n" % data.split("~join ")[1])
	if " 396 " in data or " 376 " in data: s.send("JOIN %s\r\n" % chan)
	if "~part " in data: s.send("PART %s\r\n" % data.split("~part ")[1])
	if "~quotes add " in data: quotes_list.append(data.split("~quotes add ")[1]); f = open('quotes.py', 'w+'); f.write("quotes_list = {0}".format(quotes_list)); f.close(); s.send("PRIVMSG %s :Quote was added!\r\n" % chan);
	if "~quotes del " in data: 
		try: del quotes_list[int(data.split("~quotes del ")[1])]; f = open('quotes.py', 'w+'); f.write("quotes_list = {0}".format(quotes_list)); f.close(); s.send("PRIVMSG %s :Quote was deleted!\r\n" % chan); 
		except Exception as e: s.send("PRIVMSG %s :Quote ID not found!\r\n" % chan);
	if "~quotes rand" in data: s.send("PRIVMSG %s :%s\r\n" % (chan, random.choice(quotes_list)));
	if "" in data: s.close(); print "Disconnected from server"

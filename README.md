# 🛰️ Python TCP Proxy Tool

A minimal yet powerful TCP proxy built in Python, designed for traffic interception, debugging, and learning about networking. Inspired by tools like `netcat` and `mitmproxy`, this proxy helps visualize and manipulate data flowing between a client and a server.

---

## 🚀 Features

- Bind and listen on a local port
- Connect and relay to a remote host/port
- Hexdump of all transmitted data
- Packet inspection and modification stubs (`request_handler`, `response_handler`)
- Works seamlessly on Kali Linux

---

## 🔧 Usage

```bash
python3 TCP_Proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]

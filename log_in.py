import json

print("Please enter your MySQL username: (You can leave blank if your username is 'root'")
username = input()

print("Please enter your MySQL password:")
password = input()

print("Please enter your MySQL database name: (You can leave blank if your database is 'ttsh'")
database = input()

if username == "":
	username = "root"

if database == "":
	database = "ttsh"

data = {
	"username": username,
	"password": password,
	"database": database,

}

with open('blockMapping/JSON/log_in.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
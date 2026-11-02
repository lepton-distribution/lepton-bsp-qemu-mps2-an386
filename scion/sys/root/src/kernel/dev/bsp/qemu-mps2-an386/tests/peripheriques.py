#!/usr/bin/env python3
"""peripheriques.py — test du BSP qemu-mps2-an386 : périphériques présents dans /dev (TST-2).

Lance QEMU (UART0 sur stdin/stdout), attend l'invite de lsh, exécute « ls /dev » et vérifie que
chaque nom donné par --expect y figure. La console est celle de smoke_lsh.py du greffon noyau,
désigné par --tests-noyau (le script est greffé en lien : son répertoire n'est pas celui du noyau).
Code de retour 0 si tous les noms sont présents.
"""
import argparse
import os
import re
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tests-noyau", required=True, help="répertoire tests/ du greffon noyau")
    ap.add_argument("--qemu", default="qemu-system-arm")
    ap.add_argument("--machine", required=True)
    ap.add_argument("--kernel", required=True)
    ap.add_argument("--expect", action="append", required=True, help="nom attendu dans /dev")
    ap.add_argument("--boot-timeout", type=float, default=30.0)
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--log", required=True)
    args = ap.parse_args()

    sys.path.insert(0, args.tests_noyau)
    from smoke_lsh import PROMPT, Console, run_command  # noqa: E402

    cmd = [args.qemu, "-M", args.machine, "-kernel", args.kernel, "-nographic",
           "-monitor", "none", "-serial", "stdio", "-serial", "null"]
    failures = []
    with open(args.log, "wb") as log:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        con = Console(proc, log)
        try:
            # l'invite n'apparaît qu'après une touche (initd : « any key to continue »)
            if con.read_until(re.compile(rb"any key to continue|lepton#\d+\$ "), args.boot_timeout) is None:
                failures.append("démarrage : ni invite initd ni invite lsh")
            else:
                con.send("")
                if con.read_until(PROMPT, args.timeout) is None:
                    failures.append("invite lsh absente")
            if not failures:
                out = run_command(con, "ls /dev", args.timeout)
                if out is None:
                    failures.append("ls /dev : pas de retour à l'invite")
                else:
                    names = set(out.decode(errors="replace").split())
                    failures += ["/dev/%s absent (ls /dev : %s)" % (n, " ".join(sorted(names)))
                                 for n in args.expect if n not in names]
        finally:
            proc.kill()
            proc.wait()
    for f in failures:
        print("ÉCHEC : " + f)
    print("peripheriques : %s, %d nom(s) attendu(s), %s ; journal %s"
          % (args.machine, len(args.expect), "échec" if failures else "présents", args.log))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

# simple_blockchain
PoW + block design &amp; verification


Usage of proof_of_work.py:

proof_of_work.py create [-h] [-z ZEROBYTES] [-t TEXT] [-f FILE]
proof_of_work.py validate [-h] [-z ZEROBYTES] [-f FILE]

options:
  -h, --help            show this help message and exit
  -z ZEROBYTES, --zerobytes ZEROBYTES
                        Number of zero bytes for block hash
  -t TEXT, --text TEXT  Text data for a block
  -f FILE, --file FILE  Path to blockchain json database to write

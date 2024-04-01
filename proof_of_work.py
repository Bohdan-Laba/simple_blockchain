from hashlib import sha256
import json
import os
import sys
import argparse

class Block:
    def __init__(self, block_hash, data, nonce, prev_hash):
        self.data = data
        self.nonce = nonce
        self.prev_hash = prev_hash
        self.block_hash = block_hash

    def to_dict(self):
        return {'Block_hash': self.block_hash, 'Data': self.data, 'Nonce': self.nonce, "Prev_hash": self.prev_hash}

    @classmethod
    def from_dict(cls, data):
        return cls(data['Block_hash'], data['Data'], data['Nonce'], data['Prev_hash'])


def get_block_hash(data: str, prev_hash: str, starting_zeros: int) -> tuple[str,str,int,str]:
    nonce = 0
    #Proof of work
    hash_block = sha256(bytes(data + prev_hash + str(nonce), 'utf-8')).hexdigest()
    # print(hash_block)
    while (not hash_block.startswith(starting_zeros*'0')):
        nonce +=1
        hash_block = sha256(bytes(data + prev_hash + str(nonce), 'utf-8')).hexdigest()
        # print(hash_block)

    print('Found hash with nonce: ', nonce)
    print(hash_block)

    return (hash_block,data,nonce,prev_hash)

def validate_block(block: object, starting_zeros: int) -> None:
    data = block.data
    nonce = block.nonce
    prev_hash = block.prev_hash

    hash_block = sha256(bytes(data + prev_hash + str(nonce), 'utf-8')).hexdigest()
    if (hash_block.startswith(starting_zeros*'0')):
        print('Block validated!')
    else:
        print('Validation failed!')


def create_block(block_data: tuple[str,str,int,str]) -> object:
    block_hash, data, nonce, prev_hash = block_data
    block = Block(block_hash, data, nonce, prev_hash)

    return block

def create_from_json(json_file_path: str) -> list[object]:
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    blocks_data = data['block']
    blocks = []
    for i in range(len(blocks_data)):
        blocks.append(Block.from_dict(blocks_data[i]))

    return blocks

def write_data(block: object, json_file_path: str) -> None:
    dict_block = block.to_dict()
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data['block'].append(dict_block)
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)    
    print("Block inserted to file successfully")



parser = argparse.ArgumentParser(description='Basic Proof of Work program')

subparser = parser.add_subparsers(dest = 'command')

create_parser = subparser.add_parser('create', help = "Create a block")
validate_parser = subparser.add_parser('validate', help = "Validate last block")

create_parser.add_argument("-z", "--zerobytes", type=int,
                    help = "Number of zero bytes for block hash")
create_parser.add_argument("-t", "--text", type=str,
                    help = "Text data for a block")
create_parser.add_argument("-f", "--file", type=str,
                    help = "Path to blockchain json database to write")

validate_parser.add_argument("-z", "--zerobytes", type=int,
                    help = "Number of zero bytes for block hash")
validate_parser.add_argument("-f", "--file", type=str,
                    help = "Path to blockchain json database to read")

args = parser.parse_args(args=None if sys.argv[2:] else ['--help'])
starting_zeros = args.zerobytes // 4
json_file_path = args.file
blocks = create_from_json(json_file_path)

match args.command:

    case 'create':
        prev_hash = blocks[-1].block_hash
        block_data = get_block_hash(args.text, prev_hash, starting_zeros)
        block = create_block(block_data)
        write_data(block, json_file_path)

    case 'validate':
        validate_block(blocks[-1], starting_zeros)

os.system('pause')

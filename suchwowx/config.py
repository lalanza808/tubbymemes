from os import getenv
from dotenv import load_dotenv

load_dotenv()

# App
SECRET_KEY = getenv('SECRET_KEY', 'yyyyyyyyyyyyy')
DATA_FOLDER = getenv('DATA_FOLDER', '/path/to/uploads')
SERVER_NAME = getenv('SERVER_NAME', '127.0.0.1:5000')
IPFS_SERVER = getenv('IPFS_SERVER', 'http://127.0.0.1:8080')

# Cache
CACHE_HOST = getenv('CACHE_HOST', 'localhost')
CACHE_PORT = getenv('CACHE_PORT', 6379)

# Uploads
SESSION_TYPE = 'filesystem'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'mp4', 'webp'}
MAX_CONTENT_LENGTH = 32 * 1024 * 1024
TEMPLATES_AUTO_RELOAD = getenv('TEMPLATES_AUTO_RELOAD', True)

# Contract
CONTRACT_TESTNET = getenv('TESTNET', True)
CONTRACT_ADDRESS = '0x9797afc5d0258704109f71109188fdcba19c24c2'  # Fuji
CONTRACT_ABI = [
  {
    'inputs': [],
    'stateMutability': 'nonpayable',
    'type': 'constructor'
  },
  {
    'anonymous': False,
    'inputs': [
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'owner',
        'type': 'address'
      },
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'approved',
        'type': 'address'
      },
      {
        'indexed': True,
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'Approval',
    'type': 'event'
  },
  {
    'anonymous': False,
    'inputs': [
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'owner',
        'type': 'address'
      },
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'operator',
        'type': 'address'
      },
      {
        'indexed': False,
        'internalType': 'bool',
        'name': 'approved',
        'type': 'bool'
      }
    ],
    'name': 'ApprovalForAll',
    'type': 'event'
  },
  {
    'anonymous': False,
    'inputs': [
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'previousOwner',
        'type': 'address'
      },
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'newOwner',
        'type': 'address'
      }
    ],
    'name': 'OwnershipTransferred',
    'type': 'event'
  },
  {
    'anonymous': False,
    'inputs': [
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'from',
        'type': 'address'
      },
      {
        'indexed': True,
        'internalType': 'address',
        'name': 'to',
        'type': 'address'
      },
      {
        'indexed': True,
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'Transfer',
    'type': 'event'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'to',
        'type': 'address'
      },
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'approve',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'owner',
        'type': 'address'
      }
    ],
    'name': 'balanceOf',
    'outputs': [
      {
        'internalType': 'uint256',
        'name': '',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'contractCreator',
    'outputs': [
      {
        'internalType': 'string',
        'name': '',
        'type': 'string'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'contractTipCutPercent',
    'outputs': [
      {
        'internalType': 'uint256',
        'name': '',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'contractVersion',
    'outputs': [
      {
        'internalType': 'string',
        'name': '',
        'type': 'string'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'getApproved',
    'outputs': [
      {
        'internalType': 'address',
        'name': '',
        'type': 'address'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'owner',
        'type': 'address'
      },
      {
        'internalType': 'address',
        'name': 'operator',
        'type': 'address'
      }
    ],
    'name': 'isApprovedForAll',
    'outputs': [
      {
        'internalType': 'bool',
        'name': '',
        'type': 'bool'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'string',
        'name': '',
        'type': 'string'
      }
    ],
    'name': 'metadataTokenId',
    'outputs': [
      {
        'internalType': 'uint256',
        'name': '',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'name',
    'outputs': [
      {
        'internalType': 'string',
        'name': '',
        'type': 'string'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'owner',
    'outputs': [
      {
        'internalType': 'address',
        'name': '',
        'type': 'address'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'ownerOf',
    'outputs': [
      {
        'internalType': 'address',
        'name': '',
        'type': 'address'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'publisherTipCutPercent',
    'outputs': [
      {
        'internalType': 'uint256',
        'name': '',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'renounceOwnership',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'from',
        'type': 'address'
      },
      {
        'internalType': 'address',
        'name': 'to',
        'type': 'address'
      },
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'safeTransferFrom',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'from',
        'type': 'address'
      },
      {
        'internalType': 'address',
        'name': 'to',
        'type': 'address'
      },
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      },
      {
        'internalType': 'bytes',
        'name': '_data',
        'type': 'bytes'
      }
    ],
    'name': 'safeTransferFrom',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'operator',
        'type': 'address'
      },
      {
        'internalType': 'bool',
        'name': 'approved',
        'type': 'bool'
      }
    ],
    'name': 'setApprovalForAll',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'bytes4',
        'name': 'interfaceId',
        'type': 'bytes4'
      }
    ],
    'name': 'supportsInterface',
    'outputs': [
      {
        'internalType': 'bool',
        'name': '',
        'type': 'bool'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'symbol',
    'outputs': [
      {
        'internalType': 'string',
        'name': '',
        'type': 'string'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': '',
        'type': 'uint256'
      }
    ],
    'name': 'tokenMeme',
    'outputs': [
      {
        'internalType': 'uint256',
        'name': 'publisherTipsAVAX',
        'type': 'uint256'
      },
      {
        'internalType': 'uint256',
        'name': 'creatorTipsAVAX',
        'type': 'uint256'
      },
      {
        'internalType': 'uint256',
        'name': 'contractTipsAVAX',
        'type': 'uint256'
      },
      {
        'internalType': 'address',
        'name': 'publisherAddress',
        'type': 'address'
      },
      {
        'internalType': 'address',
        'name': 'creatorAddress',
        'type': 'address'
      },
      {
        'internalType': 'string',
        'name': 'metadataIPFSHash',
        'type': 'string'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'from',
        'type': 'address'
      },
      {
        'internalType': 'address',
        'name': 'to',
        'type': 'address'
      },
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'transferFrom',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': 'newOwner',
        'type': 'address'
      }
    ],
    'name': 'transferOwnership',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'address',
        'name': '',
        'type': 'address'
      }
    ],
    'name': 'userProfile',
    'outputs': [
      {
        'internalType': 'string',
        'name': 'wowneroAddress',
        'type': 'string'
      },
      {
        'internalType': 'string',
        'name': 'userHandle',
        'type': 'string'
      },
      {
        'internalType': 'string',
        'name': 'metadataIPFSHash',
        'type': 'string'
      },
      {
        'internalType': 'uint256',
        'name': 'tippedAVAX',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'withdraw',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': 'percent',
        'type': 'uint256'
      }
    ],
    'name': 'setContractTipCut',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': 'percent',
        'type': 'uint256'
      }
    ],
    'name': 'setPublisherTipCut',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'totalSupply',
    'outputs': [
      {
        'internalType': 'uint256',
        'name': '',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'string',
        'name': 'wowneroAddress',
        'type': 'string'
      }
    ],
    'name': 'setUserWowneroAddress',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'string',
        'name': 'handle',
        'type': 'string'
      }
    ],
    'name': 'setUserHandle',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'string',
        'name': 'metadataIPFSHash',
        'type': 'string'
      }
    ],
    'name': 'setUserMetadata',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'string',
        'name': 'metadataIPFSHash',
        'type': 'string'
      },
      {
        'internalType': 'address',
        'name': 'creatorAddress',
        'type': 'address'
      }
    ],
    'name': 'mint',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'tipAVAX',
    'outputs': [],
    'stateMutability': 'payable',
    'type': 'function'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': 'tokenId',
        'type': 'uint256'
      }
    ],
    'name': 'tokenURI',
    'outputs': [
      {
        'internalType': 'string',
        'name': '',
        'type': 'string'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  }
]


# Logging
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'loggers': {
        'gunicorn.error': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
}

"""Execute every workshop notebook from repository root, retaining outputs outside Git."""
from pathlib import Path
import argparse
from traitlets.config import Config
import nbformat
from nbclient import NotebookClient

parser=argparse.ArgumentParser()
parser.add_argument('--ipc',action='store_true',help='Use Unix IPC on systems that restrict local TCP sockets')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
output=root/'outputs/executed-notebooks'
output.mkdir(parents=True,exist_ok=True)
for path in sorted((root/'notebooks').glob('*.ipynb')):
    nb=nbformat.read(path,as_version=4)
    config=Config({'KernelManager':{'transport':'ipc','ip':str(output/'ipc')}}) if args.ipc else Config()
    NotebookClient(nb,config=config,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
    nbformat.write(nb,output/path.name)
    print('Executed',path.name,flush=True)

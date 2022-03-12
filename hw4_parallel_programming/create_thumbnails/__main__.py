from functools import partial
from multiprocessing.pool import ThreadPool
from pathlib import Path
from threading import Lock
from time import perf_counter
from urllib import request, response

from hurry.filesize import size  # beautiful size representation
from PIL import Image, UnidentifiedImageError

from .cli import parser


def make_thumbnail(res: response, image_num: int,
                   max_res: tuple[int], dest_dir: Path):
    '''
    Make thumbnail of given file-like and save it.

    :param res: Response object containing image
    :param image_num: Number of image in original source
    :param max_res: Max resolution for thumbnail
    :param dest_dir: Directory to save the image in
    :return: 1 if thumbnail made successfully, None otherwise
    '''
    try:
        with Image.open(res) as im:
            im.thumbnail(max_res)
            fp = dest_dir / Path(f'{image_num:05}.jpg')
            with lock:
                im.save(fp)
            return 1  # success code
    except UnidentifiedImageError:
        return


def download_image(image_url: str) -> response:
    '''
    Download image by given url and return response object.

    :param image_url: Image url
    :return: Response object if downloaded successfully, None otherwise
    '''
    try:
        res = request.urlopen(image_url)
    except Exception:
        return
    else:
        return res


def download_and_process(image_num: int, image_url: str) -> None:
    '''
    Donwload image, make thumbnail and collect some statistics.

    :param image_num: Number of image in original source
    :param image_url: Image url
    '''
    global total_errors
    global total_downloads
    global total_processed
    global bytes_downloaded

    res = download_image(image_url)
    if not res:
        with lock:
            total_errors += 1
            print(f'{image_url} FAILED')
        return

    with lock:
        total_downloads += 1
        # Some responses that don't contain image
        # provide empty string as value of Content-Length header
        bytes_downloaded += int(res.getheader('Content-Length') or 0)
        print(f'{image_url} DOWNLOADED')

    is_ok = make_thumbnail(res, image_num)
    res.close()
    if is_ok:
        with lock:
            total_processed += 1
            print(f'{image_url} PROCESSED SUCCESSFULLY')


# Get command-line arguments
args = parser.parse_args()

# Fixate known parameters
make_thumbnail = partial(make_thumbnail,
                         max_res=args.max_res,
                         dest_dir=args.dest_dir)

# Create destination directory (and its parents) if doesn't exist
try:
    if not args.dest_dir.exists():
        Path.mkdir(args.dest_dir, parents=True)
except Exception:
    print(f'Error: {args.dest_dir} directory cannot be created.')
    exit()

# Mutex for writing, output and statistics
lock = Lock()

# Run statistics
total_downloads = 0
total_processed = 0
total_errors = 0
bytes_downloaded = 0
start_time = perf_counter()

with ThreadPool(processes=args.jobs) as pool:
    pool.starmap(download_and_process, enumerate(open(args.source), start=1))

end_time = perf_counter()
total_time = end_time - start_time

print('_'*40, '\n', 'SUMMARY'.center(40), '\n',
      f'Total downloads: {total_downloads}\n',
      f'Total traffic: {size(bytes_downloaded)}\n',
      f'Images processed: {total_processed}\n',
      f'Errors occures: {total_errors}\n\n',
      f'Total time: {total_time:.3f} sec.\n')

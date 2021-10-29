"""
Auxiliary script to create a sample from different data sources: new declaration dumps, new declaration api
and old stored declarations in previous format (offloaded).
Use with care
"""
import os
import os.path
from glob import glob
import random
import zipfile
from pathlib import Path
import shutil
import requests
from time import sleep

from tqdm.notebook import tqdm
import logging

logging.basicConfig()

logger = logging.getLogger("declarations_downloader")



class DataDownloaderException(Exception):
    pass


class DataDownloader:
    def __init__(
        self, input_dir, output_dir, sample_from_each, seed=0, skip_years=["2021"], wipe_output_dirs=True
    ):
        self.files_to_resolve = set()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.skip_years = skip_years
        self.sample_from_each = sample_from_each

        random.seed(seed)
        self.dump_dir = output_dir / "dump"
        self.api_dir = output_dir / "api"
        self.old_dir = output_dir / "old"

        dirs_to_create = [self.dump_dir, self.api_dir, self.old_dir]

        for d in dirs_to_create:
            if os.path.exists(d) and wipe_output_dirs and d == self.dump_dir:
                shutil.rmtree(d)

            if not os.path.exists(d):
                os.makedirs(d)

#             if glob(str(d / "*.json")):
#                 raise DataDownloaderException(f"{d} is non-empty")
        
        self.extract_dumps()
        # Now for the fun part
        self.download_from_api()
        self.store_file_ids()

    def extract_dumps(self):
        for dump in tqdm(glob(os.path.join(self.input_dir, "*/*.zip")), desc="Extracting sample from dumps"):
            if any(year in dump for year in self.skip_years):
                continue
            
            with zipfile.ZipFile(dump) as dump_zip:
                files = random.sample(dump_zip.namelist(), self.sample_from_each)
                
                for f in files:
                    with dump_zip.open(f, "r") as fp:
                        data = json.load(fp)
                        
                    base_name = os.path.basename(f)
                    with open(self.dump_dir / base_name, "w") as fp_out:
                        json.dump(
                            data, fp_out, ensure_ascii=False, indent=4, sort_keys=True
                        )
                    
                    self.files_to_resolve.add(os.path.splitext(base_name)[0])
    
    def download_from_api(self, sleep_for=0.5):
        for id_to_download in tqdm(self.files_to_resolve, desc="Downloading sample from api"):
            out_file = self.api_dir / f"{id_to_download}.json"
            if os.path.exists(out_file):
                logger.warning(f"{out_file} already exists, skipping it")
                continue

            resp = requests.get(f"https://public-api.nazk.gov.ua/v2/documents/{id_to_download}")
            
            if resp.status_code != 200:
                logger.error(f"Cannot download file {id_to_download}, error code is {resp.status_code}")
            
            with open(out_file, "w") as fp_out:
                json.dump(
                    resp.json(), fp_out, ensure_ascii=False, indent=4, sort_keys=True
                )

            sleep(sleep_for)

    def store_file_ids(self):
        with open(self.output_dir / "ids.txt", "w") as fp_out:
            for k in sorted(self.files_to_resolve):
                fp_out.write(f"{k}\n")

if __name__ == '__main__':
    # dd = DataDownloader(
    #     input_dir=Path("/Users/dchaplinsky/Projects/declarations/nacp_dumps"),
    #     output_dir=Path("/Users/dchaplinsky/Projects/declarations/sample"),
    #     sample_from_each=2000,
    # )

    # print(dd.files_to_resolve)
    pass
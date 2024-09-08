from os import path, makedirs, listdir, walk
from shutil import rmtree, move
from zipfile import ZipFile, BadZipFile
from requests import Session, exceptions
from requests.adapters import HTTPAdapter
from urllib3 import Retry
# from logging import basicConfig, getLogger, INFO

# # Configure logging
# basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = getLogger(__name__)

class ThemeDownloader:
    REPO_PROVIDERS = {
        "github.com": "/archive/refs/heads/master.zip",
        "gitlab.com": "/-/archive/main/main.zip",
        "codeberg.org": "/archive/main.zip",
        "git.gay": "/-/archive/main/main.zip"  # Assume similar to GitLab
    }

    def __init__(self, theme_data, extract_path, clean_install, base_dir=None):
        self.theme_data = theme_data
        self.extract_path = extract_path
        self.sanitized_title = self.sanitize_title(self.theme_data.title)
        self.zip_path = path.join(extract_path, f"{self.sanitized_title}.zip")
        self.theme_folder_path = path.join(extract_path, f"{self.sanitized_title}-main")
        self.download_url = self.construct_download_url(self.theme_data.link)
        self.clean_install = clean_install
        self.base_dir = base_dir

        makedirs(extract_path, exist_ok=True)

    def sanitize_title(self, title):
        # # Replace any problematic characters with underscores or remove them
        return title.replace('/', '_').replace('\\', '_')

    def construct_download_url(self, repo_link):
        # # Extract domain from the repository link
        domain = repo_link.split('/')[2]
        suffix = self.REPO_PROVIDERS.get(domain, None)
        if suffix:
            return repo_link + suffix
        else:
            # logger.error(f"Unsupported repository provider: {domain}")
            raise ValueError(f"Unsupported repository provider: {domain}")

    def theme_already_downloaded(self):
        return path.exists(self.theme_folder_path)

    def zip_file_exists_and_valid(self):
        if not path.exists(self.zip_path):
            return False
        try:
            with ZipFile(self.zip_path, 'r') as zip_ref:
                bad_file = zip_ref.testzip()
                if bad_file is not None:
                    # logger.error(f"Corrupt file detected in zip: {bad_file}")
                    return False
            return True
        except BadZipFile:
            # logger.error("Bad zip file detected.")
            return False

    def download_theme(self):
        if self.zip_file_exists_and_valid() and not self.clean_install:
            # logger.info("Zip file already downloaded and valid.")
            return True
                
        session = Session()
        retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            with session.get(self.download_url, stream=True, timeout=10) as response:
                response.raise_for_status()
                with open(self.zip_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
            # logger.info(f"Downloaded theme zip from {self.download_url}.")
            return True
        except exceptions.Timeout:
            # logger.error("Download timed out.")
            return False
        except exceptions.TooManyRedirects:
            # logger.error("Too many redirects.")
            return False
        except exceptions.RequestException as e:
            # logger.error(f"Request failed: {e}")
            return False

    def extract_theme(self):
        if self.theme_already_downloaded() and not self.clean_install:
            # logger.info("Theme already extracted.")
            return True

        # # Clean install: remove existing folder if it exists
        if self.clean_install and path.exists(self.theme_folder_path):
            rmtree(self.theme_folder_path)
            # logger.info("Existing theme directory removed for clean install.")

        try:
            # logger.info("Starting extraction...")
            with ZipFile(self.zip_path, "r") as zip_ref:
                # # Extract to a temporary directory first
                temp_extract_path = path.join(self.extract_path, "temp_extract")
                zip_ref.extractall(temp_extract_path)

                # # Find the actual extracted folder, which might have a varying name
                extracted_folders = [name for name in listdir(temp_extract_path) 
                                     if path.isdir(path.join(temp_extract_path, name))]
                
                if len(extracted_folders) != 1:
                    # logger.error("Unexpected structure in the extracted zip file.")
                    rmtree(temp_extract_path)
                    return False

                extracted_folder = path.join(temp_extract_path, extracted_folders[0])

                # # Rename the extracted folder to the desired theme folder path
                move(extracted_folder, self.theme_folder_path)

                # logger.info("Extraction completed successfully.")

                # # Clean up the temporary extraction directory
                rmtree(temp_extract_path)
                
                return True
        except BadZipFile as e:
            # logger.error(f"Failed to extract theme: {e}")
            return False
        except Exception as e:
            # logger.error(f"An unexpected error occurred during extraction: {e}")
            return False

    def check_theme_files(self):
        data_json_path = path.join(self.theme_folder_path, "data", "installer_files_data.json")

        if path.exists(data_json_path):
            # logger.info("Theme has its own data JSON.")
            self.user_js_target_dir = path.join(self.base_dir, "chrome")
            return {"type": "data", "path": data_json_path}

        for root, dirs, files in walk(self.theme_folder_path):
            if "userChrome.css" in files:
                # logger.info("Theme has userChrome.css file.")
                self.user_js_target_dir = root
                return {"type": "userChrome.css", "path": root}

        # logger.warning("No theme data or chrome/userChrome.css found.")
        return None

    def process_theme(self):
        try:
            if self.download_theme() and self.extract_theme():
                theme_data = self.check_theme_files()
                return theme_data
            return False
        except Exception as e:
            # logger.error(f"An error occurred: {e}")
            raise e
        
# # Example usage
# # theme_data = {
# #     'title': 'RealFire',
# #     'link': 'https://github.com/Hakanbaban53/RealFire'
# # }
# # theme_downloader = ThemeDownloader(
# #     theme_data=theme_data,
# #     extract_path="/path/to/extract",
# #     clean_install=False,
# #     base_dir="/path/to/base"
# # )
# # result = theme_downloader.process_theme()
# # print(result)

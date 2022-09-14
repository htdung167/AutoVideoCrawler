# AutoVideoCrawler
Easily download all the videos by keywords from Tiktok and Youtube

# How to download Tiktok videos
1. Install Chrome (notice the version of chrome driver in chromedriver folder)
2. Git clone:
```
git clone https://github.com/htdung167/AutoVideoCrawler.git
cd AutoVideoCrawler
```
3. Create env with conda:
```
conda create -n myenv
conda activate myenv
conda install pip
pip install --upgrade pip
pip install -r requirements.txt
```

4. Create ```.env``` file and fill your Tiktok account with Facebook in ```.env``` file (You need a activated Tiktok account with Facebook):
```
ACCOUNT_TIKTOK=<your nickname>
PASSWORD_TIKTOK=<password>
```
5. Write the keywords in ```keywords.txt``` file
6. Run:
```
python main.py --unique true --limit 30 --type tiktok
```
7.Files will be downloaded to 'download' directory.

# How to download Youtube videos
1. Install Chrome (notice the version of chrome driver in chromedriver folder)
2. Git clone:
```
git clone https://github.com/htdung167/AutoVideoCrawler.git
cd AutoVideoCrawler
```
3. Create env with conda:
```
conda create -n myenv
conda activate myenv
conda install pip
pip install --upgrade pip
pip install -r requirements.txt
```
4. Write the keywords in ```keywords.txt``` file
5. Run:
```
python main.py --unique true --limit 30 --type youtube
```

# Arguments
```
python main.py [--unique true] [--limit 30]
```
```
--unique true : Url of videos in keyword folders is different.
--limit 30 : Maximum count of videos to download per keyword.
--type tiktok: Use "tiktok" or "youtube" to download.
```
